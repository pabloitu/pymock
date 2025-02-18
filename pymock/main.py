import os
import sys
from datetime import datetime, timedelta
import numpy
from pymock import libs


def main(arg_path=None, folder=None, verbose=False):
    """
    Main pymock's function
    Contains the main steps of creating a forecast for a given time window.

    1. Parse an argument file
    2. Reads the input catalog
    3. Creates the forecast as synthetic catalogs
    4. Writes the synthetic catalogs

    params:
        arg_path (str): Path to the input arguments file.
        folder (str): (Optional) Path to save output. Defaults to 'forecasts'
        verbose (bool): print log
    """

    # Create a forecasts folder in current directory if it does not exist.
    folder = folder or os.path.join(os.path.dirname(arg_path), '../forecasts')
    os.makedirs(folder, exist_ok=True)

    # 1. Gets input data and arguments.
    args = libs.read_args(arg_path)  # A dictionary containing parameters

    cat_path = args.get('catalog')
    n_sims = args.get('n_sims', 1000)  # Gets from args or default to 1000
    seed = args.get('seed', None)  # Gets from args or default to seed

    # 2. Reads input catalog
    catalog = libs.load_cat(path=cat_path)

    # 3. Run model
    forecast = make_forecast(catalog,
                             args,
                             n_sims=n_sims,
                             seed=seed,
                             verbose=verbose)

    # 4. Write forecasts
    libs.write_forecast(args['start_date'], args['end_date'], forecast, folder)


def make_forecast(input_catalog, args, n_sims=1000, seed=None, verbose=True):
    """
    Routine to create a forecast from an input catalog and argument dictionary

    Args:
        input_catalog (list): A CSEP formatted events list (see libs.load_cat)
        args (dict): Contains the arguments and its values
        n_sims (int): Number of stochastic catalogs to create
        seed (int): seed for random number generation
        verbose (bool): Flag to print out the logging.
    """
    t0: datetime = args['start_date']
    end_date: datetime = args['end_date']
    dt_forecast = end_date - t0
    dt_prev = timedelta(args.get('lookback_days', dt_forecast.total_seconds() / 86400))
    mag_min: float | int = args.get('mag_min', 4.0)  # magnitude threshold for forecasting events
    dist: str = args.get('distribution', 'poisson')

    # Set seed for pseudo-random number gen
    if seed:
        numpy.random.seed(seed)

    # Filter catalog
    catalog_start = min([i[3] for i in input_catalog])
    cat_past = [i for i in input_catalog if i[3] < t0]
    cat_prev = [i for i in cat_past if i[3] >= t0 - dt_prev]

    # Predefine magnitude of completeness, Mc
    # Note: should not be too low/optimistic, otherwise incompleteness effects will prevail:
    #       - only for Poisson: biased rate estimation and biased scaling of `mu` to `mag_min`
    #       - sampling locations of very small events that may be too uncertain
    mag_compl = 2.0  # (a conservative Mc estimate for ISIDE)
    mag_compl = args.get('mag_compl', mag_compl)

    # Create complete catalog of past seismicity; used for:
    #  - only for Poisson: estimating BG seismicity parameter (mu)
    #  - sampling (locations of) background events for the catalog-based forecasts
    cat_past_compl = [i for i in cat_past if i[2] >= mag_compl]

    # Create a magnitude-thresholded catalog of recent seismicity; used for:
    #   - only for Poisson: estimating rate parameter of recent seismicity (lambda)
    #   - sampling (locations of) recent events for the catalog-based forecasts
    # If 'apply_mc_to_lookback' is True, this threshold will be the Mc level (mag_compl),
    # otherwise the forecast threshold (mag_min).
    mag_thresh_prev = mag_compl if args.get('apply_mc_to_lookback', False) else mag_min
    cat_prev_thresh = [i for i in cat_prev if i[2] >= mag_thresh_prev]

    if dist == 'poisson':

        # Background rate (normalized to forecast length)
        mu_compl = len(cat_past_compl) * dt_forecast.total_seconds() / (
            t0 - catalog_start).total_seconds()
        mu = mu_compl * 10**(mag_compl - mag_min)  # scale to mag_min using GR with b=1 (see above)

        # Previous time-window rate (normalized to forecast length)
        lambd = len(cat_prev_thresh) / dt_prev.total_seconds() * dt_forecast.total_seconds()
        lambd *= 10**(mag_thresh_prev - mag_min)  # scale to mag_min using GR with b=1 (see above)

    elif dist == 'negbinom':
        # Negative binomial distribution to model overdispersion (with a second parameter)
        # Important: must only use events above mag_min for estimating its parameters
        #      (because the variance/dispersion parameter cannot be simply adjusted to a
        #       different magnitude threshold)

        def calc_negbinom_params(mean, var):

            if mean == 0:  # (and therefore var == 0)
                return 1, 1  # to only sample zeros; value of tau is arbitrary

            alpha = (var - mean) / mean**2  # dispersion parameter

            if alpha == 0:  # (when var == mean)
                lim_tau = 1e6  # NBD converges converges to Poisson in the limit of r
                return lim_tau, lim_tau / (lim_tau + mean)  # will effectively resemble Poisson

            tau = 1 / alpha  # number of successes; > 0
            # theta = tau / (tau + mean)  # success probability; [0, 1]
            theta = mean / var  # equiv.

            return tau, theta

        # 1. Background component
        cat_past_minmag = [i for i in cat_past if i[2] >= mag_min]
        time_edges = numpy.arange(catalog_start.date(), t0.date() + dt_forecast, dt_forecast)
        counts, _ = numpy.histogram([i[3] for i in cat_past_minmag], time_edges)
        assert sum(counts) == len(cat_past_minmag)  # (FYI)

        mean_bg = numpy.mean(counts)  # equiv: len(cat_past_minmag) / len(timewindows[:-1])
        var_bg = numpy.var(counts)  # modeled as mean + mean**2/tau = mean + alpha*mean**2
        if var_bg < mean_bg:  # underdispersed
            # (NBD implicitely requires `var_bg` >= `mean_bg`: '==': Poisson; '>': overdispersed)
            var_bg = mean_bg  # make it (at least) Poissonian

        tau_bg, theta_bg = calc_negbinom_params(mean_bg, var_bg)

        # 2. 'Recent' (previous time-window) component
        cat_prev_minmag = [i for i in cat_prev if i[2] >= mag_min]
        mean = len(cat_prev_minmag) / dt_prev.total_seconds() * dt_forecast.total_seconds()
        # Use dispersion of BG for estimating variance from mean (leads to theta == theta_bg)
        dispersion_bg = var_bg / mean_bg if var_bg > 0 else 1.
        var = mean * dispersion_bg

        tau, theta = calc_negbinom_params(mean, var)

    else:
        raise RuntimeError(f"Distribution '{dist}' not implemented.")

    if verbose:
        print(
            f"Making forecast with model parameters:\n {args.__str__()}\n"
            f"and simulation parameters:\n"
            f" n_sims:{locals()['n_sims']}\n"
            f" seed:{locals()['seed']}")
        if dist == 'poisson':
            print(f"\tmu: {mu:.2e}\n\tlambda:{lambd:.2e}")
        elif dist == 'negbinom':
            print(f"\tmean_bg: {mean_bg:.2e}\tvar_bg:{var_bg:.2e}")
            print(f"\tmean: {mean:.2e}\tvar:{var:.2e}")

    # -- Simulating events
    # The model creates a random selection of N events from the input_catalog,
    # e.g., a simulated catalog has N_events ~ Poisson(rate_prevday)

    # Create Gutenberg-Richter (GR) distribution
    mag_bins = numpy.arange(mag_min, 8.1, 0.1)
    prob_mag = 10 ** (-mag_bins[:-1]) - 10 ** (-mag_bins[1:])  # GR with b=1
    prob_mag /= numpy.sum(prob_mag)

    forecast = []
    for n_cat in range(n_sims):
        if dist == 'poisson':
            n_events_bg = numpy.random.poisson(mu)
            n_events = numpy.random.poisson(lambd)

        elif dist == 'negbinom':
            n_events_bg = numpy.random.negative_binomial(tau_bg, theta_bg)
            n_events = numpy.random.negative_binomial(tau, theta)

        # Sample BG events
        idx_bg = numpy.random.choice(range(len(cat_past_compl)), size=n_events_bg)
        random_cat = [cat_past_compl[i] for i in idx_bg]

        # Sample from recent seismicity
        idx = numpy.random.choice(range(len(cat_prev_thresh)), size=n_events)
        random_cat.extend([cat_prev_thresh[i] for i in idx])

        for i, event in enumerate(random_cat):
            # Locations remain the same as in the randomly sampled catalog

            mag = numpy.random.choice(mag_bins[:-1], p=prob_mag)  # sample from GR
            t = t0 + numpy.random.random() * dt_forecast  # random datetime between t0 and end_date

            forecast.append([*event[0:2], mag, t, event[4], n_cat, i])

    # if verbose:
    print(
        f'\tTotal of {len(forecast)} events M>{mag_min} in {n_sims}'
        f' synthetic catalogs')
    return forecast


def run():
    """
    Advanced usage for command entry point (see setup.cfg, entry_points)
    """
    args = sys.argv
    main(*args[1:])
