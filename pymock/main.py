import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import numpy
import pymock

from pymock import libs


def default_args_path():
    return Path(pymock.__file__).parent.parent / 'input' / 'args.txt'


def default_forecast_folder():
    return Path(pymock.__file__).parent.parent / 'forecasts'


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

    if arg_path is None:
        arg_path = default_args_path()

    # Create a forecasts folder in current directory if it does not exist.
    if folder is None:
        folder = default_forecast_folder()
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
    mag_min: float | int = args.get('mag_min', 4.0)
    dist: str = args.get('distribution', 'poisson')

    # Predefine magnitude of completeness, Mc;
    # will be used with b-value = 1 to scale BG activity from M >= Mc to M >= mag_min
    #   (same optionally also for recent activity if 'apply_mc_to_lambda' is True)
    # Note: should not be too low/optimistic, otherwise this adjustment is flawed
    #       (due to incompleteness)
    mag_compl = 2.0  # (a conservative Mc estimate for ISIDE)
    mag_compl = args.get('mag_compl', mag_compl)

    # Set seed for pseudo-random number gen
    if seed:
        numpy.random.seed(seed)

    # Filter catalog
    cat_total = [i for i in input_catalog if i[3] < t0 and
                 i[2] >= mag_compl]  # only above completeness lvl (for reasons mentioned above)
    mag_thresh_prev = mag_compl if args.get('apply_mc_to_lambda', False) else mag_min  # (see above)
    catalog_prev = [i for i in cat_total if t0 - dt_prev <= i[3] and
                    i[2] >= mag_thresh_prev]

    # Previous time-window rate (normalized to forecast length)
    lambd = len(catalog_prev) / dt_prev.total_seconds() * dt_forecast.total_seconds()
    lambd *= 10 ** (mag_thresh_prev - mag_min)  # correct to mag_min using b-value of 1 (see above)

    # Background rate (normalized to forecast length)
    mu_total = len(cat_total) * dt_forecast.total_seconds() / (
        t0 - min([i[3] for i in cat_total])).total_seconds()

    mu = mu_total * 10 ** (mag_compl - mag_min)  # scale by GR with b=1

    if dist == 'negbinom':
        cat_total_mag = [j for j in cat_total if j[2] >= mag_min]
        times = [i[3] for i in cat_total_mag]
        timewindows = numpy.arange(min(times).date(), max(times).date(), dt_forecast)
        counts, _ = numpy.histogram(times, timewindows)
        var = numpy.var(counts)
        alpha = (var - mu) / mu ** 2
        tau_bg = 1. / alpha * mu
        theta_bg = tau_bg / (tau_bg + mu)

        if lambd != 0:
            tau = 1. / alpha * lambd
            theta = tau / (tau + lambd)

    if verbose:
        print(
            f"Making forecast with model parameters:\n {args.__str__()}\n"
            f"and simulation parameters:\n"
            f" n_sims:{locals()['n_sims']}\n"
            f" seed:{locals()['seed']}")
        print(f'\tmu: {mu:.2e}\n\tlambda:{lambd:.2e}')

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
            if lambd != 0:
                n_events = numpy.random.negative_binomial(tau, theta)
            else:
                n_events = 0

        # Sample BG events
        idx_bg = numpy.random.choice(range(len(cat_total)), size=n_events_bg)
        random_cat = [cat_total[i] for i in idx_bg]

        # Sample from recent seismicity
        idx = numpy.random.choice(range(len(catalog_prev)), size=n_events)
        random_cat.extend([catalog_prev[i] for i in idx])

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
