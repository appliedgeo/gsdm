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


import os, sys, subprocess
import math
import fnmatch
import fiona
import json
import zipfile
import shutil
import csv

from datetime import datetime
from fiona.crs import from_epsg
from osgeo import ogr, osr, gdal

data_dir = '/var/www/gsdm/data/'

def createShp(poly):
    #create shapefile from user geojson
    os.chdir(data_dir)

    schema = {'geometry': 'Polygon','properties': {'fld_a': 'str:50'}}

    shpfile = 'polygon.shp'

    #_crs = from_epsg(3857)

    with fiona.open(shpfile, 'w', 'ESRI Shapefile', schema) as layer:
        layer.write({'geometry': poly, 'properties': {'fld_a': 'test'}})

        spatialRef = osr.SpatialReference()
        spatialRef.ImportFromEPSG(4326)

        spatialRef.MorphToESRI()
        prjfile = open('polygon.prj', 'w')
        prjfile.write(spatialRef.ExportToWkt())
        prjfile.close()

    reprojected = reProject(shpfile)


    return reprojected


def reProject(shapefile):
    # reproject to planar coordinate system: 3857
    # tif with target projection
    tif = gdal.Open("/var/www/gsdm/data/soc_reproj21.tif")

    # shapefile with source projection
    driver = ogr.GetDriverByName("ESRI Shapefile")
    datasource = driver.Open("/var/www/gsdm/data/polygon.shp")
    layer = datasource.GetLayer()

    # set spatial reference and transformation
    sourceprj = layer.GetSpatialRef()
    targetprj = osr.SpatialReference(wkt = tif.GetProjection())
    transform = osr.CoordinateTransformation(sourceprj, targetprj)

    reprojected_shp = 'polygon_reproj.shp'

    to_fill = ogr.GetDriverByName("Esri Shapefile")
    ds = to_fill.CreateDataSource("/var/www/gsdm/data/polygon_reproj.shp")
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
    
    output_name = 'samplingout'

    temp_dir = '/var/www/gsdm/data'
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
    file.write("out_folder<-'" + output_name + "'\n")
    file.write("require('SurfaceTortoise')\n")
    file.write("require('mapsRinteractive')\n")
    file.write("require('raster')\n")
    file.write("setwd(working_directory)\n")
    file.write("r<-raster(raster_map)\n")
    file.write("a<-shapefile(aoi)\n")
    file.write("r<-crop(r, a)\n")
    file.write("r<-mask(r, a)\n")
    #file.write("r<-mask(crop(x=r, mask=a))\n")
    #file.write("r<-mask(x=r, mask=a)\n")
    file.write("sampling<-tortoise(x1 = r,\n")
    file.write("y = a,\n")
    #file.write("out_folder = out_folder,\n")
    file.write("method = sampling_method,\n")
    file.write("strat_size = strat_size,\n")
    file.write("min_dist = min_dist, \n")
    file.write("edge= edge,\n")
    file.write("stop_n = stop_dens,\n")
    file.write("stop_dens1 = 10000000,\n")
    file.write("stop_dens2 = 10000000,\n")
    file.write("plot_results = T)\n")
    file.write("shapefile(sampling$p.sp, paste0(out_folder,'//points.shp'), overwrite=TRUE)\n")
    file.write("shapefile(sampling$strat.sp, paste0(out_folder,'//strata.shp'), overwrite=TRUE)\n")
    file.close()

    return script_file


def createAdaptation(_params):
    # write parameters to R script
    point_data = _params['pointdata']
    soil_raster = _params['soil_raster']
    attr_column = _params['attribute']
    x_coords = _params['xcolumn']
    y_coords = _params['ycolumn']
    epsg_code = _params['epsg']

    output_name = 'adaptationout'

    temp_dir = '/var/www/gsdm/data'

    script_file = temp_dir + "/map_adaptation.R"

    file = open(script_file, "w")
    file.write("working_directory<-'" + temp_dir + "'\n")
    file.write("raster_map<-'" + soil_raster + "'\n")
    file.write("soil_sample<-'" + point_data + "'\n")
    file.write("attr_column<-'" + attr_column + "'\n")
    file.write("x_coords<-'" + x_coords + "'\n")
    file.write("y_coords<-'" + y_coords + "'\n")
    file.write("epsg_code<-" + epsg_code + "\n")
    file.write("out_folder<-'" + output_name + "'\n")
    file.write("require('SurfaceTortoise')\n")
    file.write("require('mapsRinteractive')\n")
    file.write("require('raster')\n")
    file.write("setwd(working_directory)\n")

    if 'txt' in point_data:
        file.write("s<-read.table(file=soil_sample, header = T, sep = \"\\t\")[,1:4]\n")
    else:
        file.write("s<-shapefile(soil_sample)\n")
    file.write("r<-raster(raster_map)\n")
    file.write("mri.out<-mri(\n")
    file.write("rst.r = r,\n")
    file.write("pts.df =s,\n")
    file.write("pts.attr = attr_column,\n")
    file.write("pts.x= x_coords,\n")
    file.write("pts.y= y_coords,\n")
    file.write("epsg = epsg_code,\n")
    file.write("out.folder = out_folder,\n")
    file.write("out.prefix = 'mri_',\n")
    file.write("out.dec = \".\", \n")
    file.write("out.sep = \";\"\n")
    file.write(")\n")
    file.write("\n")
    file.write("\n")
    file.write("\n")
    file.close()

    return script_file




def runRscript(r_script):
    # run R script
    # process = subprocess.call([r_program, '--vanilla', r_script], shell=False)
    os.system('sudo -u servir-vic /usr/bin/Rscript --vanilla %s' % (r_script,))
    #process = subprocess.Popen('sudo -u servir-vic /usr/bin/Rscript --vanilla %s' % (r_script,))




def zipFolder(folder):
    # make zip archive from outputs directory
    os.chdir(data_dir)
    out_dir = data_dir + folder

    outputs_zip = shutil.make_archive(folder, 'zip', out_dir)

    _outputs_zip = os.path.basename(outputs_zip)

    return _outputs_zip



def getStats(folder):
    # get statistics and evaluation data
    feedback_file = data_dir + folder + '/mri_feedback.txt'
    evaluation_file = data_dir + folder + '/mri_evaluation.txt'
    feedback_stats = []
    evaluation_stats = []
    with open(feedback_file) as txt_file:
        reader = csv.reader(txt_file, delimiter=';')
        next(reader)
        for row in reader:
            feedback_stats.append(row[1])

    with open(evaluation_file) as txt_file:
        reader = csv.reader(txt_file, delimiter=';')
        next(reader)
        for row in reader:
            evaluation_stats.append([float("{0:.6f}".format(float(row[1]))), float("{0:.6f}".format(float(row[2]))),float("{0:.6f}".format(float(row[3]))), float("{0:.6f}".format(float(row[4]))), float("{0:.6f}".format(float(row[5])))])


    return feedback_stats, evaluation_stats


def output_point_geo(shape_file):
    # reproject shapefile and convert to geojson

    # reproject to wgs84: 4326
    # tif with target projection
    tif = gdal.Open("/var/www/gsdm/data/soc_origin.tif")

    # shapefile with source projection
    driver = ogr.GetDriverByName("ESRI Shapefile")
    ds = data_path +'samplingout/'+ shape_file
    datasource = driver.Open(ds)
    layer = datasource.GetLayer()

    # set spatial reference and transformation
    sourceprj = layer.GetSpatialRef()
    targetprj = osr.SpatialReference(wkt=tif.GetProjection())
    transform = osr.CoordinateTransformation(sourceprj, targetprj)

    reprojected_shp = shape_file.replace('.shp','') + '_reprojected.shp'

    to_fill = ogr.GetDriverByName("Esri Shapefile")
    new_ds = data_path + 'samplingout/' + reprojected_shp
    ds2 = to_fill.CreateDataSource(new_ds)
    outlayer = ds2.CreateLayer('', targetprj, ogr.wkbPoint)
    outlayer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))

    # apply transformation
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

    ds2 = None


    # geojson conversion
    input_shp = data_path + 'samplingout/'+reprojected_shp

    # avoid duplicate geojson files
    geo_ext = datetime.now().strftime('%Y%m%d%H%M%S%f')
    geo_name = geo_ext + '.geojson'

    geojson = reprojected_shp.replace('reprojected.shp',geo_name)
    _geojson = data_path + 'samplingout/'+geojson

    with fiona.open(input_shp) as source:
        with fiona.open(_geojson, 'w', driver='GeoJSON', schema=source.schema) as sink:
            for rec in source:
                sink.write(rec)

    return geojson

def outputGeo(folder):
    # output geojson from outputs shapefiles
    points_output = 'points.shp'
    strata_output = 'strata.shp'

    points_geojson = output_point_geo(points_output)

    return points_geojson
