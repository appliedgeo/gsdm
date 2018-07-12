#
# Created on 2/7/2018 Allan Oware - CIAT
#
# Requirements:
#	arcpy
#
# Global Soil Data Manager Toolbox
# Tested on ArcGIS 10.5 and
#

import os, sys, subprocess
import arcpy


soil_sample_data = arcpy.GetParameterAsText(0)
raster_map = arcpy.GetParameterAsText(1)
area_of_interest = arcpy.GetParameterAsText(2)

r_script_path = "D:\\2018\CIAT\src\\"

def run_gsdm(soil_sample_data, raster_map, area_of_interest):
    # takes user specified data, pass to configuration file and run R script
    r_cmd = "Rscript " + r_script_path + "example_modified.R > log.txt"
    subprocess.call(r_cmd, shell=False)

if __name__ == '__main__':
    run_gsdm(soil_sample_data, raster_map, area_of_interest)