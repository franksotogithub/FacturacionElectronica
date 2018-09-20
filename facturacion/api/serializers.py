from rest_framework import serializers
from ..models import Usuario, ComprobanteCab ,ComprobanteDet ,EstadoDocumento,ResumenCab,ResumenDet

from rest_framework.fields import ChoiceField


class ChoicesSerializerField(serializers.SerializerMethodField):
    """
    A read-only field that return the representation of a model field with choices.
    """

    def to_representation(self, value):
        # sample: 'get_XXXX_display'
        method_name = 'get_{field_name}_display'.format(field_name=self.field_name)
        # retrieve instance method
        method = getattr(value, method_name)
        # finally use instance method to return result of get_XXXX_display()
        return method()

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields='__all__'

#class DetalleFacturaElectronicaSerializer(serializers.ModelSerializer):
#    class Meta:
#        model =DetalleFacturaElectronica
#        fields= '__all__'
#
#class FacturaElectronicaSerializer(serializers.ModelSerializer):
#
#    class Meta:
#        model = FacturaElectronica
#        fields=('idComprobante','serieComprobante','numComprobante','numDocUsuario','fecEmision','sumDsctoGlobal','mtoImpVenta','rznSocialUsuario')
#
#
#class FacturaElectronicaDetalleSerializer(serializers.ModelSerializer):
#    detalles=DetalleFacturaElectronicaSerializer(many=True, read_only=True)
#    class Meta:
#        model = FacturaElectronica
#        fields=('idComprobante','serieComprobante','numComprobante','numDocUsuario','fecEmision','sumDsctoGlobal','mtoImpVenta','rznSocialUsuario','detalles')


#class ComprobanteCabSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = ComprobanteCab
#        fields = '__all__'

class EstadoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoDocumento
        fields ='__all__'

class ComprobanteCabSerializer(serializers.ModelSerializer):
    raz_social_emisor = serializers.CharField( max_length=100)  # Field name made lowercase.
    nom_comercial_emisor = serializers.CharField( max_length=100)
    cffecdoc = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    estado_comprobante = serializers.CharField(max_length=100, read_only=True)  # Field name made lowercase.
#    estado_comprobante = serializers.RelatedField(source='nombre', read_only=True)  # Field name made lowercase.
    class Meta:
        model = ComprobanteCab
        fields ='__all__'




    #cffecdoc = serializers.DateTimeField(format="%Y-%m-%d")  # Field name made lowercase.
    #raz_social_emisor = serializers.CharField( max_length=100)  # Field name made lowercase.
    #nom_comercial_emisor = serializers.CharField( max_length=100)
    #ubigeo_emisor = serializers.CharField( max_length=6)  # Field name made lowercase.
    #direccion_emisor = serializers.CharField( max_length=100)  # Field name made lowercase.
    #urbanizacion_emisor = serializers.CharField( max_length=25)  # Field name made lowercase.
    #provincia_emisor = serializers.CharField( max_length=30)  # Field name made lowercase.
    #departamento_emisor = serializers.CharField( max_length=30)  # Field name made lowercase.
    #distrito_emisor = serializers.CharField( max_length=30)  # Field name made lowercase.
    #pais_emisor = serializers.CharField( max_length=2)  # Field name made lowercase.
    #ruc_emisor = serializers.CharField( max_length=11)  # Field name made lowercase.
    #tip_doc_emisor = serializers.CharField( max_length=1)  # Field name made lowercase.
    #serie_nc_nd = serializers.CharField(max_length=4)  # Field name made lowercase.
    #nro_compr_nc_nd = serializers.CharField( max_length=8)  # Field name made lowercase.
    #tip_nc_nd = serializers.CharField( max_length=2)  # Field name made lowercase.
    #motivo_nc_nd = serializers.CharField( max_length=250)  # Field name made lowercase.
    #tip_doc_modif_nc_nd = serializers.CharField( max_length=2)  # Field name made lowercase.
    #tipodoc_comprobante = serializers.CharField( max_length=2)  # Field name made lowercase.
    #cfnumser = serializers.CharField( max_length=4)  # Field name made lowercase.
    #cfnumdoc = serializers.CharField( max_length=8)  # Field name made lowercase.
    #tip_doc_receptor = serializers.CharField( max_length=1)  # Field name made lowercase.
    #nro_doc_receptor = serializers.CharField( max_length=15)  # Field name made lowercase.
    #cfcodcli = serializers.CharField( max_length=11)  # Field name made lowercase.
    #cfnombre = serializers.CharField( max_length=100)  # Field name made lowercase.
    #direccion_receptor = serializers.CharField( max_length=100)  # Field name made lowercase.
    #tvv_cod_ope_gravadas = serializers.CharField( max_length=4)  # Field name made lowercase.
    #tvv_imp_ope_gravadas = serializers.DecimalField( max_digits=12,decimal_places=2)  # Field name made lowercase.
    #tvv_cod_ope_inafectas = serializers.CharField( max_length=4)  # Field name made lowercase.
    #tvv_imp_ope_inafectas = serializers.DecimalField( max_digits=12,decimal_places=2)  # Field name made lowercase.
    #tvv_cod_ope_exoneradas = serializers.CharField( max_length=4)  # Field name made lowercase.
    #tvv_imp_ope_exoneradas = serializers.DecimalField( max_digits=12,decimal_places=2)  # Field name made lowercase.
    #sumatoria_igv = serializers.DecimalField( max_digits=12,decimal_places=2)  # Field name made lowercase.
    #cod_tributo_igv = serializers.CharField( max_length=4)  # Field name made lowercase.
    #nom_tributo_igv = serializers.CharField( max_length=6)  # Field name made lowercase.
    #cod_inter_igv = serializers.CharField( max_length=3)  # Field name made lowercase.
    #sumatoria_isc = serializers.DecimalField( max_digits=12,decimal_places=2)  # Field name made lowercase.
    #cod_tributo_isc = serializers.CharField( max_length=4)  # Field name made lowercase.
    #nom_tributo_isc = serializers.CharField(max_length=6)  # Field name made lowercase.
    #cod_inter_isc = serializers.CharField( max_length=3)  # Field name made lowercase.
    #sumatoria_otros_trib = serializers.DecimalField( max_digits=12,decimal_places=2)  # Field name made lowercase.
    #cod_tributo_otros_trib = serializers.CharField( max_length=4)  # Field name made lowercase.
    #nom_tributo_otros_trib = serializers.CharField( max_length=6)  # Field name made lowercase.
    #cod_inter_otros_trib = serializers.CharField( max_length=3)  # Field name made lowercase.
    #sumatoria_otros_cargos = serializers.DecimalField( max_digits=12,decimal_places=2)  # Field name made lowercase.
    #cod_tip_dsctos = serializers.CharField( max_length=4)  # Field name made lowercase.
    #importe_dsctos = serializers.DecimalField( max_digits=12,decimal_places=2)  # Field name made lowercase.
    #importe_total_venta = serializers.DecimalField( max_digits=12,  decimal_places=2)  # Field name made lowercase.
    #serie_guia = serializers.CharField( max_length=4)  # Field name made lowercase.
    #nro_guia = serializers.CharField( max_length=8)  # Field name made lowercase.
    #cod_tipo_guia = serializers.CharField( max_length=2)  # Field name made lowercase.
    #serie_otro_refe = serializers.CharField( max_length=4)  # Field name made lowercase.
    #nro_otro_refe = serializers.CharField( max_length=8)  # Field name made lowercase.
    #cod_tipo_refe = serializers.CharField( max_length=2)  # Field name made lowercase.
    #cod_percepcion = serializers.CharField( max_length=4)  # Field name made lowercase.
    #baseimponible_percepcion = serializers.DecimalField( max_digits=12,decimal_places=2)  # Field name made lowercase.
    #monto_percepcion = serializers.DecimalField( max_digits=12,decimal_places=2)  # Field name made lowercase.
    #totalcobrado_percepcion = serializers.DecimalField(max_digits=12,decimal_places=2)  # Field name made lowercase.
    #ubl_version = serializers.CharField( max_length=10)  # Field name made lowercase.
    #estruc_version = serializers.CharField( max_length=10)  # Field name made lowercase.
    #tvv_cod_ope_gratuitas = serializers.CharField( max_length=4)  # Field name made lowercase.
    #tvv_imp_ope_gratuitas = serializers.DecimalField( max_digits=15,decimal_places=2)  # Field name made lowercase.
    #descuentos_globales = serializers.DecimalField( max_digits=12,decimal_places=2)  # Field name made lowercase.
    #estado_comprobante = serializers.RelatedField(source='nombre', read_only=True)  # Field name made lowercase.
    #moneda = serializers.CharField(max_length=3)  # Field name made lowercase.
    #cdr = serializers.CharField(max_length=50)  # Field name made lowercase.
    #cod_resumen = serializers.CharField(max_length=20)  # Field name made lowercase.
    #cod_baja = serializers.CharField( max_length=20)  # Field name made lowercase.
    #ruta_comprobante = serializers.CharField( max_length=4000)  # Field name made lowercase.
    #ruta_cdr = serializers.CharField( max_length=4000)  # Field name made lowercase.
    #tipo_envio = serializers.CharField( max_length=10)  # Field name made lowercase.
    #correo = serializers.CharField( max_length=100, )  # Field name made lowercase.
    #leyenda = serializers.CharField( max_length=250, )  # Field name made lowercase.
    #glosa_electronica = serializers.CharField( max_length=250)  # Field name made lowercase.
    #cod_cat_detraccion = serializers.CharField( max_length=5)  # Field name made lowercase.
    #porcentaje_detraccion = serializers.CharField( max_length=18)  # Field name made lowercase.
    #monto_detraccion = serializers.DecimalField( max_digits=12, decimal_places=2)  # Field name made lowercase.
    #valor_referencial_detraccion = serializers.DecimalField( max_digits=12,decimal_places=2)  # Field name made lowercase.
    #cod_cat_bbss_detraccion = serializers.CharField( max_length=5)  # Field name made lowercase.
    #codigo_bbss_detraccion = serializers.CharField(max_length=5)  # Field name made lowercase.
    #cod_cat_cta_bn_detraccion = serializers.CharField( max_length=5)  # Field name made lowercase.
    #cta_bn_detraccion = serializers.CharField( max_length=15)  # Field name made lowercase.
    #total_anticipo = serializers.DecimalField( max_digits=15,decimal_places=2)  # Field name made lowercase.
    #tipo_operacion = serializers.CharField(max_length=3)  # Field name made lowercase.
    #estado_correo = serializers.CharField( max_length=50)  # Field name made lowercase.
    #ordencompra = serializers.CharField( max_length=20)  # Field name made lowercase.
    #usuario = serializers.CharField( max_length=20, )  # Field name made lowercase.
    #codigopventa = serializers.CharField( max_length=20)  # Field name made lowercase.
    #placa = serializers.CharField( max_length=50, )  # Field name made lowercase.
    #xml = serializers.CharField(max_length=250,)  # Field name made lowercase.
    #ubigeo_pventa = serializers.CharField( max_length=12)  # Field name made lowercase.
    #direccion_pventa = serializers.CharField( max_length=200)  # Field name made lowercase.
    #urbanizacion_pventa = serializers.CharField( max_length=50)  # Field name made lowercase.
    #provincia_pventa = serializers.CharField( max_length=60)  # Field name made lowercase.
    #departamento_pventa = serializers.CharField( max_length=60)  # Field name made lowercase.
    #distrito_pventa = serializers.CharField( max_length=60)  # Field name made lowercase.
    #pais_pventa = serializers.CharField( max_length=2)  # Field name made lowercase.

class ComprobanteDetSerializer(serializers.Serializer):

    dfnumser = serializers.CharField( max_length=4)  # Field name made lowercase.
    dfnumdoc = serializers.CharField( max_length=8)  # Field name made lowercase.
    tipodoc_comprobante = serializers.CharField( max_length=2)  # Field name made lowercase.
    orden_item = serializers.IntegerField()  # Field name made lowercase.
    um_item = serializers.CharField( max_length=6)  # Field name made lowercase.
    cant_item = serializers.DecimalField(max_digits=18, decimal_places=2)  # Field name made lowercase.
    nom_item = serializers.CharField( max_length=250, )  # Field name made lowercase.
    vu_item = serializers.DecimalField( max_digits=12, decimal_places=2)  # Field name made lowercase.
    imp_vu_item = serializers.DecimalField( max_digits=12, decimal_places=2)  # Field name made lowercase.
    cod_vu_item = serializers.CharField( max_length=2, )  # Field name made lowercase.
    monto_igv = serializers.DecimalField( max_digits=12, decimal_places=2)  # Field name made lowercase.
    afec_igv = serializers.CharField( max_length=2, )  # Field name made lowercase.
    cod_igv = serializers.CharField( max_length=4, )  # Field name made lowercase.
    nom_igv = serializers.CharField( max_length=6, )  # Field name made lowercase.
    cinter_igv = serializers.CharField( max_length=3, )  # Field name made lowercase.
    monto_isc = serializers.DecimalField( max_digits=12, decimal_places=2)  # Field name made lowercase.
    afec_isc = serializers.CharField( max_length=2, )  # Field name made lowercase.
    cod_isc = serializers.CharField( max_length=4, )  # Field name made lowercase.
    nom_isc = serializers.CharField( max_length=6, )  # Field name made lowercase.
    cinter_isc = serializers.CharField( max_length=3, )  # Field name made lowercase.
    tvu_item = serializers.DecimalField( max_digits=12, decimal_places=2)  # Field name made lowercase.
    cod_item = serializers.CharField( max_length=30, )  # Field name made lowercase.
    importe_nooneroso_item = serializers.DecimalField( max_digits=12, decimal_places=2)  # Field name made lowercase.
    cod_nooneroso_item = serializers.CharField( max_length=2, )  # Field name made lowercase.
    false_item = serializers.CharField( max_length=5, )  # Field name made lowercase.
    des_item = serializers.DecimalField( max_digits=12, decimal_places=2)  # Field name made lowercase.
    imp_total_item = serializers.DecimalField( max_digits=12, decimal_places=2, ) # Field name made lowercase.

    #class Meta:
    #    model = ComprobanteDet
    #    fields = '__all__'


class ResumenCabSerializer(serializers.ModelSerializer):
    tipo_resumen = serializers.SerializerMethodField()
    #estado_resumen = serializers.CharField(max_length=100, read_only=True)  # Field name made lowercase.

    class Meta:
        model= ResumenCab
        fields = ('__all__')
    def get_tipo_resumen(self,obj):
        return obj.get_tipo_resumen_display()

class ResumenDetSerializer(serializers.ModelSerializer):
    #nro_reg = serializers.SerializerMethodField('get_nro_reg')

    class Meta:
        model= ResumenDet
        fields = '__all__'