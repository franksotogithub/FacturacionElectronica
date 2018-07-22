from django.shortcuts import render
from datetime import datetime
#from django.conf import settings
from datetime import datetime
from ..models import Usuario , ComprobanteCab , ComprobanteDet
    #FacturaElectronica ,\

from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import  UsuarioSerializer , ComprobanteCabSerializer\
    , ComprobanteDetSerializer
from ..utils import RenderPdfMixin ,enviar_mail
from django.views.generic import TemplateView

from django.shortcuts import get_object_or_404 ,Http404
import os
from django.conf import settings
from django.http import HttpResponse



class UsuarioViewSet(ViewSet):
    def list(self,request):
        usuarios=Usuario.objects.all()
        serializer=UsuarioSerializer (usuarios,many=True)
        return Response(serializer.data)

class DescargarViewSet(ViewSet):
    @action(methods=['get'], url_path='descargar-pdf/(?P<serie>[a-zA-Z0-9\_]+)/(?P<num>[a-zA-Z0-9\_]+)/(?P<tipo>[a-zA-Z0-9\_]+)', detail=False)
    def descargarPdf(self,request,serie,num,tipo):
        cab = ComprobanteCab.objects.get(cfnumser=serie, cfnumdoc=num, tipodoc_comprobante=tipo)
        path ='{}-{}-{}-{}.pdf'.format(cab.ruc_emisor,tipo,serie,num)
        file_path = os.path.join(settings.MEDIA_ROOT_FILES_PDF, path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/pdf")
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                return response
        raise Http404

    @action(methods=['get'], url_path='descargar-xml/(?P<serie>[a-zA-Z0-9\_]+)/(?P<num>[a-zA-Z0-9\_]+)/(?P<tipo>[a-zA-Z0-9\_]+)', detail=False)
    def descargarXml(self,request,serie,num,tipo):
        cab = ComprobanteCab.objects.get(cfnumser=serie, cfnumdoc=num, tipodoc_comprobante=tipo)
        #path = '{}-{}-{}-{}.xml'.format(cab.ruc_emisor, tipo, serie, num)
        path = '{}-{}-{}-{}.zip'.format(cab.ruc_emisor, tipo, serie, num)
        file_path = os.path.join(settings.MEDIA_ROOT_FILES_XML_R, path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/zip")
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                return response
        raise Http404

    @action(methods=['get'], url_path='enviar-correo/(?P<serie>[a-zA-Z0-9\_]+)/(?P<num>[a-zA-Z0-9\_]+)/(?P<tipo>[a-zA-Z0-9\_]+)', detail=False)
    def enviarCorreo(self,request,serie,num,tipo):
        comprobante = ComprobanteCab.objects.get(cfnumser=serie, cfnumdoc=num, tipodoc_comprobante=tipo)

        if comprobante.estado_comprobante!='ENVIADO':
            return  Response({'status':False,'message':'Comprobante no ha sido Aceptado por Sunat'})

        else:
            if comprobante.correo!='':
                name_file=comprobante.ruc_emisor+'-'+comprobante.tipodoc_comprobante+'-'+comprobante.cfnumser+'-'+comprobante.cfnumdoc
                destino=comprobante.correo
                enviar_mail(name_file,destino)
                return Response({'status': True, 'message': 'Comprobante no ha sido Aceptado por Sunat'})
            else:
                return Response({'status': False, 'message': 'El cliente no tiene correo'})


class ComprobanteViewSet(ViewSet):
    queryset = ComprobanteCab.objects.all()

    def list(self,request):
        serializer= ComprobanteCabSerializer(self.queryset.order_by('cffecdoc')[:200],many=True)
        return Response(serializer.data)

    #@action(methods=['get'], url_path='detalle', detail=False)
    #def buscar(self,request, *args,**kwargs):
    #    filtros = {}
    #    print(**kwargs)

        #codcli = request.GET['cfcodcli']
        #tipdoc_comprobante = request.GET['tipodoc_comprobante']
        #numser = request.GET['cfnumser']
        #numdoc =request.GET['cfnumdoc']
        #fecdoc = request.GET['cffecdoc']
        #importe_total_venta = request.GET['importe_total_venta']



    @action(methods=['get'],url_path='listar', detail=False)
    def listarCabComprobantesPaginado(self,request):
        draw = request.GET['draw']
        start = int(request.GET['start'])
        length = int(request.GET['length'])
        #order_column = int(request.GET['order[0][column]'])
        serie = request.GET['serie']
        numdoc = request.GET['numdoc']
        razonsocial =request.GET['razonsocial']
        tipodoc = request.GET['tipodoc']
        fecha = request.GET['fecha']
        estado = request.GET['estado']
        global_search = request.GET['search[value]']


        kwargs={}

        if serie !='':
            kwargs['cfnumser__contains']=serie

        if numdoc !='':
            kwargs['cfnumdoc__contains']=numdoc

        if razonsocial !='':
            kwargs['cfnombre__contains'] = razonsocial

        if tipodoc !='':
            kwargs['tipodoc_comprobante'] = tipodoc


        if estado!='':
            kwargs['estado_comprobante'] = estado

        if fecha !='':
            kwargs['cffecdoc__lte'] = fecha

        datos_filter = self.queryset.filter(**kwargs)
        datos=datos_filter.order_by('-cffecdoc')[start:start + length]
        serializer=ComprobanteCabSerializer(datos,many=True)
        filtered_count =datos_filter.count()

        return Response({
            "draw": draw,
            "recordsTotal": filtered_count,
            "recordsFiltered": filtered_count,
            "data": serializer.data,
        })



    #@action(methods=['get'], url_path='detalle/(?P<serie>[a-zA-Z0-9\_]+)/(?P<num>[a-zA-Z0-9\_]+)/(?P<tipo>[a-zA-Z0-9\_]+)',detail=False)
    #@action(methods=['get'],url_path='detalle/(?P<tipo>[a-zA-Z0-9\_]+)', detail=False)
    #def detalle(self,request,serie,num,tipo):
    @action(methods=['post'], url_path='detalle', detail=False)
    def detalle(self, request):
        try:
            filtros={}
            codcli = request.data.get('cfcodcli')
            tipodoc_comprobante = request.data.get('tipodoc_comprobante')
            numser = request.data.get('cfnumser')
            numdoc =request.data.get('cfnumdoc')
            fecdoc = request.data.get('cffecdoc')
            importe_total_venta = request.data.get('importe_total_venta')

            if codcli!='' and codcli is not None:
                filtros['cfcodcli']=codcli
            if tipodoc_comprobante!='' and tipodoc_comprobante is not None:
                filtros['tipodoc_comprobante'] = tipodoc_comprobante
            if numser!='' and numser is not None:
                filtros['cfnumser'] = numser
            if numdoc!='' and numdoc is not None:
                filtros['cfnumdoc'] = numdoc
            if fecdoc!='' and fecdoc is not None:
                filtros['cffecdoc'] = fecdoc
            if importe_total_venta!='' and importe_total_venta is not None:
                filtros['importe_total_venta']=importe_total_venta

            print('filtros--->',filtros)

            comprobanteCab = self.queryset.filter(**filtros)[0]

            #comprobanteCab= self.queryset.get(cfnumser=serie,cfnumdoc=numdoc,tipodoc_comprobante=tipdoc_comprobante)
            serializerCab = ComprobanteCabSerializer(comprobanteCab,many=False)
            #comprobanteDet = ComprobanteDet.objects.filter(dfnumser=serie,dfnumdoc=numdoc,tipodoc_comprobante=tipdoc_comprobante)
            comprobanteDet = ComprobanteDet.objects.filter(dfnumser=numser,dfnumdoc=numdoc,tipodoc_comprobante=tipodoc_comprobante)
            serializerDets=ComprobanteDetSerializer(comprobanteDet,many=True)
            return Response({'cabecera':serializerCab.data,'detalle':serializerDets.data })
        except:
            return Response({'status': False})


