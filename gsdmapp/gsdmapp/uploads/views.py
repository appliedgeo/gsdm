from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse

from gsdmapp.uploads.models import Shapefile
from gsdmapp.uploads.forms import ShapefileForm
from zipfile import ZipFile

import os
import fnmatch

def uncompress(zipped):
    # unzip folder and extract shapefile
    zipped_path = '/var/www/gsdm/uploaded/shapefiles/' + zipped
    data_path = '/var/www/gsdm/data/'
    zf = ZipFile(zipped_path, 'r')
    zf.extractall(data_path)
    zf.close()

    unzipped = zipped.replace('.zip','')
    unzipped_dir = data_path + unzipped

    shpfile = ''

    for file in os.listdir(unzipped_dir):
        if fnmatch.fnmatch(file, '*.shp'):
            shpfile = file

    # clean up uploads folder
    os.system('rm -rf /var/www/gsdm/uploaded/shapefiles/*.*')

    return shpfile



def file_upload(request):
    # handle file upload
    if request.method == 'POST':
        form = ShapefileForm(request.POST, request.FILES)
        if form.is_valid():
            newfile = Shapefile(shapefile=request.FILES['shapefile'])
            newfile.save()

            zipped_file = os.path.basename(newfile.shapefile.name)

            _shapefile = uncompress(zipped_file)
            # return message
            upload_msg = {
                'message': 'upload successful',
                #'url': newfile.shapefile.name
                'url': _shapefile
            }
            #return HttpResponseRedirect(reverse('gsdmapp.views.app'))
            return JsonResponse(upload_msg)
