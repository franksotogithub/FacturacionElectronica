import  json
from  facturacion.models import FacturaElectronica
from facturacion.api.serializers import FacturaElectronicaSerializer

ruc='10452575014'
cc='01'
serie='0001'
n_comprobate='00000001'

def export_json():
    factura_electronica= FacturaElectronica.objects.all()
    serializer=FacturaElectronicaSerializer(factura_electronica,many=True)
    with open(ruc+'-'+cc+'-'+serie+'-'+n_comprobate+'.CAB','w') as outfile:
        json.dump(serializer.data,outfile)

def run():
    export_json()


