from django.conf.urls import url
from .views import LoginView ,CerrarSesionView
app_name = 'usuarios'
urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^cerrar-sesion/$', CerrarSesionView.as_view(), name='cerrar-sesion'),
]