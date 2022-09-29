import os
import sys
from mockup import model
from datetime import datetime, timedelta


def run(start_date=None, dt=1):

    # Create forecasts directory if does not exist
    os.makedirs('forecasts', exist_ok=True)
    # Reads input catalog
    catalog = model.load_cat(path='./input/iside')
    # Set up input parameters. In this case, only start date / end_date is needed
    if not start_date:
        params = model.read_params('parameters.txt')
    else:
        start_date = datetime.fromisoformat(start_date)
        params = {'start_date': start_date, 'end_date': start_date + timedelta(dt)}
    # Run model
    forecast = model.make_forecast(catalog, params, n_sims=10)
    # Write forecasts
    model.write_forecast(params['start_date'], forecast)


if __name__ == '__main__':


    # Reads arguments passed to this python file run.py.
    args = sys.argv
    if len(args) == 1:
        # This file was run as python run.py
        print('Running using parameter file')
    else:
        # This file was run as python run.py ${datetime}
        print('Running using input datetime')

    # Run the model, passing the unpacked arguments, if any.
    run(*args[1:])
    # Note if the modeler prefers to work with a parameter file, this can be just
    # run()
    # where the parameter file is read within.

