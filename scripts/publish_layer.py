import sys
from geoserver.catalog import Catalog

GEOSERVER_API = "http://localhost:8080/geoserver/rest"
GEOSERVER_USER = "admin"
GEOSERVER_PASS = "geoserver"

cat = Catalog(GEOSERVER_API, GEOSERVER_USER, GEOSERVER_PASS)

_file = sys.argv[1]

cat.create_coveragestore(_file, _file)