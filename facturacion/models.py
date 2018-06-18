from django.db import models

# Create your models here.

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


class FacturaElectronica(models.Model):
    idComprobante = models.CharField (primary_key=True, max_length=30)
    serieComprobante =models.CharField(max_length=10, null=True, blank=True)
    numComprobante = models.CharField(max_length=20, null=True, blank=True)
    codComprobante = models.ForeignKey (TipoComprobante , null=True , blank=True , on_delete=models.DO_NOTHING ,)
    numDocUsuario = models.ForeignKey(Usuario,null=True, blank=True , on_delete=models.DO_NOTHING ,)
    tipOperacion   = models.CharField(max_length=2,null=True,blank=True)
    fecEmision = models.CharField(max_length=10,null=False)
    codLocalEmisor   = models.CharField(max_length=3,null=True,blank=True)
    tipDocUsuario   = models.CharField(max_length=1,null=True,blank=True)
    rznSocialUsuario = models.CharField(max_length=100,null=True,blank=True)
    tipMoneda        = models.CharField(max_length=3)
    sumDsctoGlobal   = models.CharField(max_length=15,null=True,blank=True)
    sumOtrosCargos   = models.CharField(max_length=15,null=True,blank=True)
    mtoDescuentos    =models.CharField(max_length=15,null=True,blank=True)
    mtoOperGravadas  =models.CharField(max_length=15)
    mtoOperInafectas  =models.CharField(max_length=15)
    mtoOperExoneradas =models.CharField(max_length=15)
    mtoIGV            =models.CharField(max_length=15,null=True,blank=True)
    mtoISC   = models.CharField(max_length=15,null=True,blank=True)
    mtoOtrosTributos= models.CharField(max_length=15,null=True,blank=True)
    mtoImpVenta= models.CharField(max_length=15)

class DetalleFacturaElectronica(models.Model):
    idComprobante = models.ForeignKey(FacturaElectronica,null=True, blank=True , on_delete=models.DO_NOTHING,)
    codUnidadMedida = models.CharField(max_length=3)
    ctdUnidadItem = models.CharField(max_length=23)
    codProducto = models.CharField(max_length=30,null=True,blank=True)
    codProductoSUNAT = models.CharField(max_length=20,null=True,blank=True)
    desItem = models.CharField(max_length=250)
    mtoValorUnitario = models.CharField(max_length=23)
    mtoDsctoItem = models.CharField(max_length=15,null=True,blank=True)
    mtoIgvItem = models.CharField(max_length=15)
    tipAfeIGV = models.CharField(max_length=2)
    mtoIscItem = models.CharField(max_length=15,null=True,blank=True)
    tipSisISC = models.CharField(max_length=2,null=True,blank=True)
    mtoPrecioVentaItem = models.CharField(max_length=23)
    mtoValorVentaItem = models.CharField(max_length=15)