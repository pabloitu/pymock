"""
.. example_background_day

Simple simulation of a background day from a python script
===================

This example demonstrates an illustrative case to run the model for an unremarkable day.

Overview:
    1. Define model parameters in a python script
    2. Run model function passing the model parameters as arguments
    3. Read the synthetic catalogs and plot them
"""
import matplotlib.pyplot as plt
###############################################################################
# Load required modules
# -----------------------

import numpy
from datetime import datetime
from pymock.main import make_forecast
from pymock.libs import load_cat, syncat_path, write_forecast
from matplotlib import pyplot

###############################################################################
# Define forecast parameters
# ------------

catalog = load_cat('input/iside')
args = {
     'start_date': datetime(2011, 1, 1),
     'end_date': datetime(2011, 1, 2),
     'mag_min': 4.0,
}

###############################################################################
# Run simulations
# ---------------
forecast = make_forecast(catalog,
                         args,
                         n_sims=1000,
                         seed=2)

###############################################################################
# Store forecast
# --------------
write_forecast(start=args['start_date'],
               end=args['end_date'],
               forecast=forecast,
               folder='forecasts'
               )

###############################################################################
# Plot all forecast together with their ids in different color
# and magnitudes in different size.
# ------------------------------------------------------------


lon = [i[0] for i in forecast]
lat = [i[1] for i in forecast]
mag = [i[2] for i in forecast]
n_syncat = [i[5] for i in forecast]

region = numpy.genfromtxt('input/region')

pyplot.title('pyMock - synthetic catalogs 0-4')
pyplot.plot(region[:, 0], region[:, 1])
pyplot.scatter(lon, lat, s=numpy.array(mag) ** 3, c=n_syncat)
pyplot.xlabel('lon')
pyplot.ylabel('lat')
pyplot.tight_layout()
pyplot.savefig('forecasts/ex1_0-4')
pyplot.show()
