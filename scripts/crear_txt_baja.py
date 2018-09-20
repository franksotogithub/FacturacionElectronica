import  json
from facturacion.utils import generar_txt_baja
from facturacion.models import ComprobanteBaja


def run():
    bajas=ComprobanteBaja.objects.filter(estado='PENDIENTE').order_by('id')[:500]
    for corr,baja in enumerate(bajas,1):
        generar_txt_baja(baja.serie_doc,baja.numero_doc,baja.tipo_doc,str(corr).zfill(3))





