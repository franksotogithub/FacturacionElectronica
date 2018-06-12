
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
from PIL import Image, ImageDraw, ImageFont



def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    #context = Context(context_dict)
    print(context_dict)
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

