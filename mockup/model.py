from datetime import datetime, timedelta
import random
import numpy


def load_cat(path):
    catalog = []
    with open(path) as f_:
        for line in f_.readlines()[1:]:
            line = line.split(',')
            event = [float(line[0]), float(line[1]), float(line[2]), datetime.strptime(line[3], '%Y-%m-%dT%H:%M:%S.%f'),
                     float(line[4]), int(line[5]), line[6]]
            catalog.append(event)

    return numpy.array(catalog)


def read_params(path):
    params = {'start_date': None, 'end_date': None }
    with open(path) as f_:
        for line in f_.readlines():
            line_ = [i.strip() for i in line.split('=')]
            if line_[0] == 'forecastStartDate':
                params['start_date'] = datetime.strptime(line_[1], r'%Y/%m/%d %H:%M:%S')
            if line_[0] == 'forecastEndDate':
                params['end_date'] = datetime.strptime(line_[1], f'%Y/%m/%d %H:%M:%S')
    return params


def write_forecast(date, forecast):

    with open(f'./forecasts/mockup_{date.date().isoformat()}.txt', 'w') as file_:
        file_.write('lon, lat, M, time_string, depth, catalog_id, event_id\n')
        for i in range(len(forecast)):
            for syn_cat in forecast:
                for event in syn_cat:
                    line = f'{event[0]},{event[1]},{event[2]},{date.isoformat()},{event[4]},{i},\n'
                    file_.write(line)


def make_forecast(catalog, params, n_sims=1, seed=None):

    # set seed for pseudo-random number gen
    if seed:
        numpy.random.seed(seed)
    # filter catalog
    catalog = numpy.array([i for i in catalog if i[3] < params['end_date']])

    # Get rate from the previous time window. If mu == 0, a minimum of 1 is set
    mu = numpy.sum([i >= params['start_date'] for i in catalog[:, 3]]) or 1

    # The model creates a random selection of N events from the total input_catalog
    # A simulated catalog has N_events ~ Poisson(rate_prevday)
    forecast = []
    for i in range(n_sims):
        n_events = numpy.random.poisson(mu)
        syn_cat = numpy.array(random.sample(list(catalog), k=n_events))
        forecast.append(syn_cat)

    return forecast
