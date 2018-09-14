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
from fiona.crs import from_epsg
from osgeo import ogr, osr, gdal



def createShp(poly):
	#create shapefile from user geojson
    os.chdir('/tmp/gsdm')

    schema = {'geometry': 'Polygon','properties': {'fld_a': 'str:50'}}

    shpfile = 'polygon.shp'

    #_crs = from_epsg(3857)

    with fiona.open(shpfile, 'w', 'ESRI Shapefile', schema) as layer:
		layer.write({'geometry': poly, 'properties': {'fld_a': 'test'}}) 

    reprojected = reProject(shpfile)


    return reprojected


def reProject(shapefile):
	# reproject to planar coordinate system: 3857
	# tif with target projection
	tif = gdal.Open("/tmp/gsdm/soc_reproj21.tif")

	# shapefile with source projection
	driver = ogr.GetDriverByName("ESRI Shapefile")
	datasource = driver.Open("/tmp/gsdm/polygon.shp") 
	layer = datasource.GetLayer()

	# set spatial reference and transformation
	sourceprj = layer.GetSpatialRef()
	targetprj = osr.SpatialReference(wkt = tif.GetProjection())
	transform = osr.CoordinateTransformation(sourceprj, targetprj)

	reprojected_shp = 'polygon_reproj.shp'

	to_fill = ogr.GetDriverByName("Esri Shapefile")
	ds = to_fill.CreateDataSource("/tmp/gsdm/polygon_reproj.shp")
	outlayer = ds.CreateLayer('', targetprj, ogr.wkbPolygon)
	outlayer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))

	#apply transformation
	i = 0

	for feature in layer:
	    transformed = feature.GetGeometryRef()
	    transformed.Transform(transform)

	    geom = ogr.CreateGeometryFromWkb(transformed.ExportToWkb())
	    defn = outlayer.GetLayerDefn()
	    feat = ogr.Feature(defn)
	    feat.SetField('id', i)
	    feat.SetGeometry(geom)
	    outlayer.CreateFeature(feat)
	    i += 1
	    feat = None

	ds = None

	return reprojected_shp

def createSampling(_params):
	# write parameters to R script

	aoi_shp = _params['aoi']
	soil_raster = _params['soil_raster']
	sampling_method = _params['sampling_method']
	strat_size = _params['strat_size']
	min_dist = _params['min_dist']
	edge = _params['edge']
	stop_dens = _params['stop_dens']
	output_name = _params['output_name']

	temp_dir = '/tmp/gsdm'
	#os.chdir(temp_dir)

	script_file = temp_dir + "/sampling_design.R"

	file = open(script_file, "w")
	file.write("working_directory<-'" + temp_dir + "'\n")
	file.write("raster_map<-'" + soil_raster + "'\n")
	file.write("aoi<-'" + aoi_shp + "'\n")
	file.write("sampling_method<-'" + sampling_method + "'\n")
	file.write("strat_size<-" + strat_size + "\n")
	file.write("min_dist<-" + min_dist + "\n")
	file.write("edge<-" + edge + "\n")
	file.write("stop_dens<-" + stop_dens + "\n")
	file.write("require('SurfaceTortoise')\n")
	file.write("require('mapsRinteractive')\n")
	file.write("require('raster')\n")
	file.write("setwd(working_directory)\n")
	file.write("r<-raster(raster_map)\n")
	file.write("a<-shapefile(aoi)\n")
	file.write("r<-mask(x=r, mask=a)\n")
	file.write("sampling<-tortoise(x1 = r,\n")
	file.write("y = a,\n")
	file.write("out_folder = 'samplingdata',\n")
	file.write("method = sampling_method,\n")
	file.write("strat_size = strat_size,\n")
	file.write("min_dist = min_dist, \n")
	file.write("edge= edge,\n")
	file.write("stop_dens2 = stop_dens,\n")
	file.write("plot_results = T)\n")
	file.close()

	return script_file