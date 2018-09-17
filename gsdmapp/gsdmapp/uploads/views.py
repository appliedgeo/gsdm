from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse

from gsdmapp.uploads.models import Shapefile
from gsdmapp.uploads.forms import ShapefileForm

def file_upload(request):
    # handle file upload
    if request.method == 'POST':
        form = ShapefileForm(request.POST, request.FILES)
        if form.is_valid():
            newfile = Shapefile(shapefile=request.FILES['shapefile'])
            newfile.save()

            # return message
            #upload_msg = {
            #    'message': 'upload successful'
            #}
            return HttpResponseRedirect(reverse('gsdmapp.views.app'))
