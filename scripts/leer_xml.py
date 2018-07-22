import  json
from facturacion.utils import leer_xml_respuesta , leer_xml_envio ,genera_pdf_facturas_electronicas
from facturacion.models import ComprobanteCab



def run():

    comprobantes = ComprobanteCab.objects.filter(estado_comprobante='POR ENVIAR',
                                                 tipodoc_comprobante__in=('01', '03')).order_by('-cffecdoc')[:100]



    for comprobate in comprobantes:
        ruc = comprobate.ruc_emisor
        nombre=ruc+'-'+comprobate.tipodoc_comprobante+'-'+comprobate.cfnumser+'-'+ comprobate.cfnumdoc
        xml_envio=nombre+'.xml'
        codigo=leer_xml_envio(xml_envio)
        datos={}

        if codigo!='':
            ComprobanteCab.objects.filter(cfnumser=comprobate.cfnumser, cfnumdoc=comprobate.cfnumdoc,
                                          tipodoc_comprobante=comprobate.tipodoc_comprobante).update(
                estado_comprobante='ENVIADO')



