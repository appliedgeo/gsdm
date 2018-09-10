from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
import json

def app(request):
	return render_to_response('app.html')


def sampling(request, aoi, soil_raster, method, strat_size, min_dist, edge, criterium, output):
	# run sampling design
	pass