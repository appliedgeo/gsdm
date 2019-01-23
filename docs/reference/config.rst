.. _config_guide:

========================
Configuration Guide
========================

Configuration settings and credentials for the GSDM platform are stored in the */home/ubuntu/gsdm/gsdmapp/gsdmapp/local_settings.py* file::
	
	DATABASE_ENGINE = 'postgresql_psycopg2'
	DATABASE_NAME = 'gsdm'
	DATABASE_USER = 'postgres'
	DATABASE_PASSWORD = 'postgres'
	DATABASE_HOST = ''
	DATABASE_PORT = '5432'

	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'NAME': DATABASE_NAME,
			'USER': DATABASE_USER,
			'PASSWORD': DATABASE_PASSWORD,
			'HOST': DATABASE_HOST,
			'PORT': DATABASE_PORT,
		},
	}

	UPLOAD_DIR = '/var/www/html/gsdm/'




	DATA_DIR = '/var/www/html/gsdm/data/'
	UPLOAD_PATH = '/var/www/html/gsdm/uploaded/shapefiles/'

	ALLOWED_HOSTS=['localhost', ]

	GEOSERVER_URL = 'http://localhost:8080/geoserver'
	GEOSERVER_USER = 'admin'
	GEOSERVER_PASS = 'geoserver'

	R_USER = 'ubuntu'


Notes
------

* Ensure the above file reflects the correct directories, server address, database settings, GeoServer credentials and R user.

* For a background soil map to be available on the web interface for visualization and for R processing, one copy has to be published to GeoServer and another copy placed in the GSDM data directory: */var/www/html/gsdm/data*

* Background soil maps must be in *EPSG:4326* projection for Geoserver publishing and *EPSG:3857* projection for R processing.

* All user submitted data must be in *EPSG:4326* projection with lat/long coordinates.
