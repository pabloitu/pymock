import os
import unittest
import numpy
from datetime import datetime
from pymock import main, libs
arg_file = os.path.join(os.path.dirname(__file__), 'artifacts',
                        'args_test.txt')
cat_file = os.path.join(os.path.dirname(__file__), 'artifacts', 'iside_tests')


class TestMain(unittest.TestCase):

    def test_params_reader(self):
        args = libs.read_args(arg_file)
        assert args['start_date'] == datetime(2016, 11, 5, 3, 22, 31)
        assert args['end_date'] == datetime(2016, 11, 6, 3, 22, 30)

    def test_make_forecast(self):
        catalog = libs.load_cat(cat_file)
        params = libs.read_args(arg_file)
        n_sims = 100
        seed = 24
        forecast = main.make_forecast(catalog, params, n_sims, seed)
        # Check total number of events
        assert len(forecast) == 10

        numpy.testing.assert_almost_equal(forecast[9][0], 13.297)
        numpy.testing.assert_almost_equal(forecast[9][1], 42.82)
        numpy.testing.assert_almost_equal(forecast[9][2], 4.4)
        numpy.testing.assert_equal(forecast[9][3], datetime(2016, 11, 5, 19, 0, 56,759566))
        numpy.testing.assert_almost_equal(forecast[9][4], 10.0)
        numpy.testing.assert_almost_equal(forecast[9][5], 97)
        numpy.testing.assert_almost_equal(forecast[9][6], 1)


if __name__ == '__main__':
    testobj = TestMain()
    testobj.test_params_reader()
    testobj.test_make_forecast()
