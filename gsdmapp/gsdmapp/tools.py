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

from geoserver.catalog import Catalog

data_dir = '/var/www/html/gsdm/data/'

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
    #tif = gdal.Open("/var/www/gsdm/data/soc_reproj21.tif")
    tif = gdal.Open("/var/www/html/gsdm/data/Soil_Carbon_0_30_250m_3857.tif")

    # shapefile with source projection
    driver = ogr.GetDriverByName("ESRI Shapefile")
    datasource = driver.Open("/var/www/html/gsdm/data/polygon.shp")
    layer = datasource.GetLayer()

    # set spatial reference and transformation
    sourceprj = layer.GetSpatialRef()
    targetprj = osr.SpatialReference(wkt = tif.GetProjection())
    transform = osr.CoordinateTransformation(sourceprj, targetprj)

    reprojected_shp = 'polygon_reproj.shp'

    to_fill = ogr.GetDriverByName("Esri Shapefile")
    ds = to_fill.CreateDataSource("/var/www/html/gsdm/data/polygon_reproj.shp")
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

    temp_dir = '/var/www/html/gsdm/data'
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
    file.write("plot_results = F)\n")
    file.write("epsg3857<-' +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs'\n")
    file.write("wgs84<-   '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'\n")
    file.write("crs(sampling$p.sp)<-epsg3857\n")
    file.write("crs(sampling$strat.sp)<-epsg3857\n")
    file.write("sampling$p.sp<- spTransform(sampling$p.sp, CRS(wgs84))\n")
    file.write("sampling$strat.sp <- spTransform(sampling$strat.sp, CRS(wgs84))\n")
    file.write("shapefile(sampling$p.sp, paste0(out_folder,'//points.shp'), overwrite=TRUE)\n")
    file.write("shapefile(sampling$strat.sp, paste0(out_folder,'//strata.shp'), overwrite=TRUE)\n")
    file.close()

    return script_file


def createAdaptation(_params):
    # write parameters to R script
    point_data = _params['pointdata']
    aoi_data = _params['aoidata']
    soil_raster = _params['soil_raster']
    attr_column = _params['attribute']
    #x_coords = _params['xcolumn']
    #y_coords = _params['ycolumn']
    x_coords = "x_coords"
    y_coords = "y_coords"
    #epsg_code = _params['epsg']
    epsg_code = '3857'

    output_name = 'adaptationout'

    temp_dir = '/var/www/html/gsdm/data'

    script_file = temp_dir + "/map_adaptation.R"

    file = open(script_file, "w")
    file.write("working_directory<-'" + temp_dir + "'\n")
    file.write("raster_map<-'" + soil_raster + "'\n")
    file.write("soil_sample<-'" + point_data + "'\n")
    file.write("aoi<-'" + aoi_data + "'\n")
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
    file.write("a<-shapefile(aoi)\n")
    file.write("r<-raster(raster_map)\n")
    file.write("r<-crop(r, a)\n")
    file.write("r<-mask(r, a)\n")
    file.write("epsg3857<-' +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs'\n")
    file.write("wgs84<-   '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'\n")
    file.write("crs(s)<-wgs84\n")
    file.write("s<- spTransform(s, CRS(epsg3857))\n")
    file.write("coordinates<-coordinates(s)\n")
    file.write("s$x_coords<-coordinates[,1]\n")
    file.write("s$y_coords<-coordinates[,2]\n")
  
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
    file.write("maps<-mri.out$all_maps.r\n")
    file.write("crs(maps)<-epsg3857\n")
    file.write("maps<-projectRaster (from=maps, crs=CRS(wgs84))\n")
    file.write("names(maps)<-c('map' , 'ordkrig',   'reskrig' ,  'regkrig')\n")
    file.write("writeRaster(maps, paste0(outfolder,'//a.tif'), bylayer=T, suffix='names', format='GTiff', overwrite=T)\n")
    file.write("\n")
    file.write("\n")
    file.write("\n")
    file.close()

    return script_file




def runRscript(r_script):
    # run R script
    # process = subprocess.call([r_program, '--vanilla', r_script], shell=False)
    os.system('sudo -u developer /usr/bin/Rscript --vanilla %s' % (r_script,))
    #process = subprocess.Popen('sudo -u servir-vic /usr/bin/Rscript --vanilla %s' % (r_script,))
    




def zipFolder(folder):
    # make zip archive from outputs directory
    os.chdir(data_dir)
    out_dir = data_dir + folder

    outputs_zip = shutil.make_archive(folder, 'zip', out_dir)

    _outputs_zip = os.path.basename(outputs_zip)

    return _outputs_zip


def publishRasters(folder):
    # publish adaptation output files (tifs) as wms
    cat = Catalog("https://beta8.ciat.cgiar.org/geoserver/rest", "developer", "greece@GREAT@said@42")

    out_dir = data_dir + folder
    _files = os.listdir(out_dir)

    wms_layers = []

    for file in _files:
        if fnmatch.fnmatch(file, '*.tif'):
            # unique store/layer name with timestamp
            tif_ext = datetime.now().strftime('%Y%m%d%H%M%S%f')
            _tif_ext = '_' + tif_ext + '.tif'
            _file = file.replace('.tif', _tif_ext)

            # publish to geoserver
            tiff = out_dir + '/' + file
            cat.create_coveragestore(_file, tiff)

            wms_layers.append(_file)


    return wms_layers



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


def output_sampling_geo(shape_file):
    # geojson conversion
    input_shp = data_dir + 'samplingout/'+shape_file

    # avoid duplicate geojson files
    geo_ext = datetime.now().strftime('%Y%m%d%H%M%S%f')
    geo_name = geo_ext + '.geojson'

    geojson = shape_file.replace('.shp',geo_name)
    _geojson = data_dir + 'vault/'+geojson

    with fiona.open(input_shp) as source:
        with fiona.open(_geojson, 'w', driver='GeoJSON', schema=source.schema) as sink:
            for rec in source:
                sink.write(rec)

    return geojson

def outputGeo(folder):
    # output geojson from outputs shapefiles
    points_output = 'points.shp'
    strata_output = 'strata.shp'

    points_geojson = output_sampling_geo(points_output)
    strata_geojson = output_sampling_geo(strata_output)

    return points_geojson, strata_geojson
