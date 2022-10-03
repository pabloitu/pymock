"""
.. example_background_day

Simple simulation of a background day
===================

This example demonstrates an ilustrative case to run the model in an unremarkable day.

Overview:
    1. Load catalog
    2. Create filtering parameters in space, magnitude, and time
    3. Filter catalog using desired filters
    4. Write catalog to standard CSEP format
"""

####################################################################################################################################
# Load required libraries
# -----------------------
#
# Most of the core functionality can be imported from the top-level :mod:`csep` package. Utilities are available from the
# :mod:`csep.utils` subpackage.

from datetime import datetime
from run import run_model

####################################################################################################################################
# Load catalog
# ------------
#
# PyCSEP provides access to th;``e ComCat web API using :func:`csep.query_comcat` and to the Bollettino Sismico Italiano
# API using :func:`csep.query_bsi`. These functions require a :class:`datetime.datetime` to specify the start and end
# dates.

start_date = datetime(2011, 1, 1).isoformat()
run_model(start_date, nsims=1000)
