from django.shortcuts import render
from datetime import datetime
#from django.conf import settings
from ..models import FacturaElectronica
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from .serializers import FacturaElectronicaSerializer
from ..utils import RenderPdfMixin
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
# Create your views here.

class FacturaElectronicaViewSet(ViewSet):
    def list(self,request):
        facturas=FacturaElectronica.objects.all()
        serializer= FacturaElectronicaSerializer(facturas,many=True)
        return Response(serializer.data)

class ExportarFacturaElectronicaView(RenderPdfMixin ,TemplateView):
    template_name = 'pdf/factura.html'
    #serializer_class = FacturaElectronicaSerializer
    #queryset = FacturaElectronica.objects.all()
    def get_context_data(self, **kwargs):
        #codigo = self.kwargs.get('codigo')
        #factura=get_object_or_404()
        facturas = FacturaElectronica.objects.all()
        context = super(ExportarFacturaElectronicaView, self).get_context_data(**kwargs)
        context['fecha'] = datetime.now().date()
        context['datos'] = facturas
        return context
