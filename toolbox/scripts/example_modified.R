#load configuration
source("D:/2018/CIAT/dev/gsdm/toolbox/scripts/config.R")  
source("D:/2018/CIAT/dev/gsdm/toolbox/scripts/params.R")

#load packages
require('SurfaceTortoise')
require('mapsRinteractive')
require('raster')

#set working directory
setwd(working_directory)

#import data
##soil sample data (lab results)
s<-read.table(file=soil_sample, header = T, sep = "\t")[,1:4]
##a raster map of clay content (an excerpt of the digital soi lmap of Sweden, dsms)
r<-raster(raster_map) 
#a shapefile delineating the farm where the soil samples were taken
a<-shapefile(aoi)

#crop raster to area of interest
##this is not necessary
r<-mask(x=r, mask=a)

#example run of the tortoise function
sampling<-tortoise(x1 = r, 
         y = a,
         epsg = 3006, 
         out_folder = 'outdata', ##check this folder for results after wards
         method = 'stratdir',
         strat_size = 100,
         min_dist = 10, 
         edge=10,
         stop_dens2 = 1,
         plot_results = T
         )

#wiew results
plot(r)
plot(sampling$strat.sp, add=T)
plot(sampling$p.sp, add=T, pch=16)
as.data.frame(sampling$p.sp)

#example run of mapsRinteractive
mri.out<-mri(
  rst.r = r,
  pts.df =s,
  pts.attr ='clay_percent',
  pts.x= 'POINT_X',
  pts.y= 'POINT_Y',
  epsg = 3006,
  out.folder = 'outdata',
  out.prefix = 'mri_',
  out.dec = ".", 
  out.sep = ";"
)

#wiew results
plot(mri.out$all_maps.r)
##map = original map
##ordkrig = map produced by interpolation of soil samples
##reskrig and regkrig = maps produced by a combination of the original map and 
##the samples (two different methods for local adaptation)
mri.out$evaluation
