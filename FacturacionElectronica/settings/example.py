from .base import *

INSTALLED_APPS += [
    'facturacion',
    'rest_framework',
    'django_extensions',

]
# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


CORS_ORIGIN_ALLOW_ALL = True