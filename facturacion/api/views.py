from django.shortcuts import render
from datetime import datetime
#from django.conf import settings
from ..models import FacturaElectronica ,Usuario
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import FacturaElectronicaSerializer , UsuarioSerializer
from ..utils import RenderPdfMixin
from django.views.generic import TemplateView

from django.shortcuts import get_object_or_404

# Create your views here.

class FacturaElectronicaViewSet(ViewSet):
    def list(self,request):
        facturas=FacturaElectronica.objects.all()
        serializer= FacturaElectronicaSerializer(facturas,many=True)
        return Response(serializer.data)
    @action(methods=['get'],url_path='buscar/(?P<usuario>[a-zA-Z0-9\_]+)',detail=False )
    def buscar(self,request,usuario):
        facturas=FacturaElectronica.objects.filter(usuario=usuario)
        serializer=FacturaElectronicaSerializer(facturas,many=True)
        return  Response(serializer.data)




class ExportarFacturaElectronicaView(RenderPdfMixin ,TemplateView):
    template_name = 'pdf/factura.html'

    def get_context_data(self, **kwargs):
        facturas = FacturaElectronica.objects.all()
        context = super(ExportarFacturaElectronicaView, self).get_context_data(**kwargs)
        context['fecha'] = datetime.now().date()
        context['datos'] = facturas
        return context

class UsuarioViewSet(ViewSet):
    def list(self,request):
        usuarios=Usuario.objects.all()
        serializer=UsuarioSerializer (usuarios,many=True)
        return Response(serializer.data)