from datetime import datetime, timedelta, time
import random

input_catalog = '../input/iside'
parameters_file = '../parameters.txt'

def load_cat(path=input_catalog):
    with open(path) as f_:
        catalog = [line.split(',') for line in f_.readlines()[1:]]
    return catalog

def read_params(path=parameters_file):
    params = {'start_date': None, 'end_date': None }
    with open(path) as f_:
        for line in f_.readlines():
            line_ = [i.strip() for i in line.split('=')]
            if line_[0] == 'forecastStartDate':
                params['start_date'] = line_[1]
            if line_[0] == 'forecastEndDate':
                params['end_date'] = line_[1]

    return params

def write_forecast(date, forecast):

    date = date[:10].replace('/', '-')
    print(date)
    with open(f'../forecasts/mockup_{date}.txt', 'w') as file_:
        file_.write('lon,lat,M,time_string,depth,catalog_id, event_id\n')
        for i in range(len(forecast)):
            for syn_cat in forecast:
                for event in syn_cat:
                    line = f'{event[0]},{event[1]},{event[2]},{date},{event[4]},{i},\n'
                    print(line)
                    file_.write(line)

def make_forecast(n_sims=1):

    catalog = load_cat(input_catalog)
    times = [datetime.strptime(i[3][:-3], "%Y-%m-%dT%H:%M:%S") for i in catalog]
    n_days = (max(times) - min(times)).days
    forecast = []
    for i in range(n_sims):
        random_date = datetime.combine(min(times).date(), time(0, 0, 0)) + timedelta(days=random.randrange(n_days))
        idx = [i for i, boo in enumerate([random_date < i <= random_date + timedelta(days=1) for i in times]) if boo]
        forecast.append([catalog[i] for i in idx])

    return forecast


if __name__== '__main__':
    params = read_params()
    forecast = make_forecast(n_sims=10)
    write_forecast(params['start_date'], forecast)
    # write_forecast(datetime.today(), forecast)