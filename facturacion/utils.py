from decimal import *
import os ,zipfile

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
from .models import ComprobanteCab , ComprobanteDet ,ComprobanteBaja , Catalogo05TiposTributos ,\
    Catalogo15ElementosAdicionales , ResumenDet, ResumenCab ,EstadoDocumento

from herramientas.models import Proceso

from facturacion.api.serializers import ComprobanteCabSerializer , ComprobanteDetSerializer

from PIL import Image, ImageDraw, ImageFont
import  json
from django.core.mail import send_mail , EmailMessage
from xml.dom import minidom
#import xml.etree.ElementTree as ET
import lxml.etree as  etree
import pyqrcode
from django.db import IntegrityError, transaction
from django.db.models import F, Sum,Min,Q,Max
from django.db.models.functions import Concat
from sunat.models import Documento
from num2words.currency import parse_currency_parts, prefix_currency
from num2words import num2words
from django.db import connection


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
    #ruc = '10452575014'
    data=''
    if (tipo in ('01', '03','07')):
        data=cab.ruc_emisor+'|'+\
             isNone(cab.tipodoc_comprobante_id,'')+'|'+\
             isNone(cab.cfnumser,'')+'|'+\
             isNone(cab.cfnumdoc,'')+'|'+ \
             isNone(cab.sumatoria_igv, '') + '|' + \
             isNone(cab.importe_total_venta, '')+'|'+\
             isNone( "{:%Y-%m-%d }".format(cab.cffecdoc)               ,'')+'|'+\
             isNone(cab.tip_doc_receptor           ,'')+'|'+\
             isNone(cab.cfcodcli                 ,'')

    print("data>>>",data)
    code = pyqrcode.create(data, error = 'Q',encoding='utf-8')
    code.png(path_code_png, scale=5)
    return path_code_png


def genera_pdf_facturas_electronicas(datos,template_name):
    serie=datos['cfnumser']
    num = datos['cfnumdoc']
    tipo = datos['tipodoc_comprobante']
    #codigo=datos['codigo']


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
    file= cab.nom_archivo+'.pdf'

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
    if data is None or str(data).strip(' ')=='':
        return replace

    else:
        return str(data)


def isNoneNumerico(data, replace):
    if data is None:
        return replace

    else:
        return data

def generar_txt_comprobantes_electronicos(serie, num, tipo):

    cab = ComprobanteCab.objects.get(cfnumser=serie, cfnumdoc=num, tipodoc_comprobante=tipo)
    comprobanteDet = ComprobanteDet.objects.filter(dfnumser=serie, dfnumdoc=num, tipodoc_comprobante=tipo)
    tri =Catalogo05TiposTributos.objects.get(codigo=cab.cod_tributo_igv)

    nom_archivo=''
    data_cab = ''
    data_det = ''
    ruc=cab.ruc_emisor
    nom_archivo=ruc + '-' + tipo + '-' + serie + '-' + num

    imp_total_venta = isNoneNumerico(cab.sumatoria_igv, Decimal('0.0')) + isNoneNumerico(cab.tvv_imp_ope_gravadas,
                                                                                         Decimal(
                                                                                             '0.0')) - isNoneNumerico(
        cab.sumatoria_descuentos, Decimal('0.0')) + isNoneNumerico(cab.sumatoria_otros_cargos,
                                                                   Decimal('0.0')) - isNoneNumerico(
        cab.total_anticipo, Decimal('0.0'))

    if (tipo in ('01','03')):
        file_cab=  nom_archivo+'.CAB'


        data_cab=isNone(cab.tipo_operacion  ,'')+'|'+\
                isNone( "{:%Y-%m-%d}".format(cab.cffecdoc),'')+'|'+ \
                isNone("{:%H:%M:%S}".format(cab.cffecdoc), '') + '|'+("{:%Y-%m-%d}".format(cab.cffecven) if cab.cffecven is  not None else '-' ) + '|'
        data_cab += isNone(cab.codigopventa             ,'')+'|'+\
        isNone(cab.tip_doc_receptor ,'')+'|'+\
        isNone(cab.cfcodcli                 ,'')+'|'+\
        isNone(cab.cfnombre                 ,'')+'|'+\
        isNone(cab.moneda                   ,'')+'|'+\
        isNone(cab.sumatoria_igv            ,'0.0')+'|'+ \
        isNone(cab.tvv_imp_ope_gravadas     ,'0.0')+'|'+ \
        isNone(cab.sumatoria_igv + cab.tvv_imp_ope_gravadas,'0.0')+'|'+ \
        isNone(cab.sumatoria_descuentos   ,'0.0')+'|'+\
        isNone(cab.sumatoria_otros_cargos, '0.0') + '|' + \
        isNone(cab.total_anticipo, '0.0') + '|' + \
        isNone( imp_total_venta , '0.0') + '|'+\
        isNone(cab.ubl_version  ,'2.1') +  '|' +\
        isNone(cab.customizacion, '2.0') + '|'

    elif (tipo in ('07','08')):
        file_cab =        nom_archivo + '.NOT'

        data_cab=isNone(cab.tipo_operacion  ,'')+'|'+\
        isNone( "{:%Y-%m-%d}".format(cab.cffecdoc),'')+'|'+ \
        isNone("{:%H:%M:%S}".format(cab.cffecdoc), '') + '|' + \
        isNone(cab.codigopventa             ,'')+'|'+\
        isNone(cab.tip_doc_receptor           ,'')+'|'+\
        isNone(cab.cfcodcli                 ,'')+'|'+\
        isNone(cab.cfnombre                 ,'')+'|'+\
        isNone(cab.moneda                   ,'')+'|'+ \
        isNone(cab.tip_nc_nd, '') + '|' + \
        isNone(cab.motivo_nc_nd, '') + '|' + \
        isNone(cab.tip_doc_modif_nc_nd, '') + '|' + \
        isNone(cab.serie_nc_nd, '') +'-' +isNone(cab.nro_compr_nc_nd, '')+ '|' + \
        isNone(cab.sumatoria_igv            ,'0.0')+'|'+ \
        isNone(cab.tvv_imp_ope_gravadas     ,'0.0')+'|'+ \
        isNone(cab.sumatoria_igv + cab.tvv_imp_ope_gravadas,'0.0')+'|'+ \
        isNone(cab.sumatoria_descuentos   ,'0.0')+'|'+\
        isNone(cab.sumatoria_otros_cargos, '0.0') + '|' + \
        isNone(cab.total_anticipo, '0.0') + '|' + \
        isNone( imp_total_venta , '0.0') + '|' +\
        isNone(cab.ubl_version  ,'2.1') +  '|' +\
        isNone(cab.customizacion, '2.0') + '|'

    file_det = nom_archivo + '.DET'
    for d in comprobanteDet:
        data_det += isNone(d.um_item, '') + '|' + \
                    isNone(d.cant_item, '') + '|' + \
                    isNone(d.cod_item, '') + '|' + \
                    isNone('-', '-') + '|' + \
                    isNone(d.nom_item, '') + '|' + \
                    isNone(d.vu_item, '') + '|'
        #Sumatoria Tributos por item
        data_det += isNone(d.monto_igv+d.monto_isc, '') + '|'
        ######IGV
        data_det += isNone(d.cod_igv, '') + '|' + \
                    isNone(d.monto_igv, '') + '|' + \
                    isNone(d.tvu_item, '') + '|' + \
                    isNone(d.nom_igv, '') + '|' + \
                    isNone(d.cinter_igv, '') + '|' + \
                    isNone(d.afec_igv, '') + '|' + \
                    isNone(d.porcent_igv, ComprobanteDet.PORCENT_IGV) + '|'
        ############isc###
        data_det += isNone('-', '-') + '|' + \
                    isNone('', '') + '|' + \
                    isNone('', '') + '|' + \
                    isNone('', '') + '|' + \
                    isNone('', '') + '|' + \
                    isNone('', '') + '|' + \
                    isNone('', '') + '|'
        ##########otro tributo
        data_det += isNone('-', '-') + '|' + \
                    isNone('', '') + '|' + \
                    isNone('', '') + '|' + \
                    isNone('', '') + '|' + \
                    isNone('', '') + '|' + \
                    isNone('', '') + '|'

        data_det += isNone(d.imp_total_item, '') + '|' + \
                    isNone(d.tvu_item, '') + '|' + \
                    isNone('0', '-') + '|'+'\n'

    file_aca=nom_archivo + '.ACA'
    data_aca='-|-|0.0|0.0|-|-|'+cab.direccion_receptor+'|-|-|-|'



    file_tri = nom_archivo+ '.TRI'
    data_tri = tri.codigo+'|' + tri.name+'|'+tri.un_ece_5153 +'|'+isNone(cab.tvv_imp_ope_gravadas,'0.0')+'|'+isNone(cab.sumatoria_igv,'0.0')+'|'

    file_ley = nom_archivo + '.LEY'
    data_ley = '1000' + '|' + isNone(cab.leyenda ,actualizar_leyendas(imp_total_venta,cab.moneda,'Y'))+'|'




    genera_txt(file_cab,data_cab)
    genera_txt(file_det, data_det)
    genera_txt(file_tri, data_tri)
    genera_txt(file_ley, data_ley)
    #genera_txt(file_aca, data_aca)

    return nom_archivo

def generar_txt_resumenes_anulaciones():
    resumen_detalle = ResumenDet.objects.filter(tipo_resumen=ResumenCab.RESUMEN_ANULACION,
                                                numdoc_resumen__isnull=True)
    list_ids = resumen_detalle.values_list('pk', flat=True)

    serie = "{:%Y%m%d}".format(datetime.now().date())
    cant_res_gen = ResumenCab.objects.filter(tipo_resumen=ResumenCab.RESUMEN_ANULACION, numser_resumen=serie).count()

    r = resumen_detalle[0]
    res = ResumenCab(ruc_emisor=r.ruc_emisor, tipo_resumen=r.tipo_resumen, fecha_gen=datetime.now().date(),
                     estado_resumen_id=ComprobanteCab.POR_GENERAR_DOCUMENTO,
                     numdoc_resumen=str(cant_res_gen + 1).zfill(3), numser_resumen=serie)

    res.save()
    ResumenDet.objects.filter(pk__in=list(list_ids)).update(resumen_cab=res)

    file = res.ruc_emisor + '-' + res.tipo_resumen + '-' + res.numser_resumen + '-' + res.numdoc_resumen + '.CBA'

    det = ''
    for r in resumen_detalle:

        det +=isNone("{:%Y-%m-%d}".format(r.fecdoc_item),'') + '|'
        det += isNone("{:%Y-%m-%d}".format(res.fecha_gen), '') + '|'
        det += isNone(r.tipodoc_item, '') + '|'
        det += isNone(r.numserie_item+'-'+r.numdoc_item, '') + '|'
        det += isNone(r.motivo_baja, '') + '|'+'\n'


    genera_txt(file, det)
    res.nom_archivo=res.ruc_emisor + '-' + res.tipo_resumen + '-' + res.numser_resumen+'-'+res.numdoc_resumen
    res.estado_resumen_id = ComprobanteCab.DOCUMENTO_GENERADO
    res.save()

def generar_txt_resumenes(tipo_resumen):

    resumenes=ResumenCab.objects.filter(tipo_resumen=tipo_resumen, estado_resumen_id=ComprobanteCab.POR_GENERAR_DOCUMENTO)
    for res in resumenes:
        resultado   = generar_resumen(res.numser_resumen,res.numdoc_resumen,tipo_resumen)
        nom_archivo = resultado['nom_archivo']
        #try:
        doc_sunat = Documento.objects.get(nom_arch=nom_archivo)
        doc_sunat.ind_situ = ComprobanteCab.DOCUMENTO_GENERADO
        #if tipo_resumen==ResumenCab.RESUMEN_COMPROBANTE:
        #    ComprobanteCab.objects.filter(cod_resumen=res.id).update(nom_archivo='{}-{}-{}-{}'.format(F('ruc_emisor'),F('tipodoc_comprobante'),F('cfnumser'),F('cfnumdoc')) )
        doc_sunat.save()
        #except:
            #continue




def generar_resumen(serie,num_doc,tipo_resumen):
    res = ResumenCab.objects.get(tipo_resumen=tipo_resumen, numdoc_resumen=num_doc,
                                           numser_resumen=serie)
    resumen_detalle = ResumenDet.objects.filter(tipo_resumen=tipo_resumen, numdoc_resumen=num_doc,
                                           numser_resumen=serie)

    #ComprobanteCab.objects.filter(cod_resumen=res.id).update(
    #    nom_archivo='{}-{}-{}-{}'.format(F('ruc_emisor'), F('tipodoc_comprobante'), F('cfnumser'), F('cfnumdoc')))
    #print('cantidad de comprobantes>>>', ComprobanteCab.objects.filter(cod_resumen=res.id).count())



    if (tipo_resumen==ResumenCab.RESUMEN_COMPROBANTE):

        file = res.ruc_emisor + '-' + res.tipo_resumen + '-' + res.numser_resumen + '-' + res.numdoc_resumen + '.RDI'
        det = ''
        for r in resumen_detalle:
            det += isNone("{:%Y-%m-%d}".format(r.fecdoc_item), '') + '|'
            det += isNone("{:%Y-%m-%d}".format(r.fecdoc_item), '') + '|'
            det += isNone(r.tipodoc_item_id, '') + '|'
            det += isNone(r.numserie_item + '-' + r.numdoc_item, '') + '|'
            det += isNone(r.tipdoc_receptor, '0') + '|'
            det += isNone(r.nrodoc_receptor, '-') + '|'
            det += isNone(r.moneda, '') + '|'
            det += isNone(r.tvv_imp_ope_gravadas, '0.0') + '|'
            det += isNone(r.tvv_imp_ope_exoneradas, '0.0') + '|'
            det += isNone(r.tvv_imp_ope_inafectas, '0.0') + '|'
            det += isNone(r.tvv_imp_ope_gratuitas, '0.0') + '|'
            det += isNone(r.imp_total_sum_otros_cargos, '0.0') + '|'
            det += isNone(r.monto_isc, '0.0') + '|'
            det += isNone(r.monto_igv, '0.0') + '|'
            det += isNone(r.monto_otros_trib, '0.0') + '|'
            det += isNone(r.importe_total_venta, '0.0') + '|'
            det += isNone(r.tipodoc_modif, '') + '|'
            det += isNone(r.numserie_modif, '') + '|'
            det += isNone(r.numdoc_modif, '') + '|'
            det += isNone(r.regimen_percepcion, '') + '|'
            det += isNone(r.porcent_percepcion, '') + '|'
            det += isNone(r.base_imponible_percepcion, '') + '|'
            det += isNone(r.monto_percepcion, '') + '|'
            det += isNone(r.monto_percepcion, '') + '|'
            det += isNone(r.estado, '1') + '|' + '\n'

    else:
        file = res.ruc_emisor + '-' + res.tipo_resumen + '-' + res.numser_resumen + '-' + res.numdoc_resumen + '.CBA'
        det = ''
        for r in resumen_detalle:
            det += isNone("{:%Y-%m-%d}".format(r.fecdoc_item), '') + '|'
            det += isNone("{:%Y-%m-%d}".format(res.fecha_gen), '') + '|'
            det += isNone(r.tipodoc_item_id, '') + '|'
            det += isNone(r.numserie_item + '-' + r.numdoc_item, '') + '|'
            det += isNone(r.motivo_baja, '') + '|' + '\n'


    genera_txt(file, det)
    res.nom_archivo = res.ruc_emisor + '-' + res.tipo_resumen + '-' + res.numser_resumen + '-' + res.numdoc_resumen
    res.estado_resumen_id = ComprobanteCab.DOCUMENTO_GENERADO
    res.save()

    res=ResumenCab.objects.filter(tipo_resumen=tipo_resumen, numdoc_resumen=num_doc,
                                           numser_resumen=serie)

    return res.annotate(estado=F('estado_resumen__nombre')).values('fecha_gen', 'numser_resumen',
                                                            'numdoc_resumen', 'nro_reg',
                                                            'estado', 'nom_archivo', 'estado_resumen_id')[0]

def volver_generar_resumen(serie,num_doc,tipo_resumen):
    resumenCab=ResumenCab.objects.filter(tipo_resumen=tipo_resumen,numdoc_resumen=num_doc,
                                             numser_resumen=serie)
    resumenDet=ResumenDet.objects.filter(tipo_resumen=tipo_resumen,numdoc_resumen=num_doc,
                                             numser_resumen=serie)
    cab = ResumenCab.objects.filter(tipo_resumen=tipo_resumen,numser_resumen=serie).aggregate(max_res_fen=Max('numdoc_resumen'))
    cant_res_gen=int(cab['max_res_fen'])
    nuevo_num_doc_resumen=str(cant_res_gen+1).zfill(3)
    nuevo_serie = "{:%Y%m%d}".format(datetime.now().date())
    resumenCab.update(numdoc_resumen=nuevo_num_doc_resumen,estado_resumen_id=ComprobanteCab.DOCUMENTO_GENERADO,fecha_gen=datetime.now().date())
    resumenDet.update(numdoc_resumen=nuevo_num_doc_resumen)
    #resumenCab.update(numdoc_resumen=nuevo_num_doc_resumen,estado_resumen_id=ComprobanteCab.DOCUMENTO_GENERADO,numser_resumen=nuevo_serie,fecha_gen=datetime.now().date())
    #resumenDet.update(numdoc_resumen=nuevo_num_doc_resumen,numser_resumen=nuevo_serie)
    #return generar_resumen(nuevo_serie, nuevo_num_doc_resumen, tipo_resumen)
    return generar_resumen(serie, nuevo_num_doc_resumen, tipo_resumen)

def actualizar_comprobantes_detalle_resumen(serie,num_doc,tipo_resumen,estado):

    resumenDet=ResumenDet.objects.filter(tipo_resumen=tipo_resumen,numdoc_resumen=num_doc,
                                             numser_resumen=serie)#.values('tipodoc_item','numserie_item','numdoc_resumen')


    for r in resumenDet:
        ComprobanteCab.objects.filter(cfnumser=r.numserie_item,cfnumdoc=r.numdoc_item,tipodoc_comprobante=r.tipodoc_item).update(estado_comprobante_id=estado)



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


def unzip_rpta_xml():
    dir_name=settings.MEDIA_ROOT_FILES_XML_RPTA
    extension='.zip'
    for item in os.listdir(dir_name):
        if item.endswith(extension):
            file_name= os.path.join(dir_name,item)
            zip_ref = zipfile.ZipFile(file_name)
            zip_ref.extractall(dir_name)
            zip_ref.close()



def actualizar_leyendas(monto,moneda,separador):
    MONEDAS = {
        'PEN': 'soles',
        'USD': 'dolares americanos',
    }

    leyenda=''
    try:
        left,rigth,is_negative=parse_currency_parts(monto,is_int_with_cents=False)

        if left>0:
            leyenda='{} {}'.format(  num2words(left,lang='es'),separador)
        cent= '{}/100 {}'.format(rigth,MONEDAS[moneda])
        leyenda='{} {}'.format(leyenda,cent)
        return leyenda.upper()

    except NotImplementedError:
        return  ''


URL_SUNAT='http://localhost:9000'
URL_REQUEST_GENERAR_PDF=URL_SUNAT+'/api/MostrarXml.htm'
HEADERS = {'content-type': 'application/json'}
def actualizar_estado_comprobantes():
    comprobantes=ComprobanteCab.objects.filter(nom_archivo__isnull=False)
    for com in comprobantes:
        nom_arch =com.nom_archivo #.ruc_emisor+'-'+com.tipodoc_comprobante_id+'-'+com.cfnumser+'-'+com.cfnumdoc

        try:
            doc_sunat = Documento.objects.get(nom_arch=nom_arch)
            com.estado_comprobante_id=doc_sunat.ind_situ
            com.save()
        except:
            continue

def actualizar_estado_resumenes():
    resumenes=ResumenCab.objects.filter(nom_archivo__isnull=False)
    print(resumenes)
    for res in resumenes:
        nom_arch=res.nom_archivo
        #nom_arch =res.ruc_emisor+'-'+res.tipodoc_comprobante_id+'-'+res.cfnumser+'-'+res.cfnumdoc
        #try:
        doc_sunat = Documento.objects.get(nom_arch=nom_arch)
        res.estado_resumen_id=doc_sunat.ind_situ
        res.save()

        comp=ComprobanteCab.objects.filter(cod_resumen=res.id)

        comp.update(estado_comprobante=doc_sunat.ind_situ)
        print('cantidad de comprobantes>>>',comp.count())
        #except:
        #    continue


TEMPLATES={
    '01':'pdf/factura.html',
    '03':'pdf/boleta.html',
    '07':'pdf/nota_credito.html',
}



def generar_pdf():
    #comprobantes = ComprobanteCab.objects.filter(estado_comprobante__id=ComprobanteCab.DOCUMENTO_APROBADO,estado_pdf=ComprobanteCab.POR_GENERAR_PDF,tipodoc_comprobante__in=('01','07','08')).order_by('cffecdoc')

    comprobantes = ComprobanteCab.objects.filter(
        Q(tipodoc_comprobante__codigo='01') | (Q(tipodoc_comprobante__codigo='07')  ) |Q(tipodoc_comprobante__codigo='03') ,
        estado_comprobante=ComprobanteCab.DOCUMENTO_APROBADO).order_by('-cffecdoc')
    for com in comprobantes:
            #nom_arch = com.nom_archivo
            nom_arch = com.ruc_emisor+'-'+com.tipodoc_comprobante_id+'-'+com.cfnumser+'-'+com.cfnumdoc
        #try:
            xml_envio=nom_arch+'.xml'
            #codigo=leer_xml_envio(xml_envio)
            datos={}
            datos['cfnumser'] = com.cfnumser
            datos['cfnumdoc'] = com.cfnumdoc
            datos['tipodoc_comprobante'] = com.tipodoc_comprobante_id
            #datos['codigo'] = codigo

            #print('datas>>',datos)
            genera_pdf_facturas_electronicas(datos, TEMPLATES[com.tipodoc_comprobante_id])
            com.estado_pdf=ComprobanteCab.GENERARO_PDF
            com.save()


def crear_txt_comprobantes():
    # comprobantes = ComprobanteCab.objects.filter(estado_comprobante=ComprobanteCab.POR_GENERAR_DOCUMENTO,tipodoc_comprobante__codigo__in=('01','07','08') ).order_by('-cffecdoc')
    comprobantes = ComprobanteCab.objects.filter(
        Q(tipodoc_comprobante__codigo='01') | (Q(tipodoc_comprobante__codigo='07') & Q(tip_nc_nd='01')),
        estado_comprobante=ComprobanteCab.POR_GENERAR_DOCUMENTO).order_by('-cffecdoc')


    for com in comprobantes:
        # try:

        nom_archivo = generar_txt_comprobantes_electronicos(com.cfnumser, com.cfnumdoc, com.tipodoc_comprobante_id)
        com.nom_archivo = nom_archivo
        com.estado_comprobante_id = ComprobanteCab.DOCUMENTO_GENERADO
        com.save()
        print('comprobantes>>>', nom_archivo)
        try:
            doc_sunat = Documento.objects.get(nom_arch=nom_archivo)
            doc_sunat.ind_situ = ComprobanteCab.DOCUMENTO_GENERADO
            doc_sunat.save()

        except:
            continue

def actualizar_estado_tarea(id,estado):
    proceso = Proceso.objects.get(pk=id)
    proceso.estado = estado

    if proceso.estado == 'PROCESANDO':
        proceso.fecha_ini = datetime.now()
    else:
        proceso.fecha_fin = datetime.now()
    proceso.save()


def migrar_comprobantes():
    sql_result = 'EXEC migrar_comprobantes'
    cursor = connection.cursor()
    cursor.execute(sql_result)
    connection.commit()
    connection.close()
#crear_txt_comprobantes()

def migrar_resumenes_comprobantes():

    sql_result = 'EXEC migrar_resumenes_comprobantes'
    cursor = connection.cursor()
    cursor.execute(sql_result)
    connection.commit()
    connection.close()

    #generar_txt_resumenes(ResumenCab.RESUMEN_COMPROBANTE)

def migrar_resumenes_anulados():
    sql_result = 'EXEC migrar_resumenes_anulados'
    cursor = connection.cursor()
    cursor.execute(sql_result)
    connection.commit()
    connection.close()
    #generar_txt_resumenes(ResumenCab.RESUMEN_ANULACION)

def exportar_sunat():
    crear_txt_comprobantes()
    generar_txt_resumenes(ResumenCab.RESUMEN_COMPROBANTE)
    generar_txt_resumenes(ResumenCab.RESUMEN_ANULACION)


def actualizar_estados():
    actualizar_estado_comprobantes()
    actualizar_estado_resumenes()
    generar_pdf()
    #unzip_rpta_xml()

#def actualizar_configuracion():






