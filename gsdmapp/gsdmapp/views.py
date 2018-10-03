from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
from gsdmapp.tools import *
import json
import zipfile

def app(request):
	return render_to_response('app.html')


def sampling_draw(request):
	# run sampling design on drawn aoi

	sampling_data = json.loads(request.body)

	aoi = sampling_data['aoi']

	# create shapefile from geojson data
	geometry = aoi['geometry']
	shpfile = createShp(geometry)

	# create script file
	user_params = {
		'aoi': shpfile,
		'soil_raster': sampling_data['soil_raster'],
		'sampling_method': sampling_data['method'],
		'strat_size': sampling_data['strat_size'],
		'min_dist': sampling_data['min_dist'],
		'edge': sampling_data['edge'],
		'stop_dens': sampling_data['criterium'],
		'output_name': sampling_data['output']
	}

	script_file = createSampling(user_params)

	# run script file
	runRscript(script_file)

	# get outputs 
	outputs = []

	# return outputs to user
	for file in os.listdir('/var/www/gsdm/data/samplingdata'):
		#if fnmatch.fnmatch(file, '*.shp'):
		outputs.append(file)


	sampling_response = {
		'samplingout': outputs
	}

	return JsonResponse(sampling_response)


def sampling_shp(request):
	# run sampling design on shapefile

	sampling_data = json.loads(request.body)

	# create script file
	user_params = {
		'aoi': sampling_data['shp'],
		'soil_raster': sampling_data['soil_raster'],
		'sampling_method': sampling_data['method'],
		'strat_size': sampling_data['strat_size'],
		'min_dist': sampling_data['min_dist'],
		'edge': sampling_data['edge'],
		'stop_dens': sampling_data['criterium'],
		'output_name': sampling_data['output']
	}

	script_file = createSampling(user_params)
	runRscript(script_file)

	# return outputs as zip file
	outputs = []

	for file in os.listdir('/var/www/gsdm/data/samplingdata'):
		#if fnmatch.fnmatch(file, '*.shp'):
		outputs.append(file)



	sampling_response = {
		'samplingout': outputs
	}

	return JsonResponse(sampling_response)



def local_adaptation(request):
	# run local map adaptation on shapefile/textfile

	adaptation_data = json.loads(request.body)

	# create script file
	script_file = createAdaptation(adaptation_data)

	# run adaptation
	runRscript(script_file)

	# return outputs as zip file
	outputs = []

	adaptation_response = {
		'adaptout': 'localadaptation'
	}

	return JsonResponse(adaptation_response)
