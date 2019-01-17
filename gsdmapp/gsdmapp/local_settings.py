
DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = 'gsdm'
DATABASE_USER = 'gsdm'
DATABASE_PASSWORD = '?wheel?STONE?strike?12'
DATABASE_HOST = '192.168.20.3'
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

ALLOWED_HOSTS=['localhost', '45.33.28.192', 'gsdmtest.ciat.cgiar.org']
