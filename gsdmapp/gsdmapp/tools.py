#!/usr/bin/env python
#
#
# Created on 2/7/2018 Allan Oware - CIAT
#
# Requirements:
#	arcpy
#
# Global Soil Data Manager Toolbox
# Tested on ArcGIS 10.5
#


import os, sys
import math
import fnmatch
import fiona
import json
from datetime import datetime


def createShp(poly):
	#create shapefile from user geojson
    os.chdir('/tmp/gsdm')

    schema = {'geometry': 'Polygon','properties': {'fld_a': 'str:50'}}

    with fiona.open('polygon.shp', 'w', 'ESRI Shapefile', schema) as layer:
		layer.write({'geometry': json.loads(poly), 'properties': {'fld_a': 'test'}}) 


    shpfile = 'polygon.shp'

    return shpfile