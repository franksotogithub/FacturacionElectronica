from django.db import models

# Create your models here.



class Catalogo01TipoDocumento(models.Model):
    codigo = models.CharField(db_column='Codigo', max_length=2, primary_key=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=200, blank=True, null=True)  # Field name made lowercase.
    un_1001 = models.CharField(db_column='UN_1001', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CATALOGO_01_TIPO_DOCUMENTO'
    def __str__(self):
        return self.descripcion

class Catalogo06DocumentoIdentidad(models.Model):
    codigo = models.CharField(db_column='Codigo', max_length=1, primary_key=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=200, blank=True, null=True)  # Field name made lowercase.
    abrev= models.CharField(db_column='ABREV', max_length=10, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'CATALOGO_06_DOCUMENTO_IDENTIDAD'
    def __str__(self):
        return self.descripcion

class EstadoDocumento(models.Model):
    id= models.CharField(db_column='id',  max_length=2,primary_key=True)  # Field name made lowercase.
    nombre= models.CharField(db_column='nombre',  max_length=50,null=True,blank=True)
    class Meta:
        managed = True
        db_table = 'ESTADO_DOCUMENTO'
    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    numDocUsuario = models.CharField(primary_key=True,max_length=15)
    rznSocialUsuario = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()

    def __str__(self):
        return self.rznSocialUsuario

class TipoComprobante ( models.Model):
    idTipoComprobante= models.CharField(primary_key=True, max_length=2)
    descripcion=models.CharField(max_length=30,null=True,blank=True)

    def __str__(self):
        return self.descripcion

class ComprobanteCab(models.Model):
    POR_GENERAR_DOCUMENTO = '00'
    DOCUMENTO_GENERADO = '01'
    DOCUMENTO_APROBADO='03'
    POR_GENERAR_PDF='01'
    GENERARO_PDF='02'

    ESTADO_PDF_CHOICES =(
        (POR_GENERAR_PDF,'POR GENERAR'),
        (GENERARO_PDF,'GENERADO'),
    )


    id = models.AutoField(db_column='ID',primary_key=True)
    cffecdoc = models.DateTimeField(db_column='CFFECDOC', blank=True, null=True)  # Field name made lowercase.
    raz_social_emisor = models.CharField(db_column='RAZ_SOCIAL_EMISOR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nom_comercial_emisor = models.CharField(db_column='NOM_COMERCIAL_EMISOR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ubigeo_emisor = models.CharField(db_column='UBIGEO_EMISOR', max_length=6, blank=True, null=True)  # Field name made lowercase.
    direccion_emisor = models.CharField(db_column='DIRECCION_EMISOR', max_length=250, blank=True, null=True)  # Field name made lowercase.
    urbanizacion_emisor = models.CharField(db_column='URBANIZACION_EMISOR', max_length=25, blank=True, null=True)  # Field name made lowercase.
    provincia_emisor = models.CharField(db_column='PROVINCIA_EMISOR', max_length=30, blank=True, null=True)  # Field name made lowercase.
    departamento_emisor = models.CharField(db_column='DEPARTAMENTO_EMISOR', max_length=30, blank=True, null=True)  # Field name made lowercase.
    distrito_emisor = models.CharField(db_column='DISTRITO_EMISOR', max_length=30, blank=True, null=True)  # Field name made lowercase.
    pais_emisor = models.CharField(db_column='PAIS_EMISOR', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ruc_emisor = models.CharField(db_column='RUC_EMISOR', max_length=11, blank=True, null=True)  # Field name made lowercase.
    tip_doc_emisor = models.ForeignKey(Catalogo06DocumentoIdentidad,db_constraint=False,db_column='TIP_DOC_EMISOR', max_length=1, blank=True, null=True,on_delete=False)  # Field name made lowercase.
    serie_nc_nd = models.CharField(db_column='SERIE_NC_ND', max_length=4, blank=True, null=True)  # Field name made lowercase.
    nro_compr_nc_nd = models.CharField(db_column='NRO_COMPR_NC_ND', max_length=8, blank=True, null=True)  # Field name made lowercase.
    tip_nc_nd = models.CharField(db_column='TIP_NC_ND', max_length=2, blank=True, null=True)  # Field name made lowercase.
    motivo_nc_nd = models.CharField(db_column='MOTIVO_NC_ND', max_length=250, blank=True, null=True)  # Field name made lowercase.
    tip_doc_modif_nc_nd = models.CharField(db_column='TIP_DOC_MODIF_NC_ND', max_length=2, blank=True, null=True)  # Field name made lowercase.
    tipodoc_comprobante = models.ForeignKey(Catalogo01TipoDocumento,db_constraint=False,db_column='TIPODOC_COMPROBANTE', max_length=2, blank=True, null=True,on_delete=False)  # Field name made lowercase.
    cfnumser = models.CharField(db_column='CFNUMSER', max_length=4)  # Field name made lowercase.
    cfnumdoc = models.CharField(db_column='CFNUMDOC', max_length=8)  # Field name made lowercase.
    tip_doc_receptor = models.CharField(db_column='TIP_DOC_RECEPTOR', max_length=1, blank=True, null=True)  # Field name made lowercase.   -->OJO AQI HUBO UN CHANGE
    nro_doc_receptor = models.CharField(db_column='NRO_DOC_RECEPTOR', max_length=15, blank=True, null=True)  # Field name made lowercase. -->OJO AQI HUBO UN CHANGE
    cfcodcli = models.CharField(db_column='CFCODCLI', max_length=11, blank=True, null=True)  # Field name made lowercase.
    cfnombre = models.CharField(db_column='CFNOMBRE', max_length=250, blank=True, null=True)  # Field name made lowercase.
    direccion_receptor = models.CharField(db_column='DIRECCION_RECEPTOR', max_length=250, blank=True, null=True)  # Field name made lowercase.
    tvv_cod_ope_gravadas = models.CharField(db_column='TVV_COD_OPE_GRAVADAS', max_length=4, blank=True, null=True)  # Field name made lowercase.
    tvv_imp_ope_gravadas = models.DecimalField(db_column='TVV_IMP_OPE_GRAVADAS', max_digits=12, decimal_places=2)  # Field name made lowercase.
    tvv_cod_ope_inafectas = models.CharField(db_column='TVV_COD_OPE_INAFECTAS', max_length=4, blank=True, null=True)  # Field name made lowercase.
    tvv_imp_ope_inafectas = models.DecimalField(db_column='TVV_IMP_OPE_INAFECTAS', max_digits=12, decimal_places=2)  # Field name made lowercase.
    tvv_cod_ope_exoneradas = models.CharField(db_column='TVV_COD_OPE_EXONERADAS', max_length=4, blank=True, null=True)  # Field name made lowercase.
    tvv_imp_ope_exoneradas = models.DecimalField(db_column='TVV_IMP_OPE_EXONERADAS', max_digits=12, decimal_places=2)  # Field name made lowercase.
    sumatoria_igv = models.DecimalField(db_column='SUMATORIA_IGV', max_digits=12, decimal_places=2)  # Field name made lowercase.
    cod_tributo_igv = models.CharField(db_column='COD_TRIBUTO_IGV', max_length=4, blank=True, null=True)  # Field name made lowercase.
    nom_tributo_igv = models.CharField(db_column='NOM_TRIBUTO_IGV', max_length=6, blank=True, null=True)  # Field name made lowercase.
    cod_inter_igv = models.CharField(db_column='COD_INTER_IGV', max_length=3, blank=True, null=True)  # Field name made lowercase.
    sumatoria_isc = models.DecimalField(db_column='SUMATORIA_ISC', max_digits=12, decimal_places=2)    # Field name made lowercase.
    cod_tributo_isc = models.CharField(db_column='COD_TRIBUTO_ISC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    nom_tributo_isc = models.CharField(db_column='NOM_TRIBUTO_ISC', max_length=6, blank=True, null=True)  # Field name made lowercase.
    cod_inter_isc = models.CharField(db_column='COD_INTER_ISC', max_length=3, blank=True, null=True)  # Field name made lowercase.
    sumatoria_otros_trib = models.DecimalField(db_column='SUMATORIA_OTROS_TRIB', max_digits=12, decimal_places=2)  # Field name made lowercase.
    cod_tributo_otros_trib = models.CharField(db_column='COD_TRIBUTO_OTROS_TRIB', max_length=4, blank=True, null=True)  # Field name made lowercase.
    nom_tributo_otros_trib = models.CharField(db_column='NOM_TRIBUTO_OTROS_TRIB', max_length=6, blank=True, null=True)  # Field name made lowercase.
    cod_inter_otros_trib = models.CharField(db_column='COD_INTER_OTROS_TRIB', max_length=3, blank=True, null=True)  # Field name made lowercase.
    sumatoria_otros_cargos = models.DecimalField(db_column='SUMATORIA_OTROS_CARGOS', max_digits=12, decimal_places=2)  # Field name made lowercase.
    cod_tip_dsctos = models.CharField(db_column='COD_TIP_DSCTOS', max_length=4, blank=True, null=True)  # Field name made lowercase.
    importe_dsctos = models.DecimalField(db_column='IMPORTE_DSCTOS', max_digits=12, decimal_places=2)  # Field name made lowercase.
    importe_total_venta = models.DecimalField(db_column='IMPORTE_TOTAL_VENTA', max_digits=12, decimal_places=2)  # Field name made lowercase.
    serie_guia = models.CharField(db_column='SERIE_GUIA', max_length=4, blank=True, null=True)  # Field name made lowercase.
    nro_guia = models.CharField(db_column='NRO_GUIA', max_length=8, blank=True, null=True)  # Field name made lowercase.
    cod_tipo_guia = models.CharField(db_column='COD_TIPO_GUIA', max_length=2, blank=True, null=True)  # Field name made lowercase.
    serie_otro_refe = models.CharField(db_column='SERIE_OTRO_REFE', max_length=4, blank=True, null=True)  # Field name made lowercase.
    nro_otro_refe = models.CharField(db_column='NRO_OTRO_REFE', max_length=8, blank=True, null=True)  # Field name made lowercase.
    cod_tipo_refe = models.CharField(db_column='COD_TIPO_REFE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    cod_percepcion = models.CharField(db_column='COD_PERCEPCION', max_length=4, blank=True, null=True)  # Field name made lowercase.
    baseimponible_percepcion = models.DecimalField(db_column='BASEIMPONIBLE_PERCEPCION', max_digits=12, decimal_places=2)  # Field name made lowercase.
    monto_percepcion = models.DecimalField(db_column='MONTO_PERCEPCION', max_digits=12, decimal_places=2)  # Field name made lowercase.
    totalcobrado_percepcion = models.DecimalField(db_column='TOTALCOBRADO_PERCEPCION', max_digits=12, decimal_places=2)  # Field name made lowercase.
    ubl_version = models.CharField(db_column='UBL_VERSION', max_length=10, blank=True, null=True)  # Field name made lowercase.
    estruc_version = models.CharField(db_column='ESTRUC_VERSION', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tvv_cod_ope_gratuitas = models.CharField(db_column='TVV_COD_OPE_GRATUITAS', max_length=4, blank=True, null=True)  # Field name made lowercase.
    tvv_imp_ope_gratuitas = models.DecimalField(db_column='TVV_IMP_OPE_GRATUITAS', max_digits=15, decimal_places=2)  # Field name made lowercase.
    descuentos_globales = models.DecimalField(db_column='DESCUENTOS_GLOBALES', max_digits=12, decimal_places=2)  # Field name made lowercase.
    #estado_comprobante = models.CharField(db_column='ESTADO_COMPROBANTE', max_length=150, blank=True, null=True)  # Field name made lowercase.
    estado_comprobante = models.ForeignKey(EstadoDocumento, db_column='ESTADO_COMPROBANTE',max_length=20, blank=True,null=True,on_delete=False,default=POR_GENERAR_DOCUMENTO)  # Field name made lowercase.
    moneda = models.CharField(db_column='MONEDA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    cdr = models.CharField(db_column='CDR', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cod_resumen = models.CharField(db_column='COD_RESUMEN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cod_baja = models.CharField(db_column='COD_BAJA', max_length=20)  # Field name made lowercase.
    ruta_comprobante = models.CharField(db_column='RUTA_COMPROBANTE', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    ruta_cdr = models.CharField(db_column='RUTA_CDR', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    tipo_envio = models.CharField(db_column='TIPO_ENVIO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    correo = models.CharField(db_column='CORREO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    leyenda = models.CharField(db_column='LEYENDA', max_length=250, blank=True, null=True)  # Field name made lowercase.
    glosa_electronica = models.CharField(db_column='GLOSA_ELECTRONICA', max_length=250, blank=True, null=True)  # Field name made lowercase.
    cod_cat_detraccion = models.CharField(db_column='COD_CAT_DETRACCION', max_length=5, blank=True, null=True)  # Field name made lowercase.
    porcentaje_detraccion = models.CharField(db_column='PORCENTAJE_DETRACCION', max_length=18, blank=True, null=True)  # Field name made lowercase.
    monto_detraccion = models.DecimalField(db_column='MONTO_DETRACCION', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    valor_referencial_detraccion = models.DecimalField(db_column='VALOR_REFERENCIAL_DETRACCION', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    cod_cat_bbss_detraccion = models.CharField(db_column='COD_CAT_BBSS_DETRACCION', max_length=5, blank=True, null=True)  # Field name made lowercase.
    codigo_bbss_detraccion = models.CharField(db_column='CODIGO_BBSS_DETRACCION', max_length=5, blank=True, null=True)  # Field name made lowercase.
    cod_cat_cta_bn_detraccion = models.CharField(db_column='COD_CAT_CTA_BN_DETRACCION', max_length=5, blank=True, null=True)  # Field name made lowercase.
    cta_bn_detraccion = models.CharField(db_column='CTA_BN_DETRACCION', max_length=15, blank=True, null=True)  # Field name made lowercase.
    total_anticipo = models.DecimalField(db_column='TOTAL_ANTICIPO', max_digits=15, decimal_places=2)  # Field name made lowercase.
    tipo_operacion = models.CharField(db_column='TIPO_OPERACION', max_length=3, blank=True, null=True)  # Field name made lowercase.
    estado_correo = models.CharField(db_column='ESTADO_CORREO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ordencompra = models.CharField(db_column='ORDENCOMPRA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    usuario = models.CharField(db_column='USUARIO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    codigopventa = models.CharField(db_column='CODIGOPVENTA', max_length=20, blank=True, null=True)  # Field name made lowercase.
    placa = models.CharField(db_column='PLACA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    xml = models.TextField(db_column='XML', blank=True, null=True)  # Field name made lowercase.
    ubigeo_pventa = models.CharField(db_column='UBIGEO_PVENTA', max_length=12, blank=True, null=True)  # Field name made lowercase.
    direccion_pventa = models.CharField(db_column='DIRECCION_PVENTA', max_length=200, blank=True, null=True)  # Field name made lowercase.
    urbanizacion_pventa = models.CharField(db_column='URBANIZACION_PVENTA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    provincia_pventa = models.CharField(db_column='PROVINCIA_PVENTA', max_length=60, blank=True, null=True)  # Field name made lowercase.
    departamento_pventa = models.CharField(db_column='DEPARTAMENTO_PVENTA', max_length=60, blank=True, null=True)  # Field name made lowercase.
    distrito_pventa = models.CharField(db_column='DISTRITO_PVENTA', max_length=60, blank=True, null=True)  # Field name made lowercase.
    pais_pventa = models.CharField(db_column='PAIS_PVENTA', max_length=2, blank=True, null=True)  # Field name made lowercase.
    cffecven = models.DateTimeField(db_column='CFFECVEN', blank=True, null=True)  # Field name made lowercase.
    sumatoria_descuentos = models.DecimalField(db_column='SUMATORIA_DESCUENTOS', max_digits=12,
                                        decimal_places=2 ,blank=True, null=True)  # Field name made lowercase.
    customizacion = models.CharField(db_column='CUSTOMIZACION', max_length=10,blank=True, null=True)  # Field name made lowercase.
    estado_pdf= models.CharField(db_column='ESTADO_PDF',choices=ESTADO_PDF_CHOICES, max_length=2,blank=True,null=True,default=POR_GENERAR_PDF)  # Field name made lowercase.
    nom_archivo = models.TextField(db_column='NOM_ARCHIVO', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'COMPROBANTE_CAB'
        unique_together = (('cfnumser', 'cfnumdoc', 'tipodoc_comprobante'),)

class ComprobanteDet(models.Model):
    PORCENT_IGV=18.0
    PORCENT_ISC = 15.0
    id = models.AutoField(db_column='ID', primary_key=True)
    dfnumser = models.CharField(db_column='DFNUMSER', max_length=4)  # Field name made lowercase.
    dfnumdoc = models.CharField(db_column='DFNUMDOC', max_length=8)  # Field name made lowercase.
    tipodoc_comprobante = models.CharField(db_column='TIPODOC_COMPROBANTE', max_length=2)  # Field name made lowercase.
    orden_item = models.IntegerField(db_column='ORDEN_ITEM')  # Field name made lowercase.
    um_item = models.CharField(db_column='UM_ITEM', max_length=6, blank=True, null=True)  # Field name made lowercase.
    cant_item = models.DecimalField(db_column='CANT_ITEM', max_digits=18, decimal_places=10)  # Field name made lowercase.
    nom_item = models.CharField(db_column='NOM_ITEM', max_length=250, blank=True, null=True)  # Field name made lowercase.
    vu_item = models.DecimalField(db_column='VU_ITEM', max_digits=12, decimal_places=2)  # Field name made lowercase.
    imp_vu_item = models.DecimalField(db_column='IMP_VU_ITEM', max_digits=12, decimal_places=2)  # Field name made lowercase.
    cod_vu_item = models.CharField(db_column='COD_VU_ITEM', max_length=2, blank=True, null=True)  # Field name made lowercase.
    monto_igv = models.DecimalField(db_column='MONTO_IGV', max_digits=12, decimal_places=2)  # Field name made lowercase.
    afec_igv = models.CharField(db_column='AFEC_IGV', max_length=2, blank=True, null=True)  # Field name made lowercase.
    cod_igv = models.CharField(db_column='COD_IGV', max_length=4, blank=True, null=True)  # Field name made lowercase.
    nom_igv = models.CharField(db_column='NOM_IGV', max_length=6, blank=True, null=True)  # Field name made lowercase.
    cinter_igv = models.CharField(db_column='CINTER_IGV', max_length=3, blank=True, null=True)  # Field name made lowercase.
    monto_isc = models.DecimalField(db_column='MONTO_ISC', max_digits=12, decimal_places=2)  # Field name made lowercase.
    afec_isc = models.CharField(db_column='AFEC_ISC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    cod_isc = models.CharField(db_column='COD_ISC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    nom_isc = models.CharField(db_column='NOM_ISC', max_length=6, blank=True, null=True)  # Field name made lowercase.
    cinter_isc = models.CharField(db_column='CINTER_ISC', max_length=3, blank=True, null=True)  # Field name made lowercase.
    tvu_item = models.DecimalField(db_column='TVU_ITEM', max_digits=12, decimal_places=2)  # Field name made lowercase.
    cod_item = models.CharField(db_column='COD_ITEM', max_length=30, blank=True, null=True)  # Field name made lowercase.
    importe_nooneroso_item = models.DecimalField(db_column='IMPORTE_NOONEROSO_ITEM', max_digits=12, decimal_places=2)  # Field name made lowercase.
    cod_nooneroso_item = models.CharField(db_column='COD_NOONEROSO_ITEM', max_length=2, blank=True, null=True)  # Field name made lowercase.
    false_item = models.CharField(db_column='FALSE_ITEM', max_length=5, blank=True, null=True)  # Field name made lowercase.
    des_item = models.DecimalField(db_column='DES_ITEM', max_digits=12, decimal_places=2)  # Field name made lowercase.
    imp_total_item = models.DecimalField(db_column='IMP_TOTAL_ITEM', max_digits=12, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    porcent_igv=models.DecimalField(db_column='PORCENT_IGV', max_digits=5, decimal_places=2, blank=True, null=True,default=PORCENT_IGV) # Field name made lowercase.
    porcent_isc = models.DecimalField(db_column='PORCENT_ISC', max_digits=5, decimal_places=2, blank=True,
                                      null=True,default=PORCENT_ISC)  # Field name made lowercase.


    class Meta:
        managed = True
        db_table = 'COMPROBANTE_DET'
        unique_together = (('dfnumser', 'dfnumdoc', 'tipodoc_comprobante', 'orden_item'),)

class ComprobanteBaja(models.Model):
    id=models.AutoField(db_column='ID', primary_key=True)
    ruc_emisor = models.CharField(db_column='RUC_EMISOR', max_length=11, blank=True, null=True)  # Field name made lowercase.
    fecha_doc = models.DateTimeField(db_column='FECHA_DOC', blank=True, null=True)  # Field name made lowercase.
    tipo_doc = models.CharField(db_column='TIPO_DOC',  max_length=2)  # Field name made lowercase.
    serie_doc = models.CharField(db_column='SERIE_DOC', max_length=4)  # Field name made lowercase.
    numero_doc = models.CharField(db_column='NUMERO_DOC', max_length=8)  # Field name made lowercase.
    motivo_baja = models.CharField(db_column='MOTIVO_BAJA', max_length=100, blank=True, null=True)  # Field name made lowercase.
    estado = models.CharField(db_column='ESTADO', max_length=150, blank=True, null=True)  # Field name made lowercase.
    usuario = models.CharField(db_column='USUARIO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    codigopventa = models.CharField(db_column='CODIGOPVENTA', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'COMPROBANTE_BAJA'
        unique_together = (('tipo_doc', 'serie_doc', 'numero_doc'),)

class Cliente(models.Model):
    cfcodcli = models.CharField(db_column='CFCODCLI', max_length=11, primary_key=True)  # Field name made lowercase.
    cfnombre = models.CharField(db_column='CFNOMBRE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    direccion_receptor = models.CharField(db_column='DIRECCION_RECEPTOR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    correo = models.EmailField(db_column='CORREO', max_length=200, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = True
        db_table = 'CLIENTE'



class Catalogo05TiposTributos(models.Model):
    codigo = models.CharField(db_column='Codigo', max_length=4, primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=6, blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=200, blank=True, null=True)  # Field name made lowercase.
    un_ece_5153 = models.CharField(db_column='UN_ECE_5153', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CATALOGO_05_TIPOS_TRIBUTOS'


class Catalogo15ElementosAdicionales(models.Model):
    codigo = models.CharField(db_column='Codigo', max_length=4,primary_key =True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CATALOGO_15_ELEMENTOS_ADICIONALES'



class ResumenCab(models.Model):
    TIPO_RESUMEN_CHOICES= (
        ('RC','RESUMEN DE COMPROBANTE'),
        ('RA','RESUMEN DE ANULACION'),
    )
    RESUMEN_COMPROBANTE= 'RC'
    RESUMEN_ANULACION='RA'
    raz_social_emisor = models.CharField(db_column='RAZ_SOCIAL_EMISOR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ruc_emisor = models.CharField(db_column='RUC_EMISOR', max_length=11, blank=True, null=True)  # Field name made lowercase.
    tip_doc_emisor = models.CharField(db_column='TIP_DOC_EMISOR', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fec_doc = models.DateTimeField(db_column='FEC_DOC', blank=True, null=True)  # Field name made lowercase.
    tipo_resumen = models.CharField(db_column='TIPO_RESUMEN',choices=TIPO_RESUMEN_CHOICES, max_length=2, blank=True, null=True)  # Field name made lowercase.
    numser_resumen =models.CharField(db_column='NUMSER_RESUMEN', max_length=8, blank=True, null=True)  # Field name made lowercase.
    numdoc_resumen= models.CharField(db_column='NUMDOC_RESUMEN', max_length=3, blank=True, null=True)  # Field name made lowercase.
    fecha_gen = models.DateTimeField(db_column='FECHA_GEN', blank=True, null=True)  # Field name made lowercase.
    ubl_version = models.CharField(db_column='UBL_VERSION', max_length=10, blank=True, null=True)  # Field name made lowercase.
    estruc_version = models.CharField(db_column='ESTRUC_VERSION', max_length=10, blank=True, null=True)  # Field name made lowercase.
    estado_resumen = models.ForeignKey(EstadoDocumento, max_length=5, blank=True, null=True,on_delete=False)  # Field name made lowercase.
    cdr = models.CharField(db_column='CDR', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ruta_comprobante = models.CharField(db_column='RUTA_RESUMEN', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    ruta_cdr = models.CharField(db_column='RUTA_CDR', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    tipo_envio = models.CharField(db_column='TIPO_ENVIO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ticket = models.CharField(db_column='TICKET', max_length=50, blank=True, null=True)  # Field name made lowercase.
    xml = models.TextField(db_column='XML', blank=True, null=True)  # Field name made lowercase.
    nom_archivo = models.TextField(db_column='NOM_ARCHIVO', blank=True, null=True)  # Field name made lowercase.
    nro_reg = models.IntegerField(db_column='NRO_REG',blank=True,null=True,default=0)
    tipodoc_comprobante = models.CharField(db_column='TIPODOC_COMPROBANTE',blank=True,null=True,max_length=2)

    class Meta:
        managed = True
        db_table = 'RESUMEN_CAB'
        unique_together = (('tipo_resumen', 'numdoc_resumen','numser_resumen'),)



class ResumenDet(models.Model):
    ESTADO_CHOICES= (
        ('1','ADICIONAR'),
        ('2','MODIFICAR'),
        ('3','ANULADO'),
    )


    tipodoc_item = models.ForeignKey(Catalogo01TipoDocumento,db_constraint=False,db_column='TIPODOC_ITEM',  max_length=2, blank=True, null=True,on_delete=models.DO_NOTHING)  # Field name made lowercase.
    fecdoc_item =models.DateTimeField(db_column='FECDOC_ITEM',  blank=True, null=True)  # Field name made lowercase.
    numserie_item = models.CharField(db_column='NUMSERIE_ITEM', max_length=4, blank=True, null=True)  # Field name made lowercase.
    numdoc_item = models.CharField(db_column='NUMDOC_ITEM', max_length=8)  # Field name made lowercase.
    tipdoc_receptor = models.ForeignKey(Catalogo06DocumentoIdentidad,db_constraint=False,db_column='TIPDOC_RECEPTOR', max_length=1, blank=True,null=True,on_delete=models.DO_NOTHING)
    nrodoc_receptor = models.CharField(db_column='NRODOC_RECEPTOR', max_length=15, blank=True, null=True)
    moneda = models.CharField(db_column='MONEDA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    tvv_imp_ope_gravadas = models.DecimalField(db_column='TVV_IMP_OPE_GRAVADAS', max_digits=12, decimal_places=2)  # Field name made lowercase.
    tvv_cod_ope_gravadas = models.CharField(db_column='TVV_COD_OPE_GRAVADAS', max_length=4, blank=True, null=True)  # Field name made lowercase.
    tvv_imp_ope_inafectas = models.DecimalField(db_column='TVV_IMP_OPE_INAFECTAS', max_digits=12, decimal_places=2)  # Field name made lowercase.
    tvv_cod_ope_inafectas = models.CharField(db_column='TVV_COD_OPE_INAFECTAS', max_length=4, blank=True, null=True)  # Field name made lowercase.
    tvv_imp_ope_exoneradas = models.DecimalField(db_column='TVV_IMP_OPE_EXONERADAS', max_digits=12, decimal_places=2)  # Field name made lowercase.
    tvv_cod_ope_exoneradas = models.CharField(db_column='TVV_COD_OPE_EXONERADAS', max_length=4, blank=True, null=True)  # Field name made lowercase.
    tvv_imp_ope_gratuitas = models.DecimalField(db_column='TVV_IMP_OPE_GRATUITAS', max_digits=12,
                                                 decimal_places=2)  # Field name made lowercase.
    tvv_cod_ope_gratuitas = models.CharField(db_column='TVV_COD_OPE_GRATUITAS', max_length=4, blank=True,
                                              null=True)  # Field name made lowercase.
    imp_total_sum_otros_cargos = models.DecimalField(db_column='IMP_TOTAL_SUM_OTROS_CARGOS', max_digits=12,
                                                     decimal_places=2)  # Field name made lowercase.
    cod_tip_otros_cargos = models.CharField(db_column='COD_TIP_OTROS_CARGOS', max_length=5, blank=True, null=True)  # Field name made lowercase.
    monto_isc = models.DecimalField(db_column='MONTO_ISC', max_digits=12, decimal_places=2)  # Field name made lowercase.
    cod_tributo_isc = models.CharField(db_column='COD_TRIBUTO_ISC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    nom_tributo_isc = models.CharField(db_column='NOM_TRIBUTO_ISC', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cod_inter_isc = models.CharField(db_column='COD_INTER_ISC', max_length=3, blank=True, null=True)  # Field name made lowercase.
    monto_igv = models.DecimalField(db_column='MONTO_IGV', max_digits=12, decimal_places=2)  # Field name made lowercase.
    cod_tributo_igv = models.CharField(db_column='COD_TRIBUTO_IGV', max_length=4, blank=True, null=True)  # Field name made lowercase.
    nom_tributo_igv = models.CharField(db_column='NOM_TRIBUTO_IGV', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cod_inter_igv = models.CharField(db_column='COD_INTER_IGV', max_length=3, blank=True, null=True)  # Field name made lowercase.
    monto_otros_trib = models.DecimalField(db_column='MONTO_OTROS_TRIB', max_digits=12, decimal_places=2)  # Field name made lowercase.
    cod_tributo_otros_trib = models.CharField(db_column='COD_TRIBUTO_OTROS_TRIB', max_length=4, blank=True, null=True)  # Field name made lowercase.
    nom_tributo_otros_trib = models.CharField(db_column='NOM_TRIBUTO_OTROS_TRIB', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cod_inter_otros_trib = models.CharField(db_column='COD_INTER_OTROS_TRIB', max_length=3, blank=True, null=True)  # Field name made lowercase.
    importe_total_venta = models.DecimalField(db_column='IMPORTE_TOTAL_VENTA', max_digits=12, decimal_places=2)  # Field name made lowercase.
    tipodoc_modif = models.CharField(db_column='TIPODOC_MODIF', max_length=2, blank=True,null=True)  # Field name made lowercase.
    numserie_modif = models.CharField(db_column='NUMSERIE_MODIF', max_length=4, blank=True,null=True)  # Field name made lowercase.
    numdoc_modif = models.CharField(db_column='NUMDOC_MODIF', max_length=8, blank=True,null=True)  # Field name made lowercase.
    regimen_percepcion = models.CharField(db_column='REGIMEN_PERCEPCION', max_length=2, blank=True,
                                              null=True)  # Field name made lowercase.
    porcent_percepcion = models.DecimalField(db_column='PORCENT_PERCEPCION', max_digits=12, decimal_places=2,blank=True,null=True)  # Field name made lowercase.
    base_imponible_percepcion = models.DecimalField(db_column='BASE_IMPONIBLE_PERCEPCION', max_digits=12, decimal_places=2,blank=True,null=True)  # Field name made lowercase.
    monto_percepcion = models.DecimalField(db_column='MONTO_PERCEPCION', max_digits=12, decimal_places=2,blank=True,null=True)  # Field name made lowercase.
    motivo_baja = models.CharField(db_column='MOTIVO_BAJA', max_length=100, blank=True, null=True)  # Field name made lowercase.
    orden_item = models.CharField(db_column='ORDEN_ITEM', max_length=5, blank=True, null=True)  # Field name made lowercase.
    tipo_resumen = models.CharField(db_column='TIPO_RESUMEN',max_length=2,null=True ,blank=True)  # Field name made lowercase.

    numser_resumen = models.CharField(db_column='NUMSER_RESUMEN', max_length=8, blank=True,
                                      null=True)  # Field name made lowercase.
    numdoc_resumen = models.CharField(db_column='NUMDOC_RESUMEN', max_length=3, blank=True,
                                      null=True)  # Field name made lowercase.
    estado = models.CharField(db_column='ESTADO', max_length=2, blank=True, null=True)  # Field name made lowercase.
    resumen_cab= models.ForeignKey(ResumenCab, blank=True, null=True,on_delete=False)
    ruc_emisor = models.CharField(db_column='RUC_EMISOR', max_length=11, blank=True,
                                  null=True)  # Field name made lowercase.
    raz_social_emisor = models.CharField(db_column='RAZ_SOCIAL_EMISOR', max_length=100, blank=True,
                                         null=True)  # Field name made lowercase.
    tip_doc_emisor = models.CharField(db_column='TIP_DOC_EMISOR', max_length=1, blank=True,
                                      null=True)  # Field name made lowercase.



    class Meta:
        managed = True
        db_table = 'RESUMEN_DET'






