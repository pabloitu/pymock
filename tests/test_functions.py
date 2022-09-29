import os
from datetime import datetime
from mockup import model

param_file = os.path.join(os.path.dirname(__file__), 'artifacts', 'parameters_test.txt')
cat_file = os.path.join(os.path.dirname(__file__), 'artifacts', 'iside_tests')


def test_params_reader():
    params = model.read_params(param_file)

    assert params['start_date'] == datetime(2016, 11, 5, 3, 22, 31)
    assert params['end_date'] == datetime(2016, 11, 6, 3, 22, 30)


def test_make_forecast():
    catalog = model.load_cat(cat_file)
    params = model.read_params(param_file)
    n_sims = 100
    seed = 23
    forecast = model.make_forecast(catalog, params, n_sims, seed)

    # Check total number of events
    assert len(forecast) == 192

    # Check a single event
    assert forecast[124] == [13.204,
                             42.956,
                             5.1,
                             datetime(2016, 11, 5, 13, 5, 18, 711269),
                             7.8,
                             65,
                             1]


if __name__ == '__main__':
    test_params_reader()
    test_make_forecast()
