import os
import unittest
from pymock import libs
from datetime import datetime

# Get test file path
current_dir = os.path.dirname(__file__)

# Get the path to write the test catalog
write_path = os.path.join(current_dir, 'artifacts')


class TestMain(unittest.TestCase):

    def test_catwrite(self):
        start = datetime(2022, 10, 1)
        end = datetime(2022, 10, 2)
        forecast = [
            [123.12, -74.52, 1.5, start, 10, 0, 0],  # event 0, syncat 0
            [-38.24, -73.05, 9.5, start, 33, 1, 0],  # event 0, syncat 1
            [60.908, -147.339, 9.2, start, 25, 1, 1]  # event 1, syncat 1
        ]

        libs.write_forecast(start, end, forecast, folder=write_path)

        # File exist
        time_str = f'{start.date().isoformat()}_{end.date().isoformat()}'
        fpath = os.path.join(write_path, f'pymock_{time_str}.csv')
        assert os.path.isfile(fpath)

        # Read raw data from written forecast
        with open(fpath, 'r') as file_:
            data = file_.readlines()

        # Event str
        event1st_str = '123.12,-74.52,1.50,2022-10-01T00:00:00,10,0,0\n'
        assert data[1] == event1st_str

        # Datetime
        date_event = data[2].split(',')[3]
        assert datetime.fromisoformat(date_event) == forecast[1][3]


if __name__ == '__main__':
    TestMain().test_catwrite()
