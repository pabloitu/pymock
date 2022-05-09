import os
import mockup.model as model

os.makedirs('forecasts', exist_ok=True)

params = model.read_params(path='./parameters.txt')
catalog = model.load_cat(path='./input/iside')
forecast = model.make_forecast(catalog, params, n_sims=10)
model.write_forecast(params['start_date'], forecast)

