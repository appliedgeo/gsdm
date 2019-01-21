from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
from django.db import connection

from geoserver.catalog import Catalog

from gsdmapp.tools import *
import json
import zipfile
import fnmatch

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
		'stop_dens': sampling_data['criterium']
		
	}

	outputs_dir = 'samplingout'

	script_file = createSampling(user_params)

	# run script file
	runRscript(script_file)

	# return outputs as zip file
	sampling_out = zipFolder(outputs_dir)

	# convert output to geojson
	points_out, strata_out = outputGeo(outputs_dir)
	
	sampling_response = {
		'samplingout': sampling_out,
		'pointsout': points_out,
		'strataout': strata_out
	}

	return JsonResponse(sampling_response)


def sampling_shp(request):
	# run sampling design on shapefile

	sampling_data = json.loads(request.body)

	outputs_dir = 'samplingout'

	# create script file
	user_params = {
		'aoi': sampling_data['shp'],
		'soil_raster': sampling_data['soil_raster'],
		'sampling_method': sampling_data['method'],
		'strat_size': sampling_data['strat_size'],
		'min_dist': sampling_data['min_dist'],
		'edge': sampling_data['edge'],
		'stop_dens': sampling_data['criterium']
	}

	script_file = createSampling(user_params)
	runRscript(script_file)

	# return outputs as zip file
	sampling_out = zipFolder(outputs_dir)
	points_out, strata_out = outputGeo(outputs_dir)

	sampling_response = {
		'samplingout': sampling_out,
		'pointsout': points_out,
		'strataout': strata_out        
	}

	return JsonResponse(sampling_response)



def local_adaptation(request):
	# run local map adaptation on shapefile/textfile

	adaptation_data = json.loads(request.body)

	outputs_dir = 'adaptationout'

	# create script file
	script_file = createAdaptation(adaptation_data)

	# run adaptation and return outputs dir
	runRscript(script_file)

	# return outputs as zip file
	adaptation_out = zipFolder(outputs_dir)

	# publish rasters
	adaptation_wms = publishRasters(outputs_dir)

	feedback, evaluation = getStats(outputs_dir)

	adaptation_response = {
		'adaptout': adaptation_out,
		'feedback': feedback,
		'evaluation': evaluation,
		'adaptwms': adaptation_wms
	}

	return JsonResponse(adaptation_response)

def soilmaps(request):
	# return list of soilmap layers from geoserver
	cat = Catalog("http://localhost:8080/geoserver/rest")
	#gsdm_space = cat.get_resource(workspace='gsdm')
	all_layers = cat.get_layers()

	soil_maps = []
	for layer in all_layers:
		layer_name = layer.name
		if not fnmatch.fnmatch(layer_name, 'mri*'):
			soil_maps.append(layer_name)

	layers_json = {
		'soil_maps': soil_maps
	}

	return JsonResponse(layers_json)


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

    cur.execute("SELECT ST_AsGeoJSON(geom) FROM gadm0 WHERE adm0_name = %s", (country,))
    boundary = cur.fetchall()[0]


    gadm_json = {
        'level1': level1,
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

    cur.execute("SELECT ST_AsGeoJSON(geom) FROM gadm1 WHERE adm1_name = %s", (level1,))
    boundary = cur.fetchall()[0]

    gadm_json = {
        'level2': level2,
        'boundary': eval(boundary[0])
    }

    cur.close()

    return JsonResponse(gadm_json)


def level3(request, level2):
    # return gadm level 2 areas as geojson
    cur = connection.cursor()

    cur.execute("SELECT ST_AsGeoJSON(geom) FROM gadm2 WHERE adm2_name = %s", (level2,))
    boundary = cur.fetchall()[0]

    gadm_json = {
        'boundary': eval(boundary[0])
    }

    cur.close()

    return JsonResponse(gadm_json)




