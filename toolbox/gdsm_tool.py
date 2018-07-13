#
# Created on 2/7/2018 Allan Oware - CIAT
#
# Requirements:
#	arcpy
#
# Global Soil Data Manager Toolbox
# Tested on ArcGIS 10.5
#

import os, sys, subprocess
import arcpy


soil_sample_data = arcpy.GetParameterAsText(0)
raster_map = arcpy.GetParameterAsText(1)
area_of_interest = arcpy.GetParameterAsText(2)

r_script_path = "D:\\2018\CIAT\dev\gsdm\\toolbox\scripts\\"

def create_param_file(soil_sample_data, raster_map, area_of_interest):
    # write parameters to R file
    _soil_sample_data = os.path.basename(soil_sample_data)
    _raster_map = os.path.basename(raster_map)
    _area_of_interest = os.path.basename(area_of_interest)

    param_file = r_script_path + "params.R"
    file = open(param_file, "w")
    file.write("soil_sample<-'indata/"+_soil_sample_data+"'\n")
    file.write("raster_map<-'indata/"+_raster_map+"'\n")
    file.write("aoi<-'indata/"+_area_of_interest+"'\n")
    file.close()

def run_gsdm():
    # takes user specified data, pass to configuration file and run R script
    r_cmd = "Rscript " + r_script_path + "example_modified.R > log.txt"
    subprocess.call(r_cmd, shell=False)

if __name__ == '__main__':
    create_param_file(soil_sample_data, raster_map,area_of_interest)
    run_gsdm()