"""
.. example_intense_forecast

Simulation of the Amatrice sequence
===================

This example demonstrates an ilustrative case to run the Amatrice sequence, which should have a large computational effort.
Similar to example 2, but has a larger number of simulations and lower cutoff magnitude.

Overview:
    1. Define the model parameters in a python script
    2. Creates the required start dates
    2. Run the model passing a random seed value (derived from the main seed)
    3. Read the synthetic catalogs and plot the daily average
"""
import time

####################################################################################################################################
# Load required modules
# -----------------------

import numpy
import os
import time
from datetime import datetime, timedelta
from run import run_model
from pymock.model import load_cat, syncat_path
from matplotlib import pyplot

####################################################################################################################################
# Define forecast parameters
# ------------
start_date = datetime(2016, 9, 4)
ndays = 100
forecast_dates = [start_date + timedelta(i) for i in range(ndays)]
dt = 1  # one-day forecasts
mag_min = 3.0  # cut-off magnitude of the given forecasts
nsims = 10
seed = 23

####################################################################################################################################
# Run simulations
# ------------

stime = time.perf_counter()
for date in forecast_dates:
    run_model(date.isoformat(),
              dt=dt,
              mag_min=mag_min,
              nsims=nsims,
              seed=numpy.random.randint(1, 100),  # a different seed for each day, derived from the main seed (23).
              verbose=False)
print(f'Time: {time.perf_counter() - stime:1f}')
####################################################################################################################################
# Load forecasted synthetic catalogs, calculate the mean rate and plot them all together
# ------------

cat = load_cat(os.path.join('input', 'iside'))
cat = [i for i in cat if i[2] >= mag_min]

cat_events = []
forecast_avg = []

for date in forecast_dates:
    syncat = load_cat(syncat_path(date, 'forecasts'))
    cat_ids = [i[5] for i in syncat]
    events_per_cat = numpy.unique(cat_ids, return_counts=True)[1]
    avg_events = numpy.sum(events_per_cat) / nsims
    forecast_avg.append(avg_events)

    day_cat = [i for i in cat if i[3] >= date]
    day_cat = [i for i in day_cat if i[3] < (date + timedelta(dt))]
    cat_events.append(len(day_cat))

pyplot.semilogy(range(ndays), cat_events, label='Observed events')
pyplot.semilogy(range(ndays), forecast_avg, label='Mean simulated events')
pyplot.show()
