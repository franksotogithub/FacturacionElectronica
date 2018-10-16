from django.conf.urls import url
from .views import *

app_name = 'configuracion'
urlpatterns = [
    url(r'^locales/$', Locales.as_view(), name='locales'),
    url(r'^parametros/$', Parametros.as_view(), name='parametros'),
    ]