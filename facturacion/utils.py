
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
from .models import FacturaElectronica , DetalleFacturaElectronica
from facturacion.api.serializers import FacturaElectronicaSerializer , DetalleFacturaElectronicaSerializer
from PIL import Image, ImageDraw, ImageFont
import  json
from django.core.mail import send_mail , EmailMessage


ruc = settings.RUC

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
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)

        if directory is None:
            filepath = os.path.join(settings.MEDIA_ROOT, file)
        else:
            filedir = os.path.join(settings.MEDIA_ROOT, directory)
            if not os.path.exists(filedir):
                os.makedirs(filedir)
            filepath = os.path.join(filedir, file)

        with open(filepath, 'wb') as pdf:
            pdf.write(result.getvalue())

def genera_facturas_electronicas(idComprobante,template_name):
    #try:
        cabecera = FacturaElectronica.objects.get(idComprobante=idComprobante)
        detalle=DetalleFacturaElectronica.objects.filter(idComprobante=idComprobante)
        context = {}
        context['fecha'] = datetime.now().date()
        cab_serializer=FacturaElectronicaSerializer(cabecera,many=False)
        det_serializer = DetalleFacturaElectronicaSerializer(detalle, many=True)
        context['cab'] = cab_serializer.data
        context['datos'] = det_serializer.data


        print('cabecera-->', cab_serializer.data)
        cc=cabecera.codComprobante_id
        serie= cabecera.serieComprobante
        n_comprobante = cabecera.numComprobante
        file = ruc + '-' + cc + '-' + serie + '-' + n_comprobante + '.pdf'
        directory= cabecera.numDocUsuario

        genera_pdf(file, template_name, context)
        return file
    #except Exception:

    #    return None

def enviar_mail(name_file):
    message = EmailMessage('prueba', 'prueba para alex de envio de correo con archivo adjunto.', settings.EMAIL_HOST_USER,
              to=['franksoto2012@gmail.com','puntocom.alex@gmail.com'])

    filepath = os.path.join(settings.MEDIA_ROOT, name_file)
    file = open(filepath, "rb")
    message.attach(name_file, file.read(), 'application/pdf')
    message.send()
    file.close()
    #send_mail('prueba', 'prueba para alex de envio de correo con archivo adjunto.', settings.EMAIL_HOST_USER,
    #          ['franksoto2012@gmail.com'], fail_silently=False)

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

def export_json(idComprobante):
    cabecera = FacturaElectronica.objects.get(idComprobante=idComprobante)
    detalle = DetalleFacturaElectronica.objects.filter(idComprobante=idComprobante)
    cabserializer=FacturaElectronicaSerializer(cabecera,many=False)
    detserializer= DetalleFacturaElectronicaSerializer(detalle,many=True)

    cc = cabecera.codComprobante_id
    serie = cabecera.serieComprobante
    n_comprobante = cabecera.numComprobante



    file_cab = ruc + '-' + cc + '-' + serie + '-' + n_comprobante + '.CAB'
    file_det = ruc + '-' + cc + '-' + serie + '-' + n_comprobante + '.DET'
    data_cab = cabserializer.data
    data_det = detserializer.data

    genera_json(file_cab,data_cab)
    genera_json(file_det, data_det)
