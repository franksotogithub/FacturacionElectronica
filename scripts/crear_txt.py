import  json
from facturacion.utils import generar_txt_comprobantes_electronicos ,genera_pdf_facturas_electronicas
from facturacion.models import ComprobanteCab


def run():
    comprobantes=ComprobanteCab.objects.filter(estado_comprobante='POR ENVIAR',tipodoc_comprobante__in=('01','03')).order_by('-cffecdoc')[:5]
    for comprobate in comprobantes:
        generar_txt_comprobantes_electronicos(comprobate.cfnumser, comprobate.cfnumdoc, comprobate.tipodoc_comprobante)




