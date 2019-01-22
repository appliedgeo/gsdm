
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

UPLOAD_DIR = '/var/www/gsdm/'




DATA_DIR = '/var/www/gsdm/data/'
UPLOAD_PATH = '/var/www/gsdm/uploaded/shapefiles/'

ALLOWED_HOSTS=['localhost', ]

GEOSERVER_URL = 'http://localhost:8080/geoserver'
GEOSERVER_USER = 'admin'
GEOSERVER_PASS = 'geoserver'

R_USER = 'servir-vic'