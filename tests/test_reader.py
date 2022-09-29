import numpy
import os
from mockup import model
from datetime import datetime

# Get test file path
current_dir = os.path.abspath(__file__)

# Here we get the path from the catalog that the modeler provides as artifact
catalog_path = os.path.join(current_dir, 'artifacts', 'iside_tests')


def test_catread():
    # Reads the artifact catalog
    catalog = model.load_cat(catalog_path)

    # Test number of events in catalog
    assert len(catalog) == 35499

    # Test max mag (uses numpy to test floating points)
    assert numpy.isclose(numpy.max(catalog[:, 2]), 6.2)

    # Test an individual event
    # lat, lon, mag, datetime, depth, cat_id, event_id
    # 14.02,38.592,2.2,2008-06-22T23:43:42.78,10.0,-1,1827439
    assert numpy.isclose(catalog[3211][0], 14.02)
    assert numpy.isclose(catalog[3211][1], 38.592)
    assert numpy.isclose(catalog[3211][2], 2.2)
    assert catalog[3211][3] == datetime(2008, 6, 22, 23, 43, 42, 780000)
    assert numpy.isclose(catalog[3211][4], 10.0)
    assert catalog[3211][5] == -1
    assert catalog[3211][6] == 1827439


if __name__ == '__main__':
    test_catread()
