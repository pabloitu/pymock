import os
from datetime import datetime
from pymock import main, libs

arg_file = os.path.join(os.path.dirname(__file__), 'artifacts',
                        'args_test.txt')
cat_file = os.path.join(os.path.dirname(__file__), 'artifacts', 'iside_tests')


def test_params_reader():
    args = libs.read_args(arg_file)
    assert args['start_date'] == datetime(2016, 11, 5, 3, 22, 31)
    assert args['end_date'] == datetime(2016, 11, 6, 3, 22, 30)


def test_make_forecast():
    catalog = libs.load_cat(cat_file)
    params = libs.read_args(arg_file)
    n_sims = 100
    seed = 24
    forecast = main.make_forecast(catalog, params, n_sims, seed)
    # Check total number of events
    assert len(forecast) == 11

    # Check a single event
    assert forecast[10] == [13.382,
                            37.701,
                            4.1,
                            datetime(2016, 11, 5, 19, 0, 4, 641429),
                            5.0,
                            81,
                            0]


if __name__ == '__main__':
    test_params_reader()
    test_make_forecast()
