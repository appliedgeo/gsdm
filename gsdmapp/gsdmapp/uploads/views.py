from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse

from gsdmapp.uploads.models import Shapefile
from gsdmapp.uploads.forms import ShapefileForm
from zipfile import ZipFile
from osgeo import ogr

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
            # return message
            upload_msg = {
                'message': 'upload successful',
                #'url': newfile.shapefile.name
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
                data_fields = shp_extract_fields(uploadedfile)
            else:
                # text data
                uploadedfile = move_data(zipped_file)
                data_fields = txt_extract_fields(uploadedfile)
            # return message
            upload_msg = {
                'message': 'upload successful',
                'fields': data_fields,
                'url': uploadedfile
            }
            #return HttpResponseRedirect(reverse('gsdmapp.views.app'))
            return JsonResponse(upload_msg)
