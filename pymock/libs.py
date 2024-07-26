from datetime import datetime, time
import os


def syncat_path(start, end, folder):
    """
    Returns the file path of a forecast based on its start and end dates.
    """

    variant = 'long'
    variant = 'short'  # hardcode

    if variant == 'short':
        return os.path.join(folder, f'pymock_{start.date().isoformat()}.csv')

    # Long version
    filename = f"pymock_{start.isoformat()}_{end.isoformat()}.csv"
    if os.name == 'nt':
        filename.replace(':', '.')  # on Windows, filenames cannot contain ':'
    return os.path.join(folder, filename)


def load_cat(path):
    """
    Loads a catalog forecast using the CSEP format

    Args:
        path (str): Path to the catalog file

    Returns:
        A list of CSEP formatted events in
            lon, lat, mag, time_str, depth, catalog_id, event_id
    """
    catalog = []
    with open(path) as f_:
        for line in f_.readlines()[1:]:
            line = line.split(',')
            event = [float(line[0]), float(line[1]), float(line[2]),
                     datetime.fromisoformat(line[3]),
                     float(line[4]), int(line[5]), int(line[6])]
            catalog.append(event)

    return catalog


def write_forecast(start, end, forecast, folder=None):
    """
    Writes a catalog forecast using the CSEP format  in
        lon, lat, mag, time_str, depth, catalog_id, event_id
    """

    if folder is None:
        folder = 'forecasts'
    os.makedirs(folder, exist_ok=True)
    with open(syncat_path(start, end, folder), 'w') as file_:
        file_.write('lon,lat,mag,time_string,depth,catalog_id,event_id\n')
        for event in forecast:
            line = f'{event[0]},{event[1]},{event[2]:.2f},' \
                   f'{event[3].isoformat()},{event[4]},{event[5]},{event[6]}\n'
            file_.write(line)


def read_args(path):
    """
    Parses an arguments file. This file should be build as:
    {argument} = {argument_value}
    """

    map_dict = {  # lists all supported params and their string -> type mapping
        "start_date": datetime.fromisoformat,
        "end_date": datetime.fromisoformat,
        "catalog": lambda x: os.path.join(os.path.dirname(path), x),
        "mag_min": float,
        "n_sims": int,
        "seed": int,
        "distribution": str,
        "lookback_days": int,
        "mag_compl": float,
        "apply_mc_to_lambda": bool
    }

    params = {}

    with open(path) as f_:
        for line in f_.readlines():
            line_ = [i.strip() for i in line.split('=')]
            if line_[0] not in map_dict:
                continue
            if len(line_) > 2:
                raise ValueError(f"Value of property '{line_[0]}' contains '=' character.")
            k, v = line_
            params[k] = map_dict.get(k, str)(v)

    return params
