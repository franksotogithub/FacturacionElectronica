from django.conf.urls import url
from .views import *

app_name = 'resumenes'
urlpatterns = [
    #url(r'^$', ResumenesComprobanteView.as_view(), name='index'),
    url(r'^resumen_comprobantes/$', ResumenesComprobanteView.as_view(), name='resumenes_comprobantes'),
    url(r'^resumen_anulaciones/$', ResumenesAnulacionesView.as_view(), name='resumenes_anulaciones'),
    #url(r'^resumenes_comprobantes/$', ResumenesComprobanteView.as_view(), name='resumenes_comprobantes'),


    ]