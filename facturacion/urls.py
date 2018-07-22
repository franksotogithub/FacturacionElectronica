from django.conf.urls import url
from .views import *

app_name = 'facturacion'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^facturas/$', FacturasView.as_view(), name='facturas'),
    url(r'^boletas/$', BoletasView.as_view(), name='boletas'),
    url(r'^notas-credito/$', NotasCreditoView.as_view(), name='notas-credito'),
    url(r'^consultar-comprobantes/$', ConsultarComprobanteView.as_view(), name='consultar-comprobantes'),
    ]