import os
import sys
from mockup import model
from datetime import datetime, timedelta


def run_model(start_date=None, dt=1, mag_min=4.0, nsims=10, seed=None, folder=None):
    """
    Main run function
    Wraps the main steps of creating a forecast for a given time window.
    1.- Reads a catalog
    2.- Gets the parameters (e.g. forecast dates)
    3.- Creates the forecast as synthetic catalogs
    4.- Writes the synthetic catalogs

    params:
        start_date (str): Start of the forecast. If None, tries to read from parameters.txt
        dt (int):  time interval of the forecast, in days
        mag_min (float): Forecast minimum magnitude
        nsims (int): Number of synthetic catalogs
        seed (int): pseudo_random number seed
        folder (str): where to save forecasts. Defaults to current path
    """

    # Create forecasts folder in current directory if it does not exist.
    os.makedirs(folder or 'forecasts', exist_ok=True)

    # 1. Reads input catalog
    cat_path = os.path.join(os.path.dirname(__file__), 'input', 'iside')
    catalog = model.load_cat(path=cat_path)

    # 2. Set up input parameters. In this case, only start date / end_date is needed
    if not start_date:
        params = model.read_params('parameters.txt')
    else:
        start_date = datetime.fromisoformat(start_date)
        params = {'start_date': start_date,
                  'end_date': start_date + timedelta(dt),
                  'mag_min': mag_min}

    # 3. Run model
    forecast = model.make_forecast(catalog, params, n_sims=nsims, seed=seed)

    # 4. Write forecasts
    model.write_forecast(params['start_date'], forecast, folder)


if __name__ == '__main__':

    # Reads arguments passed to this python file run.py.
    args = sys.argv
    if len(args) == 1:
        # This file was run as `python run.py`
        print('Running using parameter file')
    elif len(args) > 1:
        # This file was run as `python run.py ${datetime}`
        print('Running using input datetime')

    # Run the model, passing the unpacked arguments, if any.
    run_model(*args[1:])
