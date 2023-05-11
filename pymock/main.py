import os
import sys
import numpy
from pymock import libs


def main(argpath=None, nsims=10, seed=None, folder=None, verbose=True):
    """
    Main pymock's function
    Wraps the main steps of creating a forecast for a given time window.
    1. Parse an argument file
    2. Reads the input catalog
    3. Creates the forecast as synthetic catalogs
    4. Writes the synthetic catalogs

    params:
        argpath (str): Path to the input arguments file.
        nsims (int): Number of synthetic catalogs
        seed (int): pseudo_random number seed
        folder (str): where to save forecasts. Defaults to 'forecasts'
        verbose (bool): print log
    """

    # Create forecasts folder in current directory if it does not exist.
    os.makedirs(folder or 'forecasts', exist_ok=True)

    # 1. Gets input data and arguments.
    args = libs.read_args(argpath)  # A dict containing parameters

    cat_path = args.get('catalog')
    nsims = args.get('nsims', nsims)
    seed = args.get('seed', seed)

    # 2. Reads input catalog
    catalog = libs.load_cat(path=cat_path)

    # 3. Run model
    forecast = make_forecast(catalog, args,
                             n_sims=nsims,
                             seed=seed,
                             verbose=verbose)

    # 4. Write forecasts
    libs.write_forecast(args['start_date'], args['end_date'], forecast, folder)


def make_forecast(catalog, args, n_sims=1, seed=None, verbose=True):
    start_date = args['start_date']
    end_date = args['end_date']
    dt = end_date - start_date
    mag_min = args.get('mag_min', 4.0)

    # set seed for pseudo-random number gen
    if seed:
        numpy.random.seed(seed)
    # filter catalog
    catalog = [i for i in catalog if i[3] < start_date]

    # Previous time window catalog
    catalog_prev = [i for i in catalog if
                    i[3] >= (start_date - dt) and i[2] >= mag_min]

    # Previous time-window rate
    lambd = len(catalog_prev)
    # Background rate
    mu_total = len(catalog) * (end_date - start_date) / (
            max([i[3] for i in catalog]) - min([i[3] for i in catalog]))

    # scale by GR with b=1
    obsmag_min = min([i[2] for i in catalog])
    mu = mu_total * 10 ** (obsmag_min - mag_min)

    if verbose:
        print(
            f"Making forecast with model parameters:\n {args.__str__()}\n"
            f"and simulation parameters:\n"
            f" n_sims:{locals()['n_sims']}\n"
            f" seed:{locals()['seed']}")
        print(f'\tmu: {mu:.2e}\n\tlambda:{lambd:.2e}')

    # The model creates a random selection of N events from the input_catalog
    # A simulated catalog has N_events ~ Poisson(rate_prevday)
    forecast = []
    for n_cat in range(n_sims):
        n_events_bg = numpy.random.poisson(mu)
        idx_bg = numpy.random.choice(range(len(catalog)), size=n_events_bg)

        n_events = numpy.random.poisson(lambd)
        idx = numpy.random.choice(range(len(catalog_prev)), size=n_events)

        random_cat = [catalog[i] for i in idx_bg]
        random_cat.extend([catalog_prev[i] for i in idx])

        for i, event in enumerate(random_cat):
            # Positions remains the same as the random catalog
            # Get the magnitude value using GR with b=1
            mag_bins = numpy.arange(mag_min, 8.1, 0.1)
            prob_mag = 10 ** (-mag_bins[:-1]) - 10 ** (-mag_bins[1:])
            mag = numpy.random.choice(mag_bins[:-1],
                                      p=prob_mag / numpy.sum(prob_mag))
            event[2] = mag
            # For each event, assigns a random datetime between start and end:
            dt = numpy.random.random() * (
                    args['end_date'] - args['start_date'])
            event[3] = args['start_date'] + dt
            # Replace events and catalog ids
            event[5] = n_cat
            event[6] = i
            forecast.append(event)
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
