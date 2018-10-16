from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from core.decorators import logged ,permission
from django.utils.decorators import method_decorator
# Create your views here.

class DatosView(TemplateView):
    template_name = 'herramientas/datos.html'
    @method_decorator(permission)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=403)