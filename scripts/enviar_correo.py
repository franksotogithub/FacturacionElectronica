import  json
from facturacion.utils import enviar_mail
from facturacion.models import ComprobanteCab



def run():
    comprobantes=ComprobanteCab.objects.filter(estado_comprobante='ENVIADO',correo__isnull=False,estado_correo='PENDIENTE',tipodoc_comprobante__in=('01','03','07','08'))

    for comprobante in comprobantes:
        if comprobante.correo!='':
            name_file=comprobante.ruc_emisor+'-'+comprobante.tipodoc_comprobante+'-'+comprobante.cfnumser+'-'+comprobante.cfnumdoc
            destino=comprobante.correo
            enviar_mail(name_file,destino)



