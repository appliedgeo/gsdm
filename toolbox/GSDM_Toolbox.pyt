#
# Created on 2/7/2018 Allan Oware - CIAT
#
# Requirements:
#	arcpy
#
# Global Soil Data Manager Toolbox
# Tested on ArcGIS 10.5
#

import os, sys, subprocess, shlex
import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [DesignSampling, UploadSample]


class DesignSampling(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Design Sampling"
        self.description = "Design Sampling"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # working directory
        param1 = arcpy.Parameter(
            displayName="Working Directory",
            name="working_dir",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )

        # path to package (mapsRinteractive)
        """
        param2 = arcpy.Parameter(
            displayName="Path to mapsRinteractive package",
            name="mapsr_path",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        """

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
            displayName="Soil Raster Map",
            name="soil_raster",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Input"
        )

        # optimize sampling parameters
        # epsg code
        param4 = arcpy.Parameter(
            displayName="EPSG",
            name="epsg_code",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input"
        )

        # sampling method
        param5 = arcpy.Parameter(
            displayName="Sampling Method",
            name="sampling_method",
            datatype="GPString",
            parameterType="Optional",
            direction="Input"
        )

        # strat size
        param6 = arcpy.Parameter(
            displayName="Strat Size",
            name="strat_size",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input"
        )

        # minimum distance
        param7 = arcpy.Parameter(
            displayName="Minimum Distance",
            name="min_dist",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input"
        )

        # edge
        param8 = arcpy.Parameter(
            displayName="Edge",
            name="edge",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input"
        )

        # stop dens
        param9 = arcpy.Parameter(
            displayName="Stopping Criterium",
            name="stop_dens",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input"
        )

        params = [param1, param2, param3,
                  param4, param5, param6,
                  param7, param8, param9]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        parameters[3].value = 3006
        parameters[4].value = "stratdir"
        parameters[5].value = 100
        parameters[6].value = 10
        parameters[7].value = 10
        parameters[8].value = 1

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def create_params_file(self, _params):
        # write parameters to R file
        # get user input
        working_dir = _params[0].valueAsText
        #mapsr_path = _params[1].valueAsText
        aoi = os.path.basename(_params[1].valueAsText)
        soil_raster = os.path.basename(_params[2].valueAsText)
        epsg_code = _params[3].valueAsText
        sampling_method = _params[4].valueAsText
        strat_size = _params[5].valueAsText
        min_dist = _params[6].valueAsText
        edge = _params[7].valueAsText
        stop_dens = _params[8].valueAsText

        working_dir = working_dir.replace('\\','/')

        param_file = working_dir + "\params.R"
        file = open(param_file, "w")
        file.write("working_directory<-'" + working_dir + "'\n")
        file.write("raster_map<-'" + soil_raster + "'\n")
        file.write("aoi<-'" + aoi + "'\n")
        file.write("epsg_code<-" + epsg_code + "\n")
        file.write("sampling_method<-'" + sampling_method + "'\n")
        file.write("strat_size<-" + strat_size + "\n")
        file.write("min_dist<-" + min_dist + "\n")
        file.write("edge<-" + edge + "\n")
        file.write("stop_dens<-" + stop_dens + "\n")
        file.close()


    def spatial_sampling(self, _params):
        # run spatial sampling using surface tortoise
        working_dir = _params[0].valueAsText
        working_dir = working_dir.replace('\\', '/')
        arcpy.AddMessage("Running spatial sampling \n")
        #CREATE_NO_WINDOW = 0x08000000
        #process = subprocess.Popen(shlex.split(r_cmd), stdout=subprocess.PIPE, creationflags=CREATE_NO_WINDOW)
        r_script = working_dir + '/run_spatial_sampling.R'
        process = subprocess.call(['C:/Program Files/R/R-3.4.0//bin/i386/Rscript', '--vanilla', r_script], shell=False)


    def display_outputs(self, _params):
        # display sampling outputs
        working_dir = _params[0].valueAsText

        st_points_shp = working_dir + '\\outdata\\st_points.shp'
        st_strata_shp = working_dir + '\\outdata\\st_strata.shp'

        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
        st_points_layer = arcpy.mapping.Layer(st_points_shp)
        st_strata_layer = arcpy.mapping.Layer(st_strata_shp)

        arcpy.mapping.AddLayer(df, st_points_layer)
        arcpy.mapping.AddLayer(df, st_strata_layer)


    def execute(self, parameters, messages):
        """The source code of the tool."""
        # create params file
        self.create_params_file(parameters)
        # run sampling
        sampling = self.spatial_sampling(parameters)
        outputs = self.display_outputs(parameters)

        return

class UploadSample(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Upload Samples"
        self.description = "Upload Samples"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        # upload sample
        param0 = arcpy.Parameter(
            displayName="Working Directory",
            name="working_dir",
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
            displayName="Samples File (Text)",
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

        param6 = arcpy.Parameter(
            displayName="EPSG Code",
            name="epsg",
            datatype="GPLong",
            parameterType="Required",
            direction="Input"
        )

        params = [param0, param1, param2, param3, param4, param5, param6]
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
        working_dir = _params[0].valueAsText
        raster_layer = os.path.basename(_params[1].valueAsText)
        sample_file = os.path.basename(_params[2].valueAsText)
        attr_column = _params[3].valueAsText
        x_coords = _params[4].valueAsText
        y_coords = _params[5].valueAsText
        epsg_code = _params[6].valueAsText

        working_dir = working_dir.replace('\\', '/')

        param_file = working_dir + "\params.R"
        file = open(param_file, "w")
        file.write("working_directory<-'" + working_dir + "'\n")
        file.write("raster_map<-'" + raster_layer + "'\n")
        file.write("soil_sample<-'" + sample_file + "'\n")
        file.write("epsg_code<-" + epsg_code + "\n")
        file.write("attr_column<-'" + attr_column + "'\n")
        file.write("x_coords<-'" + x_coords + "'\n")
        file.write("y_coords<-'" + y_coords + "'\n")
        file.close()

    def upload_sampling(self, _params):
        # run upload sampling
        working_dir = _params[0].valueAsText
        working_dir = working_dir.replace('\\', '/')
        arcpy.AddMessage("Running sampling \n")
        r_script = working_dir + '/run_upload_sampling.R'
        process = subprocess.call(['C:/Program Files/R/R-3.4.0//bin/i386/Rscript', '--vanilla', r_script], shell=False)

    def display_outputs(self, _params):
        # display sampling outputs
        working_dir = _params[0].valueAsText

        mri_mapped_shp = working_dir + '\\outdata\\mri_mapped_area.shp'
        mri_used_shp = working_dir + '\\outdata\\mri_used_samples.shp'

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
