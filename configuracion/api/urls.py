from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import EmpresaParametroViewSet , LocalViewSet


app_name = 'configuracion'
router = DefaultRouter()
router.register(r'parametros',EmpresaParametroViewSet ,base_name='parametros')
router.register(r'locales', LocalViewSet ,base_name='locales')
urlpatterns = [

]

urlpatterns += router.urls