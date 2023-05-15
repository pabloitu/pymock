"""
.. example_intense_forecast

Simulation of the Amatrice sequence
===================

This example demonstrates an illustrative case to run the Amatrice sequence,
 which should have a large computational effort. Similar to example 2, but has
 a larger number of simulations and lower cutoff magnitude (a model sub-class)

Overview:
    1. Define the model arguments in a python script
    2. Creates the required start dates
    2. Run the model passing a random seed value (derived from the main seed)
    3. Read the synthetic catalogs and plot the daily average
"""

###############################################################################
# Load required modules
# -----------------------

import numpy
import os
import time
from datetime import datetime, timedelta

from pymock.main import make_forecast
from pymock.libs import load_cat, syncat_path, write_forecast
from matplotlib import pyplot

###############################################################################
# Define forecast parameters
# --------------------------
catalog = load_cat('input/iside')
start_date = datetime(2009, 3, 1)
n_days = 100
mag_min = 3.5
forecast_windows = [(start_date + timedelta(i),
                     start_date + timedelta(i + 1)) for i in range(n_days)]

n_sims = 1000
seed = 23
numpy.random.seed(seed)

###############################################################################
# Run simulations
# ------------
stime = time.perf_counter()
daily_forecasts = []

for start, end in forecast_windows:
    args = {
        'start_date': start,     # To be updated for every window
        'end_date': end,
        'mag_min': mag_min,
    }
    day = make_forecast(input_catalog=catalog,
                        args=args,
                        n_sims=n_sims,
                        # a different seed for each day, which is
                        # derived from the main seed (23).
                        seed=numpy.random.randint(1, 10000),
                        verbose=False)

    # Uncomment to store forecast
    write_forecast(start, end, day, './forecasts/')

    daily_forecasts.append(day)

print(f'Run-Time: {time.perf_counter() - stime:1f}')

############################################################################
# Load forecasted synthetic catalogs, get mean rate and plot them all together
# ----------------------------------------------------------------------------

cat = load_cat(os.path.join('input', 'iside'))
cat = [i for i in cat if i[2] >= mag_min]

cat_events = []
forecast_avg = []

for start, end in forecast_windows:
    syncat = load_cat(syncat_path(start, end, 'forecasts'))
    cat_ids = [i[5] for i in syncat]
    events_per_cat = numpy.unique(cat_ids, return_counts=True)[1]
    avg_events = numpy.sum(events_per_cat) / n_sims
    forecast_avg.append(avg_events)

    day_cat = [i for i in cat if i[3] >= start]
    day_cat = [i for i in day_cat if i[3] < end]
    cat_events.append(len(day_cat))

issued_dates = numpy.array([i[0] for i in forecast_windows])
fig = pyplot.figure(figsize=(8, 4))
pyplot.title("pyMock - L'Aquila sequence")
pyplot.plot(issued_dates, cat_events, label='Observed events')
pyplot.plot(issued_dates, forecast_avg, label='Mean simulated events')
pyplot.legend()
pyplot.xlabel('Date')
pyplot.ylabel('Daily rate')
pyplot.grid()
pyplot.tight_layout()
pyplot.savefig('forecasts/ex3_0-4')
pyplot.show()
