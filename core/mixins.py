from django.conf import settings
from django.http.response import JsonResponse
from io import StringIO, BytesIO
from xhtml2pdf import pisa
from html import escape
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse



class FormAjaxMixin(object):
    def form_invalid(self, form):
        return JsonResponse({"success": False, "message": "Datos incorrectos", "erros": form.errors})
