#
# Created on 2/7/2018 Allan Oware - CIAT
#
# Requirements:
#	arcpy
#
# Global Soil Data Manager Toolbox
# Tested on ArcGIS 10.5
#

import os, sys, subprocess, shlex, tempfile
import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [SamplingDesign, MapAdaptation]


class SamplingDesign(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Sampling Design"
        self.description = "Sampling Design"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # working directory
        param1 = arcpy.Parameter(
            displayName="R Executable",
            name="r_exec_path",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )

        # area of interest (shapefile)
        param2 = arcpy.Parameter(
            displayName="Area of Interest",
            name="aoi",
            datatype="DEShapefile",
            parameterType="Required",
            direction="Input"
        )

        # digital soil raster map
        param3 = arcpy.Parameter(
            displayName="Soil Raster Layer",
            name="soil_raster",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Input"
        )

        # optimize sampling parameters

        # sampling method
        param4 = arcpy.Parameter(
            displayName="Sampling Algorithm",
            name="sampling_method",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        param4.filter.list = ['stratdir','dir','grid','stratrand']

        # strat size
        param5 = arcpy.Parameter(
            displayName="Strat Size",
            name="strat_size",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input"
        )

        # minimum distance
        param6 = arcpy.Parameter(
            displayName="Minimum Distance",
            name="min_dist",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input"
        )

        # edge
        param7 = arcpy.Parameter(
            displayName="Edge",
            name="edge",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input"
        )

        # stop dens
        param8 = arcpy.Parameter(
            displayName="Stopping Criterium",
            name="stop_dens",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input"
        )

        output1 = arcpy.Parameter(
            displayName="Points Shapefile",
            name="points_shp",
            datatype="DEShapefile",
            parameterType="Derived",
            direction="Output"
        )

        output2 = arcpy.Parameter(
            displayName="Points Text",
            name="points_txt",
            datatype="DETextfile",
            parameterType="Derived",
            direction="Output"
        )

        output3 = arcpy.Parameter(
            displayName="Strata Shapefile",
            name="strata_shp",
            datatype="DEShapefile",
            parameterType="Derived",
            direction="Output"
        )

        params = [param1, param2, param3,
                  param4, param5, param6,
                  param7, param8, output1, output2, output3]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        #parameters[4].value = "stratdir"
        parameters[4].value = 100
        parameters[5].value = 10
        parameters[6].value = 10
        parameters[7].value = 1

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def create_script_file(self, _params):
        # write parameters to R file
        # get user input
        r_exec_path = _params[0].valueAsText
        r_exec_path = r_exec_path.replace('\\', '/')

        aoi = _params[1].valueAsText
        aoi = aoi.replace('\\','/')

        soil_raster = _params[2].valueAsText
        soil_raster = soil_raster.replace('\\','/')

        sampling_method = _params[3].valueAsText
        strat_size = _params[4].valueAsText
        min_dist = _params[5].valueAsText
        edge = _params[6].valueAsText
        stop_dens = _params[7].valueAsText

        temp_dir = tempfile.gettempdir()
        temp_dir = temp_dir.replace('\\','/')

        script_file = temp_dir + "/sampling_design.R"
        file = open(script_file, "w")
        file.write("working_directory<-'" + temp_dir + "'\n")
        file.write("raster_map<-'" + soil_raster + "'\n")
        file.write("aoi<-'" + aoi + "'\n")
        #file.write("epsg_code<-" + epsg_code + "\n")
        file.write("sampling_method<-'" + sampling_method + "'\n")
        file.write("strat_size<-" + strat_size + "\n")
        file.write("min_dist<-" + min_dist + "\n")
        file.write("edge<-" + edge + "\n")
        file.write("stop_dens<-" + stop_dens + "\n")
        file.write("require('SurfaceTortoise')\n")
        file.write("require('mapsRinteractive')\n")
        file.write("require('raster')\n")
        file.write("setwd(working_directory)\n")
        file.write("r<-raster(raster_map)\n")
        file.write("a<-shapefile(aoi)\n")
        file.write("r<-mask(x=r, mask=a)\n")
        file.write("sampling<-tortoise(x1 = r,\n")
        file.write("y = a,\n")
        #file.write("epsg = epsg_code,\n")
        file.write("out_folder = 'outdata',\n")
        file.write("method = sampling_method,\n")
        file.write("strat_size = strat_size,\n")
        file.write("min_dist = min_dist, \n")
        file.write("edge= edge,\n")
        file.write("stop_dens2 = stop_dens,\n")
        file.write("plot_results = T)\n")
        #file.write("\n")
        file.close()

        self.spatial_sampling(r_exec_path, script_file)
        self.display_outputs(temp_dir)


    def spatial_sampling(self, r_program, r_script):
        # run spatial sampling using surface tortoise
        arcpy.AddMessage("Running spatial sampling \n")
        #CREATE_NO_WINDOW = 0x08000000
        #process = subprocess.Popen(shlex.split(r_cmd), stdout=subprocess.PIPE, creationflags=CREATE_NO_WINDOW)

        process = subprocess.call([r_program, '--vanilla', r_script], shell=False)


    def display_outputs(self, outputs_dir):
        # display sampling outputs
        outputs_dir = outputs_dir + '/outdata/'

        st_points_shp = outputs_dir + '/st_points.shp'
        st_strata_shp = outputs_dir + '/st_strata.shp'
        st_points_txt = outputs_dir + '/st_points.txt'

        arcpy.SetParameter(8, st_points_shp)
        arcpy.SetParameter(9, st_points_txt)
        arcpy.SetParameter(10, st_strata_shp)

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # create params file
        self.create_script_file(parameters)

        return

class MapAdaptation(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Local Map Adaptation"
        self.description = "Local Map Adaptation"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        # upload sample
        param0 = arcpy.Parameter(
            displayName="R Executable Path",
            name="r_exec_dir",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )

        param1 = arcpy.Parameter(
            displayName="Raster Layer",
            name="raster_layer",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Input"
        )

        param2 = arcpy.Parameter(
            displayName="Points File (Text)",
            name="samples_file",
            datatype="DETextfile",
            parameterType="Required",
            direction="Input"
        )

        param3 = arcpy.Parameter(
            displayName="Attribute Column",
            name="attribute_column",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        param4 = arcpy.Parameter(
            displayName="X Coordinates",
            name="x_coords",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        param5 = arcpy.Parameter(
            displayName="Y Coordinates",
            name="y_coords",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )


        params = [param0, param1, param2, param3, param4, param5]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        parameters[3].value = "clay_percent"
        parameters[4].value = "POINT_X"
        parameters[5].value = "POINT_Y"
        parameters[6].value = 3006
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def create_params_file(self, _params):
        # write parameters to R file
        r_exec_dir = _params[0].valueAsText
        raster_layer = os.path.basename(_params[1].valueAsText)
        sample_file = os.path.basename(_params[2].valueAsText)
        attr_column = _params[3].valueAsText
        x_coords = _params[4].valueAsText
        y_coords = _params[5].valueAsText
        #epsg_code = _params[6].valueAsText

        r_exec_dir = r_exec_dir.replace('\\', '/')

        param_file = r_exec_dir + "\params.R"
        file = open(param_file, "w")
        file.write("r_exec_directory<-'" + r_exec_dir + "'\n")
        file.write("raster_map<-'" + raster_layer + "'\n")
        file.write("soil_sample<-'" + sample_file + "'\n")
        #file.write("epsg_code<-" + epsg_code + "\n")
        file.write("attr_column<-'" + attr_column + "'\n")
        file.write("x_coords<-'" + x_coords + "'\n")
        file.write("y_coords<-'" + y_coords + "'\n")
        file.close()

    def upload_sampling(self, _params):
        # run upload sampling
        r_exec_dir = _params[0].valueAsText
        r_exec_dir = r_exec_dir.replace('\\', '/')
        arcpy.AddMessage("Running sampling \n")
        r_script = r_exec_dir + '/run_upload_sampling.R'
        process = subprocess.call(['C:/Program Files/R/R-3.4.0//bin/i386/Rscript', '--vanilla', r_script], shell=False)

    def display_outputs(self, _params):
        # display sampling outputs
        r_exec_dir = _params[0].valueAsText

        mri_mapped_shp = r_exec_dir + '\\outdata\\mri_mapped_area.shp'
        mri_used_shp = r_exec_dir + '\\outdata\\mri_used_samples.shp'

        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
        mri_mapped_layer = arcpy.mapping.Layer(mri_mapped_shp)
        mri_used_layer = arcpy.mapping.Layer(mri_used_shp)

        arcpy.mapping.AddLayer(df, mri_mapped_layer)
        arcpy.mapping.AddLayer(df, mri_used_layer)

    def execute(self, parameters, messages):
        """The source code of the tool."""
        self.create_params_file(parameters)
        sampling = self.upload_sampling(parameters)
        outputs = self.display_outputs(parameters)
        return
