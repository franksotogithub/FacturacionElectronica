import  json
from facturacion.utils import generar_txt_comprobantes_electronicos ,genera_pdf_facturas_electronicas ,leer_xml_envio ,unzip_rpta_xml
from facturacion.models import ComprobanteCab , ResumenCab ,ResumenDet
from sunat.models import Documento
import requests
import os ,zipfile

URL_SUNAT='http://localhost:9000'
URL_REQUEST_GENERAR_PDF=URL_SUNAT+'/api/MostrarXml.htm'
HEADERS = {'content-type': 'application/json'}
def actualizar_estado_comprobantes():
    comprobantes=ComprobanteCab.objects.filter(nom_archivo__isnull=False)
    for com in comprobantes:
            nom_arch =com.nom_archivo #.ruc_emisor+'-'+com.tipodoc_comprobante_id+'-'+com.cfnumser+'-'+com.cfnumdoc

        #try:
            print(nom_arch)
            doc_sunat = Documento.objects.get(nom_arch=nom_arch)

            com.estado_comprobante_id=doc_sunat.ind_situ
            print(doc_sunat.ind_situ)
            com.save()
        #except:
        #    continue

def actualizar_estado_resumenes():
    resumenes=ResumenCab.objects.filter(nom_archivo__isnull=False)
    for res in resumenes:
        nom_arch=res.nom_archivo
        #nom_arch =res.ruc_emisor+'-'+res.tipodoc_comprobante_id+'-'+res.cfnumser+'-'+res.cfnumdoc
        #try:
        doc_sunat = Documento.objects.get(nom_arch=nom_arch)
        res.estado_resumen_id=doc_sunat.ind_situ
        res.save()
        ComprobanteCab.objects.filter(cod_resumen=res.id).update(estado_comprobante=doc_sunat.ind_situ)
        #except:
        #    continue


TEMPLATES={
    '01':'pdf/factura.html',
    '03':'pdf/boleta.html',
    '07':'pdf/boleta.html',
}




def generar_pdf():
    comprobantes = ComprobanteCab.objects.filter(estado_comprobante__id=ComprobanteCab.DOCUMENTO_APROBADO,estado_pdf=ComprobanteCab.POR_GENERAR_PDF,tipodoc_comprobante__in=('01','07','08')).order_by('cffecdoc')
    for com in comprobantes:
            nom_arch = com.nom_archivo
        #try:
            xml_envio=nom_arch+'.xml'
            codigo=leer_xml_envio(xml_envio)
            datos={}


            datos['cfnumser'] = com.cfnumser
            datos['cfnumdoc'] = com.cfnumdoc
            datos['tipodoc_comprobante'] = com.tipodoc_comprobante_id
            datos['codigo'] = codigo

            print('datas>>',datos)
            genera_pdf_facturas_electronicas(datos, TEMPLATES[com.tipodoc_comprobante_id])
            com.estado_pdf=ComprobanteCab.GENERARO_PDF
            com.save()
        #except:
        #    continue
        #data= json.dumps({"nomArch": nom_arch})
        #r= requests.post(URL_REQUEST_GENERAR_PDF,data=data,headers=HEADERS)


def run():
    actualizar_estado_comprobantes()
    actualizar_estado_resumenes()
    generar_pdf()
    unzip_rpta_xml()


