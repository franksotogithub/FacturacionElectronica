from django.conf.urls import url
from .views import *

app_name = 'webclient'
urlpatterns = [

    url(r'^$', IndexView.as_view(), name='index'),
    ]