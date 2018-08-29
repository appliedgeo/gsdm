
DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = 'gsdm'
DATABASE_USER = 'postgres'
DATABASE_PASSWORD = 'postgres'
DATABASE_HOST = ''
DATABASE_PORT = '5432'

DATABASE = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': DATABASE_NAME,
		'USER': DATABASE_USER,
		'PASSWORD': DATABASE_PASSWORD,
		'HOST': DATABASE_HOST,
		'PORT': DATABASE_PORT,
	},
}

ALLOWED_HOSTS=['localhost', '45.33.28.192', ]