#install packages
path_to_package<-"F:/working/mapsRinteractive_0.1.0.tar.gz"

install.packages('raster')
install.packages('SurfaceTortoise', repos = "http://cran.us.r-project.org")
install.packages(path_to_package, 
                 repos = NULL, 
                 type = "source"
                 )
