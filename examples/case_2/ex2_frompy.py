"""
.. example_long_forecast

Simple simulation of daily forecast for one year
================================================

This example demonstrates an illustrative case to run the model sequentially.

Overview:
    1. Define the model arguments in a python script
    2. Creates multiple start dates
    2. Run the model passing a random seed value (derived from the main seed)
    3. Get the mean rate from synthetic catalogs and plot against events
"""

###############################################################################
# Load required modules
# -----------------------

import numpy
import time
from datetime import datetime, timedelta
from pymock.main import make_forecast
from pymock.libs import load_cat, write_forecast
from matplotlib import pyplot
###############################################################################
# Define forecast parameters
# --------------------------
catalog = load_cat('input/iside')
start_date = datetime(2010, 1, 1)

n_days = 365
forecast_windows = [(start_date + timedelta(i),
                     start_date + timedelta(i + 1)) for i in range(n_days)]

n_sims = 100
seed = 23
numpy.random.seed(seed)

###############################################################################
# Run simulations
# ---------------
stime = time.perf_counter()
daily_forecasts = []

for start, end in forecast_windows:
    args = {
            'start_date': start,     # To be updated for every window
            'end_date': end,
            'mag_min': 4.0,
                }
    day = make_forecast(input_catalog=catalog,
                        args=args,
                        n_sims=n_sims,
                        # a different seed for each day, which is
                        # derived from the main seed (23).
                        seed=numpy.random.randint(1, 10000),
                        verbose=False)

    # Uncomment to store forecast
    # write_forecast(start, end, day, './forecasts/')

    daily_forecasts.append(day)

print(f'Run-Time: {time.perf_counter() - stime:1f}')

#############################################################################
# Calculate the mean rate from synthetic catalogs and plot them all together
# --------------------------------------------------------------------------
catalog = [i for i in catalog if i[2] >= args['mag_min']]
cat_events = []
forecast_avg = []



for window, forecast in zip(forecast_windows, daily_forecasts):

    # Get forecast mean rates
    cat_ids = [i[5] for i in forecast]
    events_per_cat = numpy.unique(cat_ids, return_counts=True)[1]
    avg_events = numpy.sum(events_per_cat) / n_sims
    forecast_avg.append(avg_events)

    # Get observed events
    day_cat = [i for i in catalog if window[0] <= i[3] < window[1]]
    cat_events.append(len(day_cat))

cat_events = numpy.array(cat_events)
issued_dates = numpy.array([i[0] for i in forecast_windows])


# Plot
pyplot.title('pyMock - Mean rate')
pyplot.plot(issued_dates, cat_events, label='Observed events')
pyplot.plot(issued_dates, forecast_avg, '--', label='Mean simulated events')
pyplot.plot(issued_dates[cat_events > 0], cat_events[cat_events > 0], 'o',
            color='steelblue')
pyplot.legend()
pyplot.xlabel('Date')
pyplot.ylabel('Daily rate')
pyplot.tight_layout()
pyplot.savefig('forecasts/ex2_0-4')
pyplot.show()
