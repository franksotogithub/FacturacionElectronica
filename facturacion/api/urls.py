from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import  FacturaElectronicaViewSet ,ExportarFacturaElectronicaView
#from .views import RegistroCajaViewSet, AsignarSupViewSet, UsuariosViewSet, AsignarDigViewSet, LoteAsignacionViewSet, \
#    CerrarDigitacionViewSet, SalidaCajaViewSet, CedulasViewset

router = DefaultRouter()
router.register(r'facturas',FacturaElectronicaViewSet ,base_name='facturas')
urlpatterns = [
    url(r'^export_facturas/$',ExportarFacturaElectronicaView.as_view() , name='export_facturas'),

]

urlpatterns += router.urls