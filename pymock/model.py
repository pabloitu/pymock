import os
import numpy
from datetime import datetime
from pymock.libs import syncat_path, load_cat


def make_forecast(catalog, params, n_sims=1, seed=None, verbose=True):
    start_date = params['start_date']
    end_date = params['end_date']
    dt = end_date - start_date
    mag_min = params.get('mag_min', 4.0)

    # set seed for pseudo-random number gen
    if seed:
        numpy.random.seed(seed)
    # filter catalog
    catalog = [i for i in catalog if i[3] < start_date]

    # Previous time window catalog
    catalog_prev = [i for i in catalog if i[3] >= (start_date - dt) and i[2] >= mag_min]

    # Previous window rate
    lambd = len(catalog_prev)
    # print('ltotal', lambda_total)
    # Background rate
    mu_total = len(catalog) * (end_date - start_date) / (
            max([i[3] for i in catalog]) - min([i[3] for i in catalog]))

    # scale by GR with b=1
    obsmag_min = min([i[2] for i in catalog])
    mu = mu_total * 10 ** (obsmag_min - mag_min)


    if verbose:
        print(f"Making pymock forecast with model parameters:\n {params.__str__()}\n"
              f"and simulation parameters:\n"
              f" n_sims:{locals()['n_sims']}\n"
              f" seed:{locals()['seed']}")
        print(f'\tmu: {mu:.2e}\n\tlambda:{lambd:.2e}')
    # The model creates a random selection of N events from the total input_catalog
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
            mag = numpy.random.choice(mag_bins[:-1], p=prob_mag / numpy.sum(prob_mag))
            event[2] = mag
            # For each event, assigns a random datetime between start and end date:
            dt = numpy.random.random() * (params['end_date'] - params['start_date'])
            event[3] = params['start_date'] + dt
            # Replace events and catalog ids
            event[5] = n_cat
            event[6] = i
            forecast.append(event)
    print(f'\tTotal of {len(forecast)} events M>{mag_min} in {n_sims} synthetic catalogs')
    return forecast
