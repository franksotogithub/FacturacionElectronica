import  json
from facturacion.utils import generar_txt_comprobantes_electronicos ,genera_pdf_facturas_electronicas ,leer_xml_envio
from facturacion.models import ComprobanteCab



def run():
    comprobantes=ComprobanteCab.objects.filter(estado_comprobante='ENVIADO',tipodoc_comprobante__in=('01','03','07','08')).order_by('-cffecdoc')[:200]

    for comprobate in comprobantes:
        ruc = comprobate.ruc_emisor
        nombre=ruc+'-'+comprobate.tipodoc_comprobante+'-'+comprobate.cfnumser+'-'+ comprobate.cfnumdoc
        xml_envio=nombre+'.xml'
        codigo=leer_xml_envio(xml_envio)
        datos={}
        datos['cfnumser'] = comprobate.cfnumser
        datos['cfnumdoc'] = comprobate.cfnumdoc
        datos['tipodoc_comprobante'] = comprobate.tipodoc_comprobante
        datos['codigo'] = codigo
        genera_pdf_facturas_electronicas(datos, 'pdf/factura.html')

