
import os

from io import StringIO, BytesIO
from datetime import datetime
from django.db.models import Sum
from xhtml2pdf import pisa
from html import escape
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from .models import ComprobanteCab , ComprobanteDet ,ComprobanteBaja
from facturacion.api.serializers import ComprobanteCabSerializer , ComprobanteDetSerializer

from PIL import Image, ImageDraw, ImageFont
import  json
from django.core.mail import send_mail , EmailMessage
from xml.dom import minidom
#import xml.etree.ElementTree as ET
import lxml.etree as  etree
import pyqrcode
ruc = settings.RUC

NAMESPACES={
    'schemaLocation':r'urn:oasis:names:specification:ubl:schema:xsd:Invoice-2',
    'ar' :'urn:oasis:names:specification:ubl:schema:xsd:ApplicationResponse-2',
    'cac':'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2' ,
    'cbc':"urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
    'ext':"urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2",
     'ds':"http://www.w3.org/2000/09/xmldsig#",
    'sac':"urn:sunat:names:specification:ubl:peru:schema:xsd:SunatAggregateComponents-1",
}

def template_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    #context = Context(context_dict)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(StringIO(html), result, encoding='utf-8')
    if not pdf.err:
        return result
    else:
        return False

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    #context = Context(context_dict)

    html = template.render(context_dict)
    result = BytesIO()
    kw = {'leftMargin': 0, 'rightMargin': 0, 'topMargin': 0, 'bottomMargin': 0}
    pdf = pisa.pisaDocument(StringIO(html), result, encoding='utf-8', **kw)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse("Error: <pre>%s</pre>" % escape(html))

class RenderPdfMixin(object):
    def render_to_response(self, context, **response_kwargs):
        return render_to_pdf(self.template_name, context)

def genera_pdf(file, template_name, context, directory=None):
    result = template_to_pdf(template_name, context)
    if result:
        if not os.path.exists(settings.MEDIA_ROOT_FILES_PDF):
            os.makedirs(settings.MEDIA_ROOT_FILES_PDF)

        if directory is None:
            filepath = os.path.join(settings.MEDIA_ROOT_FILES_PDF, file)
        else:
            filedir = os.path.join(settings.MEDIA_ROOT_FILES_PDF, directory)
            if not os.path.exists(filedir):
                os.makedirs(filedir)
            filepath = os.path.join(filedir, file)

        with open(filepath, 'wb') as pdf:
            pdf.write(result.getvalue())

def genera_qr_code(tipo,serie,num,cab):
    path_code_png = os.path.join(settings.MEDIA_ROOT, '{}-{}-{}.png'.format(tipo, serie, num))

    #ruc=cab.ruc_emisor
    ruc = '10452575014'

    if (tipo in ('01', '03')):
        data=ruc+'|'+\
             isNone(cab.tipodoc_comprobante,'')+'|'+\
             isNone(cab.cfnumser,'')+'|'+\
             isNone(cab.cfnumdoc,'')+'|'+ \
             isNone(cab.sumatoria_igv, '') + '|' + \
             isNone(cab.importe_total_venta, '')+'|'+\
             isNone( "{:%Y-%m-%d }".format(cab.cffecdoc)               ,'')+'|'+\
             isNone(cab.tip_doc_receptor           ,'')+'|'+\
             isNone(cab.cfcodcli                 ,'')
    code = pyqrcode.create(data, error = 'Q',encoding='utf-8')
    code.png(path_code_png, scale=5)
    return path_code_png


def genera_pdf_facturas_electronicas(datos,template_name):
    serie=datos['cfnumser']
    num = datos['cfnumdoc']
    tipo = datos['tipodoc_comprobante']
    codigo=datos['codigo']


    cab = ComprobanteCab.objects.get(cfnumser=serie, cfnumdoc=num, tipodoc_comprobante=tipo)
    det = ComprobanteDet.objects.filter(dfnumser=serie, dfnumdoc=num, tipodoc_comprobante=tipo).order_by('orden_item')
    serializerCab = ComprobanteCabSerializer(cab, many=False)
    serializerDets = ComprobanteDetSerializer(det, many=True)
    path_code_png=genera_qr_code(tipo, serie, num, cab)


    context = {}
    context['cab']=serializerCab.data
    context['detalles'] = serializerDets.data
    context['img']= settings.MEDIA_ROOT_IMG
    context['qr_code']=path_code_png
    file= cab.ruc_emisor+'-'+cab.tipodoc_comprobante+'-'+cab.cfnumser+'-'+cab.cfnumdoc+'.pdf'

    genera_pdf(file, template_name, context)

    return file



def enviar_mail(name_file,destino):

    message = EmailMessage('prueba', 'prueba para alex de envio de correo con archivo adjunto.', settings.EMAIL_HOST_USER,
              to=[destino])

    filepath_zip = os.path.join(settings.MEDIA_ROOT_FILES_XML_R,'{}.zip'.format( name_file))
    filepath_pdf = os.path.join(settings.MEDIA_ROOT_FILES_PDF, '{}.pdf'(name_file))
    file = open(filepath_zip, "rb")
    message.attach(name_file, file.read(), 'application/zip')
    file = open(filepath_pdf, "rb")
    message.attach(name_file, file.read(), 'application/pdf')
    message.send()
    file.close()


def genera_json(file,data,directory=None):
    if not os.path.exists(settings.FILES_JSON):
        os.makedirs(settings.FILES_JSON)


    if directory is None:
        filepath = os.path.join(settings.FILES_JSON, file)
    else:
        filedir = os.path.join(settings.FILES_JSON, directory)
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        filepath = os.path.join(filedir, file)

    with open(filepath, 'w') as outfile:
        json.dump(data, outfile)

def genera_txt(file,data,directory=None):
    if not os.path.exists(settings.MEDIA_ROOT_FILES_TXT):
        os.makedirs(settings.MEDIA_ROOT_FILES_TXT)

    if directory is None:
        filepath = os.path.join(settings.MEDIA_ROOT_FILES_TXT, file)
    else:
        filedir = os.path.join(settings.MEDIA_ROOT_FILES_TXT, directory)
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        filepath = os.path.join(filedir, file)

    with open(filepath, 'w') as outfile:
        outfile.write(data)

def isNone(data,replace):
    if data is None:
        return str(replace)
    else:
        return str(data).strip()


def generar_txt_comprobantes_electronicos(serie, num, tipo):

    cab = ComprobanteCab.objects.get(cfnumser=serie, cfnumdoc=num, tipodoc_comprobante=tipo)
    comprobanteDet = ComprobanteDet.objects.filter(dfnumser=serie, dfnumdoc=num, tipodoc_comprobante=tipo)

    data_cab = ''
    data_det = ''
    ruc=cab.ruc_emisor
    #ruc = '10452575014'

    if (tipo in ('01', '03')):
        file_cab=ruc+'-'+cab.tipodoc_comprobante+'-'+cab.cfnumser+'-'+cab.cfnumdoc+'.CAB'
        data_cab=isNone(cab.tipo_operacion  ,'')+'|'+\
        isNone( "{:%Y-%m-%d }".format(cab.cffecdoc)               ,'')+'|'+\
        isNone(cab.codigopventa             ,'')+'|'+\
        isNone(cab.tip_doc_emisor           ,'')+'|'+\
        isNone(cab.cfcodcli                 ,'')+'|'+\
        isNone(cab.cfnombre                 ,'')+'|'+\
        isNone(cab.moneda                   ,'')+'|'+\
        isNone(cab.descuentos_globales      ,'')+'|'+\
        isNone(cab.sumatoria_otros_cargos   ,'')+'|'+\
        isNone(cab.importe_dsctos           ,'')+'|'+\
        isNone(cab.tvv_imp_ope_gravadas     ,'')+'|'+\
        isNone(cab.tvv_imp_ope_inafectas     ,'')+'|'+\
        isNone(cab.tvv_imp_ope_exoneradas   ,'')+'|'+\
        isNone(cab.sumatoria_igv            ,'')+'|'+\
        isNone(cab.sumatoria_isc            ,'')+'|'+\
        isNone(cab.sumatoria_otros_trib     ,'')+'|'+\
        isNone(cab.importe_total_venta      ,'')

        file_det=ruc+'-'+cab.tipodoc_comprobante+'-'+cab.cfnumser+'-'+cab.cfnumdoc+'.DET'

        for d in  comprobanteDet:
            data_det +=isNone(d.um_item,'')+'|'+\
            isNone(d.cant_item,'')+'|'+\
            isNone(d.cod_item,'')+'|'+\
            isNone('','')+'|'+\
            isNone(d.nom_item,'')+'|'+\
            isNone(d.vu_item,'')+'|'+\
            isNone(d.des_item,'')+'|'+\
            isNone(d.monto_igv,'')+'|'+\
            isNone(d.afec_igv,'')+'|'+\
            isNone(d.monto_isc,'')+'|'+\
            isNone(d.cod_isc,'')+'|'+\
            isNone(d.imp_vu_item,'')+'|'+\
            isNone(d.tvu_item,'')+'\n'

    elif (tipo in ('07','08')):
        file_cab = ruc + '-' + cab.tipodoc_comprobante + '-' + cab.cfnumser + '-' + cab.cfnumdoc + '.NOT'
        data_cab = isNone("{:%Y-%m-%d }".format(cab.cffecdoc), '') + '|' + \
                   isNone(cab.tip_nc_nd, '') + '|' + \
                   isNone(cab.motivo_nc_nd, '') + '|' + \
                   isNone(cab.tip_doc_nc_nd, '') + '|' + \
                   isNone(cab.tip_doc_emisor, '') + '|' + \
                   isNone(cab.cfcodcli, '') + '|' + \
                   isNone(cab.cfnombre, '') + '|' + \
                   isNone(cab.moneda, '') + '|' + \
                   isNone(cab.sumatoria_otros_cargos, '') + '|' + \
                   isNone(cab.tvv_imp_ope_gravadas, '') + '|' + \
                   isNone(cab.tvv_imp_ope_inafectas, '') + '|' + \
                   isNone(cab.tvv_cod_ope_exoneradas, '') + '|' + \
                   isNone(cab.sumatoria_igv, '') + '|' + \
                   isNone(cab.sumatoria_isc, '') + '|' + \
                   isNone(cab.sumatoria_otros_trib, '') + '|' + \
                   isNone(cab.importe_total_venta, '')

        file_det = ruc + '-' + cab.tipodoc_comprobante + '-' + cab.cfnumser + '-' + cab.cfnumdoc + '.DET'

        for d in comprobanteDet:
            data_det += isNone(d.um_item, '') + '|' + \
                        isNone(d.cant_item, '') + '|' + \
                        isNone(d.cod_item, '') + '|' + \
                        isNone('', '') + '|' + \
                        isNone(d.nom_item, '') + '|' + \
                        isNone(d.vu_item, '') + '|' + \
                        isNone(d.des_item, '') + '|' + \
                        isNone(d.monto_igv, '') + '|' + \
                        isNone(d.afec_igv, '') + '|' + \
                        isNone(d.monto_isc, '') + '|' + \
                        isNone(d.cod_isc, '') + '|' + \
                        isNone(d.imp_vu_item, '') + '|' + \
                        isNone(d.tvu_item, '') + '\n'

    genera_txt(file_cab,data_cab)
    genera_txt(file_det, data_det)

def generar_txt_baja(serie, num, tipo,corr):
    baja = ComprobanteBaja.objects.get(serie_doc=serie, numero_doc=num, tipo_doc=tipo)
    file_baja=baja.ruc_emisor+'-RA-'+"{:%YYYY%mm%dd }".format(datetime.datetime.now().date())+'-'+corr+'.CBA'
    data_baja=isNone( "{:%Y-%m-%d }".format(baja.fecha_doc),'')+'|'+ \
              isNone("{:%Y-%m-%d }".format(datetime.datetime.now().date()), '') + '|' + \
              isNone(baja.tipo_doc,'')+'|'+\
              isNone("{}-{}".format(baja.serie_doc,baja.numero_doc)           ,'')+'|'+\
              isNone(baja.motivo_baja,'')+'|'
    genera_txt(file_baja, data_baja)


def leer_xml_respuesta(file):

    if not os.path.exists(settings.MEDIA_ROOT_FILES_XML_R):
        os.makedirs(settings.MEDIA_ROOT_FILES_XML_R)

    filepath = os.path.join(settings.MEDIA_ROOT_FILES_XML_R, file)
    tree = etree.parse(filepath)
    respuesta = tree.xpath('.//cbc:Description', namespaces=NAMESPACES)
    for el in respuesta:
        print(el.text)

def leer_xml_envio(file):

    if not os.path.exists(settings.MEDIA_ROOT_FILES_XML_FIRMA):
        os.makedirs(settings.MEDIA_ROOT_FILES_XML_FIRMA)


    filepath = os.path.join(settings.MEDIA_ROOT_FILES_XML_FIRMA, file)
    if not os.path.exists(filepath):
        print('no existe documento')
        return ''

    else:
        recovering_parser = etree.XMLParser(recover=True)
        tree = etree.parse(filepath, parser=recovering_parser)


        #respuesta = tree.xpath('.//ds:X509Certificate', namespaces=NAMESPACES)
        digest_value = tree.xpath('.//ds:DigestValue', namespaces=NAMESPACES)[0]
        print(digest_value.text)
        return digest_value.text





