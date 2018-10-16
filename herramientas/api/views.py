from django.shortcuts import render
from datetime import datetime

from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import  ProcesoSerializer

from django.views.generic import TemplateView
from django.db.models import Count, Max, Case, When, Sum , F
from django.shortcuts import get_object_or_404 ,Http404
import os
from django.conf import settings
from django.http import HttpResponse
from herramientas.models import Proceso
from herramientas.tasks import generar_tareas_task

class ProcesoViewSet(ModelViewSet):
    queryset = Proceso.objects.all()
    serializer_class = ProcesoSerializer

    @action(methods=['post'], url_path='ejecutar_proceso', detail=False)
    def ejecutar_proceso(self,request):
        procesos = request.data.get('procesos')
        #try:
        generar_tareas_task.delay(procesos)
        return Response({"success":True})
        #except Exception:
            #return Response({"success": False})

        #try:
        #    if tipo=='comprobantes':
        #        migrar_comprobantes()
        #    elif tipo=='resumenComprobantes':
        #        migrar_resumenes_comprobantes()
        #    elif tipo=='resumenAnulados':
        #        migrar_resumenes_anulados()
        #    elif tipo=='exportarSunat':
        #        exportar_sunat()
        #    elif tipo=='actualizarEstados':
        #        actualizar_estados()
#
        #    return Response({'status': True})
#
        #except:
        #    return Response({'status': False})


