#load configuration
source("F:/working/params.R")

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
#a<-shapefile(aoi)

#crop raster to area of interest
##this is not necessary
#r<-mask(x=r, mask=a)


#example run of mapsRinteractive
mri.out<-mri(
  rst.r = r,
  pts.df =s,
  pts.attr = attr_column,
  pts.x= x_coords,
  pts.y= y_coords,
  epsg = epsg_code,
  out.folder = 'outdata',
  out.prefix = 'mri_',
  out.dec = ".", 
  out.sep = ";"
)

#wiew results
#plot(mri.out$all_maps.r)
##map = original map
##ordkrig = map produced by interpolation of soil samples
##reskrig and regkrig = maps produced by a combination of the original map and 
##the samples (two different methods for local adaptation)
#mri.out$evaluation
