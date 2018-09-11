from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
import json

def app(request):
	return render_to_response('app.html')


def sampling(request):
	# run sampling design

	sampling_data = json.loads(request.body)

	aoi = sampling_data['aoi']
	soil_raster = sampling_data['soil_raster']
	method = sampling_data['method']
	strat_size = sampling_data['strat_size']
	min_dist = sampling_data['min_dist']
	edge = sampling_data['edge']
	criterium = sampling_data['criterium']
	output = sampling_data['output']


	sampling_response = {
		'result': aoi
	}

	#return HttpResponse(json.dumps(sampling_response), mimetype="application/json")
	return JsonResponse(sampling_response)