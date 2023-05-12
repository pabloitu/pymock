"""
.. example_long_forecast

Simple simulation of daily forecast for one year
===================

This example demonstrates an ilustrative case to run the model sequentially.

Overview:
    1. Define the model parameters in a python script
    2. Creates multiple start dates
    2. Run the model passing a random seed value (derived from the main seed)
    3. Read the synthetic catalogs and plot the daily average
"""

####################################################################################################################################
# Load required modules
# -----------------------

import numpy
import time
from datetime import datetime, timedelta
from pymock.main import make_forecast
from pymock.libs import load_cat
from matplotlib import pyplot
####################################################################################################################################
# Define forecast parameters
# ------------
catalog = load_cat('input/iside')
start_date = datetime(2010, 1, 1)

ndays = 1000
forecast_windows = [(start_date + timedelta(i),
                     start_date + timedelta(i + 1)) for i in range(ndays)]


n_sims = 50
seed = 23

###############################################################################
# Run simulations
# ------------
stime = time.perf_counter()
daily_forecasts = []
for start, end in forecast_windows:
    args = {
            'start_date': start,     # To be updated for every window
            'end_date': end,
            'mag_min': 4.0,
                }
    day = make_forecast(catalog=catalog,
                        args=args,
                        n_sims=n_sims,
                        # a different seed for each day,
                        # derived from the main seed (23).
                        # seed=numpy.random.randint(1, 100),
                        verbose=False)

    daily_forecasts.append(day)
print(f'Time: {time.perf_counter() - stime:1f}')
#
# #############################################################################
# # Calculate the mean rate from synthetic catalogs and plot them all together
# # --------------------------------------------------------------------------
# # catalog = [i for i in catalog if i[2] >= args['mag_min']]
# # cat_events = []
# # forecast_avg = []
# #
# # for window, forecast in zip(forecast_windows, daily_forecasts):
# #
# #     cat_ids = [i[5] for i in forecast]
# #     events_per_cat = numpy.unique(cat_ids, return_counts=True)[1]
# #     avg_events = numpy.sum(events_per_cat) / n_sims
# #     forecast_avg.append(avg_events)
# #
# #     day_cat = [i for i in catalog if window[0] <= i[3] < window[1]]
# #     cat_events.append(len(day_cat))
# #
# # cat_events = numpy.array(cat_events)
# #
# # issued_dates = numpy.array([i[0] for i in forecast_windows])
# # pyplot.title('pyMock - Mean rate')
# # pyplot.plot(issued_dates, cat_events, label='Observed events')
# # pyplot.plot(issued_dates, forecast_avg, '--', label='Mean simulated events')
# # pyplot.plot(issued_dates[cat_events > 0], cat_events[cat_events > 0], 'o',
# #             color='steelblue')
# # pyplot.legend()
# # pyplot.xlabel('Date')
# # pyplot.ylabel('Daily rate')
# # pyplot.tight_layout()
# # pyplot.savefig('forecasts/ex2_0-4')
# # pyplot.show()
