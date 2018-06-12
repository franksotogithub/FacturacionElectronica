from django.db import models

# Create your models here.

class FacturaElectronica(models.Model):
    tipOperacion   = models.CharField(max_length=2,null=True,blank=True)
    fecEmision= models.CharField(max_length=10,null=False)
    codLocalEmisor   = models.CharField(max_length=3,null=True,blank=True)
    tipDocUsuario   = models.CharField(max_length=1,null=True,blank=True)
    numDocUsuario   = models.CharField(max_length=15,null=True,blank=True)
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

