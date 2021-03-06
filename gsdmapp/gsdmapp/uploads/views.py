from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse

from gsdmapp.uploads.models import Shapefile
from gsdmapp.uploads.forms import ShapefileForm
from gsdmapp import settings
from zipfile import ZipFile
from datetime import datetime
from geoserver.catalog import Catalog

import geoserver.util
from osgeo import ogr, osr, gdal
import fiona
import os
import fnmatch
import csv

data_path = settings.DATA_DIR
upload_path = settings.UPLOAD_PATH

def uncompress(zipped):
    # unzip folder and extract shapefile
    zipped_path = upload_path + zipped
    zf = ZipFile(zipped_path, 'r')
    zf.extractall(data_path)
    zf.close()

    unzipped = zipped.replace('.zip','')
    unzipped_dir = data_path + unzipped

    shpfile = ''

    for file in os.listdir(unzipped_dir):
        if fnmatch.fnmatch(file, '*.shp'):
            shpfile = file


    # copy to working dir 
    os.system('cp %s/*.* %s' % (unzipped_dir, data_path))

    # clean up uploads folder
    cmd = 'rm -rf ' + upload_path + '*.*'
    os.system(cmd)

    return shpfile


def publish_layer(shape_file):
    # reproject shapefile and publish to geoserver

    # reproject to wgs84: 4326
    # tif with target projection
    tiff_src = settings.DATA_DIR + 'soc_origin.tif'
    tif = gdal.Open(tiff_src)

    # shapefile with source projection
    driver = ogr.GetDriverByName("ESRI Shapefile")
    ds = data_path + shape_file
    datasource = driver.Open(ds)
    layer = datasource.GetLayer()

    # set spatial reference and transformation
    sourceprj = layer.GetSpatialRef()
    targetprj = osr.SpatialReference(wkt=tif.GetProjection())
    transform = osr.CoordinateTransformation(sourceprj, targetprj)

    reprojected_shp = shape_file.replace('.shp','') + '_reprojected.shp'

    to_fill = ogr.GetDriverByName("Esri Shapefile")
    new_ds = data_path + reprojected_shp
    ds2 = to_fill.CreateDataSource(new_ds)
    outlayer = ds2.CreateLayer('', targetprj, ogr.wkbPolygon)
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


    # geoserver publishing
    geoserver_api = settings.GEOSERVER_URL + '/rest'
    cat = Catalog(geoserver_api)

    shpfile = reprojected_shp.replace('.shp','')
    _shpfile = data_path + shpfile

    shapefile_plus_sidecars = geoserver.util.shapefile_and_friends(_shpfile)

    # avoid duplicate wms
    wms_ext = datetime.now().strftime('%Y%m%d%H%M%S%f')
    wms_name = shpfile + '_' + wms_ext

    ft = cat.create_featurestore(wms_name, shapefile_plus_sidecars)

    return wms_name

def geojson_layer(shape_file):
    # reproject shapefile and convert to geojson

    # reproject to wgs84: 4326
    # tif with target projection
    tiff_src = settings.DATA_DIR + 'Soil_Carbon_0_30_250m_4326.tif'
    tif = gdal.Open(tiff_src)

    # shapefile with source projection
    driver = ogr.GetDriverByName("ESRI Shapefile")
    ds = data_path + shape_file
    datasource = driver.Open(ds)
    layer = datasource.GetLayer()

    # set spatial reference and transformation
    sourceprj = layer.GetSpatialRef()
    targetprj = osr.SpatialReference(wkt=tif.GetProjection())
    transform = osr.CoordinateTransformation(sourceprj, targetprj)

    reprojected_shp = shape_file.replace('.shp','') + '_reprojected.shp'

    to_fill = ogr.GetDriverByName("Esri Shapefile")
    new_ds = data_path + reprojected_shp
    ds2 = to_fill.CreateDataSource(new_ds)
    outlayer = ds2.CreateLayer('', targetprj, ogr.wkbPolygon)
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
    input_shp = data_path + reprojected_shp

    # avoid duplicate geojson files
    geo_ext = datetime.now().strftime('%Y%m%d%H%M%S%f')
    geo_name = geo_ext + '.geojson'

    geojson = reprojected_shp.replace('reprojected.shp',geo_name)
    _geojson = data_path + geojson

    with fiona.open(input_shp) as source:
        with fiona.open(_geojson, 'w', driver='GeoJSON', schema=source.schema) as sink:
            for rec in source:
                sink.write(rec)

    return geojson

def geojson_point_layer(shape_file):
    # reproject shapefile and convert to geojson

    # reproject to wgs84: 4326
    # tif with target projection
    tiff_src = settings.DATA_DIR + 'Soil_Carbon_0_30_250m_4326.tif'
    tif = gdal.Open(tiff_src)

    # shapefile with source projection
    driver = ogr.GetDriverByName("ESRI Shapefile")
    ds = data_path + shape_file
    datasource = driver.Open(ds)
    layer = datasource.GetLayer()

    # set spatial reference and transformation
    sourceprj = layer.GetSpatialRef()
    targetprj = osr.SpatialReference(wkt=tif.GetProjection())
    transform = osr.CoordinateTransformation(sourceprj, targetprj)

    reprojected_shp = shape_file.replace('.shp','') + '_reprojected.shp'

    to_fill = ogr.GetDriverByName("Esri Shapefile")
    new_ds = data_path + reprojected_shp
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
    input_shp = data_path + reprojected_shp

    # avoid duplicate geojson files
    geo_ext = datetime.now().strftime('%Y%m%d%H%M%S%f')
    geo_name = geo_ext + '.geojson'

    geojson = reprojected_shp.replace('reprojected.shp',geo_name)
    _geojson = data_path + geojson

    with fiona.open(input_shp) as source:
        with fiona.open(_geojson, 'w', driver='GeoJSON', schema=source.schema) as sink:
            for rec in source:
                sink.write(rec)

    return geojson

def move_data(textfile):
    # move to working directory
    file_path = upload_path + textfile
    os.system('mv %s %s' % (file_path, data_path))

    return textfile

def txt2shp(textfile):
    # convert txt to shapefile
    # move to working directory and rename txt to csv
    file_path = upload_path + textfile

    csv_file = textfile.replace('.txt', '.csv')
    csv_path = data_path + csv_file

    os.system('mv %s %s' % (file_path, csv_path))

    # convert csv to shp
    _shp_file = textfile.replace('.txt', '.shp')
    _shp_file_path = data_path + _shp_file

    # AUTODETECT_TYPE=YES
    os.system('ogr2ogr -s_srs EPSG:4326 -t_srs EPSG:4326 -oo X_POSSIBLE_NAMES=LON* -oo Y_POSSIBLE_NAMES=LAT* -mapFieldType All=Real -f "ESRI Shapefile" %s %s' % (_shp_file_path, csv_path))


    return _shp_file


def shp_extract_fields(shape_file):
    # return shapefile fields
    daShapefile = data_path + shape_file

    dataSource = ogr.Open(daShapefile)
    daLayer = dataSource.GetLayer(0)
    layerDefinition = daLayer.GetLayerDefn()

    fields = []

    for i in range(layerDefinition.GetFieldCount()):
        fieldName = layerDefinition.GetFieldDefn(i).GetName()
        fieldTypeCode = layerDefinition.GetFieldDefn(i).GetType()
        fieldType = layerDefinition.GetFieldDefn(i).GetFieldTypeName(fieldTypeCode)

        #if fieldType == 'Real':
        fields.append(fieldName)


    return fields

def txt_extract_fields(txt_file):
    # return textfile fields
    text_file = data_path + txt_file

    with open(text_file) as inf:
        reader = csv.reader(inf, delimiter=" ")
        headers = reader.next()

        fields = headers[0].split()

    return fields



def sampling_file_upload(request):
    # handle sampling file upload
    if request.method == 'POST':
        form = ShapefileForm(request.POST, request.FILES)
        if form.is_valid():
            newfile = Shapefile(shapefile=request.FILES['shapefile'])
            newfile.save()

            zipped_file = os.path.basename(newfile.shapefile.name)

            # shapefile data
            uploadedfile = uncompress(zipped_file)
            layer_geojson = geojson_layer(uploadedfile)
            #layer_wms = 'no wms'
            # return message
            upload_msg = {
                'message': 'upload successful',
                'layer_wms': layer_geojson,
                'url': uploadedfile
            }
            return JsonResponse(upload_msg)


def adaptation_file_upload(request):
    # handle adaptation data upload
    if request.method == 'POST':
        form = ShapefileForm(request.POST, request.FILES)
        if form.is_valid():
            newfile = Shapefile(shapefile=request.FILES['shapefile'])
            newfile.save()

            zipped_file = os.path.basename(newfile.shapefile.name)

            if 'zip' in zipped_file:
                # shapefile data
                uploadedfile = uncompress(zipped_file)
                layer_wms = geojson_point_layer(uploadedfile)
                #layer_wms = 'no wms'
                data_fields = shp_extract_fields(uploadedfile)
            else:
                # text data
                #uploadedfile = move_data(zipped_file)
                shp_file = txt2shp(zipped_file)
                uploadedfile = shp_file
                #data_fields = txt_extract_fields(uploadedfile)
                data_fields = shp_extract_fields(shp_file)
                #layer_wms = 'no wms'
                layer_wms = geojson_point_layer(shp_file)
            # return message
            upload_msg = {
                'message': 'upload successful',
                'fields': data_fields,
                'url': uploadedfile,
                'layer_wms': layer_wms

            }
            return JsonResponse(upload_msg)
