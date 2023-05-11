from datetime import datetime
import numpy
import os


def syncat_path(date, folder):
    if isinstance(date, str):
        date = datetime.fromisoformat(date)
    return os.path.join(folder, f'pymock_{date.date().isoformat()}.txt')


def load_cat(path):
    catalog = []
    with open(path) as f_:
        for line in f_.readlines()[1:]:
            line = line.split(',')
            event = [float(line[0]), float(line[1]), float(line[2]), datetime.strptime(line[3], '%Y-%m-%dT%H:%M:%S.%f'),
                     float(line[4]), int(line[5]), int(line[6])]
            catalog.append(event)

    return catalog


def write_forecast(date, forecast, folder=None):
    if folder is None:
        folder = 'forecasts'
    with open(syncat_path(date, folder), 'w') as file_:
        file_.write('lon, lat, M, time_string, depth, catalog_id, event_id\n')
        for event in forecast:
            line = f'{event[0]},{event[1]},{event[2]:.2f},{event[3].isoformat()},{event[4]},{event[5]},{event[6]}\n'
            file_.write(line)


def read_params(path):
    params = {'start_date': None, 'end_date': None}
    with open(path) as f_:
        for line in f_.readlines():
            line_ = [i.strip() for i in line.split('=')]
            if line_[0] == 'start_date':
                params['start_date'] = datetime.strptime(line_[1], r'%Y/%m/%d %H:%M:%S')
            elif line_[0] == 'end_date':
                params['end_date'] = datetime.strptime(line_[1], f'%Y/%m/%d %H:%M:%S')
            elif line_[0] == 'mag_min':
                params['mag_min'] = float(line_[1])
            elif line_[0] == 'nsims':
                params['nsims'] = float(line_[1])
            elif line_[0] == 'seed':
                params['seed'] = float(line_[1])

    return params
