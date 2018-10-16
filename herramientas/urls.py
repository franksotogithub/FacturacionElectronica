from django.conf.urls import url
from .views import *

app_name = 'herramientas'
urlpatterns = [
    url(r'^datos/$', DatosView.as_view(), name='datos'),
    ]