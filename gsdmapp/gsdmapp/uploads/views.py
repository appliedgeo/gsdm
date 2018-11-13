from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse

from gsdmapp.uploads.models import Shapefile
from gsdmapp.uploads.forms import ShapefileForm
from zipfile import ZipFile
from datetime import datetime
from geoserver.catalog import Catalog

import geoserver.util
from osgeo import ogr, osr, gdal
import os
import fnmatch
import csv

data_path = '/var/www/gsdm/data/'
upload_path = '/var/www/gsdm/uploaded/shapefiles/'

def uncompress(zipped):
    # unzip folder and extract shapefile
    zipped_path = '/var/www/gsdm/uploaded/shapefiles/' + zipped
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
    # os.system('gdal_translate -of GTiff -a_ullr 33.9402616506841 0.155713888855809 34.1237268086358 0.0483376209782989 -a_srs EPSG:4326 %s %s' % (tifname, tifname2))
    os.system('cp %s/*.* %s' % (unzipped_dir, data_path))

    # clean up uploads folder
    os.system('rm -rf /var/www/gsdm/uploaded/shapefiles/*.*')

    return shpfile


def publish_layer(shape_file):
    # reproject shapefile and publish to geoserver

    # reproject to planar coordinate system: 3857
    # tif with target projection
    tif = gdal.Open("/var/www/gsdm/data/soc_origin.tif")

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
    cat = Catalog("http://localhost:8080/geoserver/rest")

    shpfile = reprojected_shp.replace('.shp','')
    _shpfile = data_path + shpfile

    shapefile_plus_sidecars = geoserver.util.shapefile_and_friends(_shpfile)

    # avoid duplicate wms
    wms_ext = datetime.now().strftime('%Y%m%d%H%M%S%f')
    wms_name = shpfile + '_' + wms_ext

    ft = cat.create_featurestore(wms_name, shapefile_plus_sidecars)

    return wms_name



def move_data(textfile):
    # move to working directory
    file_path = upload_path + textfile
    os.system('mv %s %s' % (file_path, data_path))

    return textfile


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

        if fieldType == 'Real':
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
            #layer_wms = publish_layer(uploadedfile)
            layer_wms = 'no wms'
            # return message
            upload_msg = {
                'message': 'upload successful',
                'layer_wms': layer_wms,
                'url': uploadedfile
            }
            #return HttpResponseRedirect(reverse('gsdmapp.views.app'))
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
                #layer_wms = publish_layer(uploadedfile)
                layer_wms = 'no wms'
                data_fields = shp_extract_fields(uploadedfile)
            else:
                # text data
                uploadedfile = move_data(zipped_file)
                data_fields = txt_extract_fields(uploadedfile)
                layer_wms = 'no wms'
            # return message
            upload_msg = {
                'message': 'upload successful',
                'fields': data_fields,
                'url': uploadedfile,
                'layer_wms': layer_wms

            }
            #return HttpResponseRedirect(reverse('gsdmapp.views.app'))
            return JsonResponse(upload_msg)
