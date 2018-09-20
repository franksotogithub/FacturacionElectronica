from django.shortcuts import render
from datetime import datetime
#from django.conf import settings
from datetime import datetime
from ..models import Usuario , ComprobanteCab , ComprobanteDet ,EstadoDocumento ,ResumenCab ,ResumenDet
    #FacturaElectronica ,\

from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import  UsuarioSerializer , ComprobanteCabSerializer\
    , ComprobanteDetSerializer , EstadoDocumentoSerializer, ResumenCabSerializer, ResumenDetSerializer
from ..utils import RenderPdfMixin ,enviar_mail ,volver_generar_resumen
from django.views.generic import TemplateView
from django.db.models import Count, Max, Case, When, Sum , F
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
    #@action(methods=['get'], url_path='descargar-pdf/(?P<serie>[a-zA-Z0-9\_]+)/(?P<num>[a-zA-Z0-9\_]+)/(?P<tipo>[a-zA-Z0-9\_]+)', detail=False)
    @action(methods=['get'],
            url_path='descargar-pdf/(?P<nom_archivo>[a-zA-Z0-9\_-]+)',
            detail=False)
    def descargarPdf(self,request,nom_archivo):
        #cab = ComprobanteCab.objects.get(cfnumser=serie, cfnumdoc=num, tipodoc_comprobante=tipo)
        #path ='{}-{}-{}-{}.pdf'.format(cab.ruc_emisor,tipo,serie,num)
        path = '{}.pdf'.format(nom_archivo)
        file_path = os.path.join(settings.MEDIA_ROOT_FILES_PDF, path)
        #file_path = os.path.join(settings.MEDIA_ROOT_FILES_PDF, path)
        if nom_archivo is not None:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/pdf")
                    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                    return response
            raise Http404
        else:
            raise Http404
    #@action(methods=['get'], url_path='descargar-xml/(?P<serie>[a-zA-Z0-9\_]+)/(?P<num>[a-zA-Z0-9\_]+)/(?P<tipo>[a-zA-Z0-9\_]+)', detail=False)
    @action(methods=['get'],
            url_path='descargar-xml/(?P<nom_archivo>[a-zA-Z0-9\_-]+)',
            detail=False)
    #def descargarXml(self,request,nom):
    def descargarXml(self, request,nom_archivo):
        #nom_archivo=request.GET.get('nomArchivo',None)
        #cab = ComprobanteCab.objects.get(cfnumser=serie, cfnumdoc=num, tipodoc_comprobante=tipo)
        #path = '{}-{}-{}-{}.xml'.format(cab.ruc_emisor, tipo, serie, num)
        #path = '{}-{}-{}-{}.zip'.format(cab.ruc_emisor, tipo, serie, num)
        #path = 'R-{}.zip'.format(nom_archivo)
        if nom_archivo is not None:
            path = 'R-{}.xml'.format(nom_archivo)
            file_path = os.path.join(settings.MEDIA_ROOT_FILES_XML_RPTA, path)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    #response = HttpResponse(fh.read(), content_type="application/zip")
                    response = HttpResponse(fh.read(), content_type="application/xml")
                    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                    return response
            raise Http404
        else:
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
        fechaIni = request.GET['fechaIni']
        fechaFin = request.GET['fechaFin']
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
            kwargs['estado_comprobante__id'] = estado

        if fechaIni !='':
            kwargs['cffecdoc__gte'] = fechaIni

        if fechaFin != '':
            kwargs['cffecdoc__lte'] = fechaFin

            #kwargs['cffecdoc__lte'] = datetime.strftime(fecha,'%Y-%m-%d')

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
                filtros['cffecdoc'] = datetime.strftime(fecdoc,'%Y-%m-%d')
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

class EstadoViewSet(ViewSet):
    def list(self,request):
        estados=EstadoDocumento.objects.all()
        serializer= EstadoDocumentoSerializer(estados,many=True)
        return Response(serializer.data)

class ResumenViewSet(ViewSet):
    queryset =ResumenCab.objects.all()

    def list(self,request):
        serializer= ResumenCabSerializer(self.queryset[:200],many=True)
        return Response(serializer.data)

    @action(methods=['get'],url_path='listar_detalle', detail=False)
    def listar_detalle(self,request):
        serializer= ResumenDetSerializer(ResumenDet.objects.all()[:200],many=True)
        return Response(serializer.data)


    @action(methods=['get'],url_path='listar', detail=False)
    def listarCabResumenesPaginado(self,request):

        draw = request.GET['draw']
        start = int(request.GET['start'])
        length = int(request.GET['length'])
        fecha_ini =request.GET['fechaIni']
        fecha_fin = request.GET['fechaFin']
        nomdoc_resumen =request.GET['nomdocResumen']
        estado_resumen = request.GET['estado']
        tipo_resumen=request.GET['tipoResumen']

        kwargs={}

        if nomdoc_resumen !=''  and nomdoc_resumen is not None:
            kwargs['nom_archivo__contains']=nomdoc_resumen

        if estado_resumen !='' and estado_resumen is not None:
            kwargs['estado_resumen'] = estado_resumen


        if fecha_ini !='' and fecha_ini is not None:
            kwargs['fecha_gen__gte'] = fecha_ini


        if fecha_fin != '' and fecha_fin is not  None:
            kwargs['fecha_gen__lte'] = fecha_fin

        if tipo_resumen!='' and tipo_resumen is not None:
            kwargs['tipo_resumen'] = tipo_resumen



        datos_filter = self.queryset.filter(**kwargs)
        datos=datos_filter.annotate(estado=F('estado_resumen__nombre')).values('fecha_gen','numser_resumen','numdoc_resumen','nro_reg','estado','estado_resumen_id','id','tipo_resumen').order_by('-fecha_gen')[start:start + length]
        filtered_count =datos_filter.count()

        return Response({
            "draw": draw,
            "recordsTotal": filtered_count,
            "recordsFiltered": filtered_count,
            "data": datos,
        })


    @action(methods=['post'], url_path='detalle', detail=False)
    def detalle(self, request):
            filtros={}
            numser = request.data.get('numser')
            numdoc = request.data.get('numdoc')
            tipo_resumen = request.data.get('tipoResumen')

            filtros['numser_resumen'] =numser

            filtros['numdoc_resumen'] = numdoc

            filtros['tipo_resumen']=tipo_resumen


            resumenCab = self.queryset.filter(**filtros)
            datos = resumenCab.annotate(estado=F('estado_resumen__nombre')).values('fecha_gen', 'numser_resumen',
                                                                                     'numdoc_resumen', 'nro_reg',
                                                                                     'estado','nom_archivo')[0]

            resumenDet = ResumenDet.objects.filter(**filtros)

            datosDet = resumenDet.annotate(tipodoc=F('tipodoc_item__descripcion') , tipdoc_identidad=F('tipdoc_receptor__abrev')).values( 'tipodoc',
                    'numserie_item' ,
                    'numdoc_item'  ,
                    'tipdoc_identidad' ,
                    'nrodoc_receptor' ,
                    'importe_total_venta'  ,
                    'estado','motivo_baja')

            return Response({'cabecera':datos,'detalle':datosDet })


    @action(methods=['post'], url_path='generar_resumen', detail=False)
    def generar_resumen(self,request):
        numser = request.data.get('numser')
        numdoc = request.data.get('numdoc')
        tipo_resumen = request.data.get('tipoResumen')

        try:

            doc=volver_generar_resumen(numser,numdoc,tipo_resumen)
            return Response({'success':True,'data':doc})
        except:
            return Response({'success':False})
