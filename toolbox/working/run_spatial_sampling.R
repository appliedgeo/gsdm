#load params
source("F:/working/params.R")

#load packages
require('SurfaceTortoise')
require('mapsRinteractive')
require('raster')

#set working directory
setwd(working_directory)

#import data
##soil sample data (lab results)
#s<-read.table(file=soil_sample, header = T, sep = "\t")[,1:4]
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
                   epsg = epsg_code, 
                   out_folder = 'outdata', ##check this folder for results after wards
                   method = sampling_method,
                   strat_size = strat_size,
                   min_dist = min_dist, 
                   edge= edge,
                   stop_dens2 = stop_dens,
                   plot_results = T
)

#wiew results
#plot(r)
#plot(sampling$strat.sp, add=T)
#plot(sampling$p.sp, add=T, pch=16)
as.data.frame(sampling$p.sp)

#wiew results
#plot(mri.out$all_maps.r)
##map = original map
##ordkrig = map produced by interpolation of soil samples
##reskrig and regkrig = maps produced by a combination of the original map and 
##the samples (two different methods for local adaptation)
#mri.out$evaluation
