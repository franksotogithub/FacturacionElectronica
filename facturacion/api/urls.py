from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet ,DescargarViewSet , ComprobanteViewSet ,EstadoViewSet,ResumenViewSet,\
    HerramientasViewSet



app_name = 'facturacion'
router = DefaultRouter()
router.register(r'usuarios',UsuarioViewSet ,base_name='usuarios')
router.register(r'descargas', DescargarViewSet ,base_name='descargas')
router.register(r'comprobantes', ComprobanteViewSet ,base_name='comprobantes')
router.register(r'estados', EstadoViewSet ,base_name='estados')
router.register(r'resumenes', ResumenViewSet ,base_name='resumenes')
router.register(r'herramientas', HerramientasViewSet ,base_name='herramientas')

urlpatterns = [

    #url(r'^export_facturas/$',ExportarFacturaElectronicaView.as_view() , name='export_facturas'),
]

urlpatterns += router.urls