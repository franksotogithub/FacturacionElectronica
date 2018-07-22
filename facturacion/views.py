from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'

class FacturasView(TemplateView):
    template_name = 'facturacion/facturas.html'


class ConsultarComprobanteView(TemplateView):
    template_name = 'facturacion/consultar_comprobante_cliente.html'

class BoletasView(TemplateView):
    template_name = 'facturacion/boletas.html'

class NotasCreditoView(TemplateView):
    template_name = 'facturacion/notas_credito.html'