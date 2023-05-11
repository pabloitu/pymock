import os
from pymock import main
from datetime import datetime

# Get test file path
current_dir = os.path.dirname(__file__)

# Get the path to write the test catalog
write_path = os.path.join(current_dir, 'artifacts')


def test_catwrite():
    date_forecast = datetime(2022, 10, 1)
    forecast = [
        [123.12, -74.52, 1.5, date_forecast, 10, 0, 0],  # event 0, syncat 0
        [-38.24, -73.05, 9.5, date_forecast, 33, 1, 0],  # event 0, syncat 1
        [60.908, -147.339, 9.2, date_forecast, 25, 1, 1]  # event 1, syncat 1
    ]

    model.write_forecast(date_forecast, forecast, folder=write_path)

    ## File exist
    forecast_name = os.path.join(write_path,
                                 f'pymock_{date_forecast.date().isoformat()}.txt')
    assert os.path.isfile(forecast_name)

    # Read raw data from written forecast
    with open(forecast_name, 'r') as file_:
        data = file_.readlines()

    # Event str
    event1st_str = '123.12,-74.52,1.5,2022-10-01T00:00:00,10,0,0\n'
    assert data[1] == event1st_str

    # Datetime
    date_event = data[2].split(',')[3]
    assert datetime.fromisoformat(date_event) == forecast[1][3]


if __name__ == '__main__':
    test_catwrite()
