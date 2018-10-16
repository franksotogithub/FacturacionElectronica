from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from core.decorators import logged ,permission
from django.utils.decorators import method_decorator
# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'

class FacturasView(TemplateView):
    template_name = 'facturacion/facturas.html'
    @method_decorator(permission)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=403)

class ConsultarComprobanteView(TemplateView):
    template_name = 'facturacion/consultar_comprobante_cliente.html'
    #@method_decorator(permission)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=403)

class BoletasView(TemplateView):
    template_name = 'facturacion/boletas.html'
    @method_decorator(permission)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=403)

class NotasCreditoView(TemplateView):
    template_name = 'facturacion/notas_credito.html'
    @method_decorator(permission)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=403)

