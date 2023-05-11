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
####################################################################################################################################
# Load required modules
# -----------------------

import numpy
from datetime import datetime
from run import run_model
from pymock.model import load_cat, syncat_path
from matplotlib import pyplot

####################################################################################################################################
# Define forecast parameters
# ------------

forecast_date = datetime(2011, 1, 1)  # daily rate ~1/5 of input catalog mean rate
dt = 1  # one-day forecast
mag_min = 4.0  # cut-off magnitude of the given forecasts
nsims = 1000
seed = 2

####################################################################################################################################
# Run simulations
# ------------
run_model(forecast_date.isoformat(),
          dt=dt,
          mag_min=mag_min,
          nsims=nsims,
          seed=seed)

####################################################################################################################################
# Load forecasted synthetic catalogs and plot them all together
# ------------

syncat = load_cat(syncat_path(forecast_date, 'forecasts'))
lon = [i[0] for i in syncat]
lat = [i[1] for i in syncat]
mag = [i[2] for i in syncat]
n_syncat = [i[5] for i in syncat]

region = numpy.genfromtxt('input/region')

pyplot.title('pyMock - synthetic catalogs 0-4')
pyplot.plot(region[:,0], region[:, 1])
pyplot.scatter(lon, lat, s=numpy.array(mag) ** 3, c=n_syncat)
pyplot.xlabel('lon')
pyplot.ylabel('lat')
pyplot.tight_layout()
pyplot.savefig('forecasts/ex1_0-4')
pyplot.show()
