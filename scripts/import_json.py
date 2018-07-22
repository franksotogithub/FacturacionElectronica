import  json
#from  facturacion.models import FacturaElectronica
#from facturacion.api.serializers import FacturaElectronicaSerializer
from facturacion.utils import genera_pdf_facturas_electronicas ,enviar_mail ,export_json
from django.conf import settings


def run():
    export_json('000010000000001')
    name_file=genera_pdf_facturas_electronicas('000010000000001', 'pdf/factura.html')
    enviar_mail(name_file)



