from .base import *

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'franksoto2012@gmail.com'
EMAIL_HOST_PASSWORD = 'MBs0p0rt301'
EMAIL_PORT = 587

RUC= '10452575014'

SUNAT_ARCHIVOS_ROOT = r'\\DESKTOP-ML6FRVL\sunat_archivos\sfs'
SUNAT_DATABASE_ROOT = r'\\DESKTOP-ML6FRVL\bd'

MEDIA_ROOT_FILES =os.path.join(SUNAT_ARCHIVOS_ROOT,'FIRMA')
MEDIA_ROOT_FILES_TXT =os.path.join(SUNAT_ARCHIVOS_ROOT,'DATA')
MEDIA_ROOT_FILES_PDF =os.path.join(SUNAT_ARCHIVOS_ROOT,'REPO')
MEDIA_ROOT_IMG =os.path.join(BASE_DIR, "static","img")
MEDIA_ROOT_FILES_XML_FIRMA =os.path.join(SUNAT_ARCHIVOS_ROOT,'FIRMA')

MEDIA_ROOT_FILES_XML_RPTA =os.path.join(SUNAT_ARCHIVOS_ROOT, 'RPTA')
MEDIA_ROOT_FILES_XML_ENVIO =os.path.join(SUNAT_ARCHIVOS_ROOT,'ENVIO')

QR_CODE_CACHE_ALIAS = 'qr-code'

INSTALLED_APPS += [
    'facturacion',
    'usuarios',
    'modulos',
    'herramientas',
    'rest_framework',
    'django_extensions',
    'qr_code',
    'mptt',
    'sunat',
    'configuracion',
    'import_export',
    'djcelery',
    #'django_celery_results',

]
# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'sql_server.pyodbc',
        'HOST': '192.168.0.100',
        'NAME': 'FACTURACION_ELECTRONICA',
        'USER': 'fsoto',
        'PASSWORD': 'MBs0p0rt301',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'SQL Server Native Client 10.0',
        },
    },
    'romasa': {
        'ENGINE': 'sql_server.pyodbc',
        'HOST': '192.168.0.100',
        'NAME': '003BDCOMUN',
        'USER': 'fsoto',
        'PASSWORD': 'MBs0p0rt301',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'SQL Server Native Client 10.0',
        },
    },
    'sunat':{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SUNAT_DATABASE_ROOT, 'BDFacturador.db'),
    },

}

DATABASE_ROUTERS = ['core.dbrouters.SunatRouter','core.dbrouters.FacturacionRouter']
AUTH_USER_MODEL = 'usuarios.Usuario'
CORS_ORIGIN_ALLOW_ALL = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 300 # set just 10 seconds to test
SESSION_SAVE_EVERY_REQUEST = True
BROKER_URL = 'amqp://guest:guest@localhost//'
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
#CELERY_RESULT_BACKEND='django-db'

import djcelery
djcelery.setup_loader()


from datetime import timedelta
from celery.schedules import crontab

#CELERYBEAT_SCHEDULE = {
    #'add-every-30-seconds': {
    #    'task': 'facturacion.tasks.sumar',
    #    'schedule': timedelta(seconds=5),
    #    'args': (15, 35),
    #    #‘schedule’: timedelta(seconds=30),
    #    #‘args’: (15, 35)
    #},

#}


CELERYBEAT_SCHEDULE = {
    # Executes every Monday morning at 7:30 A.M

    'migrar_comprobantes':{
    'task': 'herramientas.tasks.generar_tareas_task',
    'schedule': crontab(hour=7, minute=30, day_of_week=1),
    'args': ([1,2,4]),
    },

    'actualizar_estados':{
    'task': 'herramientas.tasks.generar_tareas_task',
    'schedule': crontab(hour='*', minute=30, day_of_week=1),
    'args': ([5]),
    },

    'migrar_anulaciones':{
    'task': 'herramientas.tasks.generar_tareas_task',
    'schedule': crontab(hour=9, minute=30, day_of_week=1),
    'args': ([3,4]),
    },

}
TIME_ZONE = 'America/Lima'
LANGUAGE_CODE = 'es-PE'
USE_I18N = True
USE_L10N = True
USE_TZ = False
