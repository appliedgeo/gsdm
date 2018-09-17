from django.db import models

class Shapefile(models.Model):
    shapefile = models.FileField(upload_to='shapefiles/%Y/%m/%d')
