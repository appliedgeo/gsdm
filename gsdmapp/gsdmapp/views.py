from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
from django.db import connection

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

	outputs_dir = sampling_data['output']
	if outputs_dir == '':
		outputs_dir = 'samplingout'

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
	sampling_out = zipFolder(outputs_dir)

	sampling_response = {
		'samplingout': sampling_out
	}

	return JsonResponse(sampling_response)



def local_adaptation(request):
	# run local map adaptation on shapefile/textfile

	adaptation_data = json.loads(request.body)

	outputs_dir = adaptation_data['output']
	if outputs_dir == '':
		outputs_dir = 'adaptationout'

	# create script file
	script_file = createAdaptation(adaptation_data)

	# run adaptation and return outputs dir
	runRscript(script_file)

	# return outputs as zip file
	adaptation_out = zipFolder(outputs_dir)

	feedback, evaluation = getStats(outputs_dir)

	adaptation_response = {
		'adaptout': adaptation_out,
		'feedback': feedback,
		'evaluation': evaluation
	}

	return JsonResponse(adaptation_response)


def gadm(request):
    # return gadm countries as json
    cur = connection.cursor()

    cur.execute("""SELECT adm0_name FROM gadm0 ORDER BY adm0_name ASC""")
    countries = []
    for row in cur.fetchall():
        countries.append(row[0])

    gadm_json = {
        'countries': countries
    }

    cur.close()

    return JsonResponse(gadm_json)

def level1(request, country):
    # return gadm level 1 areas as json
    cur = connection.cursor()

    cur.execute("SELECT adm1_name FROM gadm1 WHERE adm0_name = %s", (country,))
    level1 = []
    for row in cur.fetchall():
        level1.append(row[0])

    cur.execute("SELECT ST_AsGeoJSON(ST_Centroid(geom)) FROM gadm0 WHERE adm0_name = %s", (country,))
    centroid = cur.fetchall()[0]

    cur.execute("SELECT ST_AsGeoJSON(geom) FROM gadm0 WHERE adm0_name = %s", (country,))
    boundary = cur.fetchall()[0]


    gadm_json = {
        'level1': level1,
        'centroid': eval(centroid[0]),
        'boundary': eval(boundary[0])
    }

    cur.close()

    return JsonResponse(gadm_json)


def level2(request, level1):
    # return gadm level 2 areas as json
    cur = connection.cursor()

    cur.execute("SELECT adm2_name FROM gadm2 WHERE adm1_name = %s",  (level1,))
    level2 = []
    for row in cur.fetchall():
        level2.append(row[0])

    cur.execute("SELECT ST_AsGeoJSON(ST_Centroid(geom)) FROM gadm1 WHERE adm1_name = %s", (level1,))
    centroid = cur.fetchall()[0]

    cur.execute("SELECT ST_AsGeoJSON(geom) FROM gadm1 WHERE adm1_name = %s", (level1,))
    boundary = cur.fetchall()[0]

    gadm_json = {
        'level2': level2,
        'centroid': eval(centroid[0]),
        'boundary': eval(boundary[0])
    }

    cur.close()

    return JsonResponse(gadm_json)


def level3(request, level2):
    # return gadm level 2 areas as geojson
    cur = connection.cursor()

    cur.execute("SELECT ST_AsGeoJSON(ST_Centroid(geom)) FROM gadm2 WHERE adm2_name = %s", (level2,))
    centroid = cur.fetchall()[0]

    cur.execute("SELECT ST_AsGeoJSON(geom) FROM gadm2 WHERE adm2_name = %s", (level2,))
    boundary = cur.fetchall()[0]

    gadm_json = {
        'centroid': eval(centroid[0]),
        'boundary': eval(boundary[0])
    }

    cur.close()

    return JsonResponse(gadm_json)




