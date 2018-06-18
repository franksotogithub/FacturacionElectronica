import  json
from  facturacion.models import FacturaElectronica
from facturacion.api.serializers import FacturaElectronicaSerializer
from facturacion.utils import genera_facturas_electronicas ,enviar_mail ,export_json
from django.conf import settings


#def export_json():
#    factura_electronica= FacturaElectronica.objects.all()
#    serializer=FacturaElectronicaSerializer(factura_electronica,many=True)
#    with open(ruc+'-'+cc+'-'+serie+'-'+n_comprobate+'.CAB','w') as outfile:
#        json.dump(serializer.data,outfile)

def run():
    export_json('000010000000001')
    name_file=genera_facturas_electronicas('000010000000001','pdf/factura.html')
    enviar_mail(name_file)



