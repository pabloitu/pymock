"""
.. example_background_day

Simple simulation of a background day from a python script
==========================================================

This example demonstrates an illustrative case to run the model for an unremarkable day.

Overview:
    1. Define model parameters in a python script
    2. Run model function passing the model parameters as arguments
    3. Read the synthetic catalogs and plot them
"""

###############################################################################
# Load required modules
# -----------------------

import numpy
from datetime import datetime
from pymock.main import make_forecast
from pymock.libs import load_cat, write_forecast
from matplotlib import pyplot

###############################################################################
# Define forecast parameters
# --------------------------

catalog = load_cat('input/iside')
args = {
    'start_date': datetime(2011, 1, 1),
    'end_date': datetime(2011, 1, 2),
    'mag_min': 4.0,
}

###############################################################################
# Run simulations
# ---------------
nsims = 1000
forecast = make_forecast(catalog,
                         args,
                         n_sims=nsims,
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
mag = numpy.array(mag)
n_syncat = [i[5] for i in forecast]

region = numpy.genfromtxt('input/region')


pyplot.title('pyMock - synthetic catalogs')
pyplot.plot(region[:, 0], region[:, 1], ls='--', c='0.3')
# pyplot.scatter(lon, lat, s=numpy.array(mag) ** 3, c=n_syncat)
pyplot.scatter(lon, lat, s=12 + 10**(mag - mag.min() + 0.5),
               c=n_syncat, alpha=0.5, ec='none')  # [mh mod]
pyplot.gca().set_aspect('equal', adjustable='box')  # (only approximate)
cbar = pyplot.colorbar()
cbar.ax.set_ylabel('Catalog N°')
pyplot.xlabel('lon')
pyplot.ylabel('lat')
pyplot.tight_layout()
pyplot.savefig('forecasts/ex1_0-4.png')
pyplot.show()
