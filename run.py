import os
import sys
from pymock import model
from pymock import libs
from datetime import datetime, timedelta


def run_model(start_date=None, dt=1, mag_min=4.0, nsims=10,
              seed=None, folder=None, verbose=True):
    """
    Main run function
    Wraps the main steps of creating a forecast for a given time window.
    1.- Reads a catalog
    2.- Gets the parameters (e.g. forecast dates)
    3.- Creates the forecast as synthetic catalogs
    4.- Writes the synthetic catalogs

    params:
        start_date (str): Start of the forecast. If None, tries to read from parameters.txt
        dt (float/str):  time interval of the forecast, in days
        mag_min (float): Forecast minimum magnitude
        nsims (int): Number of synthetic catalogs
        seed (int): pseudo_random number seed
        folder (str): where to save forecasts. Defaults to current path
        verbose (bool): print log
    """

    # Create forecasts folder in current directory if it does not exist.
    os.makedirs(folder or 'forecasts', exist_ok=True)

    # 1. Reads input catalog. Defaults to a catalog with path in ${currentpath}/input/iside
    #  * Can be added as extra argument
    cat_path = os.path.join('input', 'iside')
    catalog = libs.load_cat(path=cat_path)

    # 2. Set up input and model parameters.
    if not start_date:
        # If no start_date is passed, model tries to read from a parameters.txt file found in the directory
        params = libs.read_params('parameters.txt')  # A dict containing start_date, end_date and mag_min
        nsims = params.get('nsims', nsims)  # Check if nsims and seed are in parameters.txt. If not, uses defaults
        seed = params.get('seed', seed)
    else:
        start_date = datetime.fromisoformat(start_date)
        # Creates a params dictionary using the parameters passed
        params = {'start_date': start_date,
                  'end_date': start_date + timedelta(float(dt)),
                  'mag_min': float(mag_min)}

    # 3. Run model
    forecast = model.make_forecast(catalog, params, n_sims=int(nsims),
                                   seed=int(seed) if seed else seed,  # pass int(seed) if seed is not None
                                   verbose=verbose)

    # 4. Write forecasts
    libs.write_forecast(params['start_date'], forecast, folder)


def run():
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


if __name__ == '__main__':
    run()
