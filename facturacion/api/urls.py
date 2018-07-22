from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet ,DescargarViewSet , ComprobanteViewSet
    #FacturaElectronicaViewSet ,ExportarFacturaElectronicaView ,

#from .views import RegistroCajaViewSet, AsignarSupViewSet, UsuariosViewSet, AsignarDigViewSet, LoteAsignacionViewSet, \
#    CerrarDigitacionViewSet, SalidaCajaViewSet, CedulasViewset ,

app_name = 'facturacion'
router = DefaultRouter()
router.register(r'usuarios',UsuarioViewSet ,base_name='facturas')
router.register(r'descargas', DescargarViewSet ,base_name='descargas')
router.register(r'comprobantes', ComprobanteViewSet ,base_name='comprobantes')

#router.register(r'facturas',FacturaElectronicaViewSet ,base_name='facturas')
urlpatterns = [

    #url(r'^export_facturas/$',ExportarFacturaElectronicaView.as_view() , name='export_facturas'),
]

urlpatterns += router.urls