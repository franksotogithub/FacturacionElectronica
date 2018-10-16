from django.db import models

# Create your models here.
class EmpresaParametro(models.Model):
    ruc = models.CharField(db_column='RUC', max_length=11, blank=True, null=True)  # Field name made lowercase.
    razon_social = models.CharField(db_column='RAZON_SOCIAL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    correo = models.CharField(db_column='CORREO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pass_correo = models.CharField(db_column='PASS_CORREO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    servidor_smtp = models.CharField(db_column='SERVIDOR_SMTP', max_length=100, blank=True, null=True)  # Field name made lowercase.
    puerto_correo = models.IntegerField(db_column='PUERTO_CORREO',blank=True, null=True)
    logo = models.FileField(db_column='LOGO',blank=True, null=True)
    ruta_archivos_sunat = models.CharField(db_column='RUTA_ARCHIVOS_SUNAT',max_length=250,blank=True,null=True)
    ruta_base_sunat = models.CharField(db_column='RUTA_BASE_SUNAT',max_length=250,blank=True,null=True)
   #class Meta:
   #    managed = True
   #    db_table = 'EMPRESA_PARAMETRO'

#class Local(models.Model):
#
#    codigo = models.CharField(db_column='CODIGO', max_length=3,blank=True, null=True)  # Field name made lowercase.
#    descripcion =  models.CharField(db_column='DESCRIPCION', max_length=100, blank=True, null=True)  # Field name made lowercase.
#    class Meta:
#        managed = True
#        db_table = 'LOCAL'


class Local(models.Model):
    codigo = models.CharField(max_length=5,null=True,blank=True)  # Field name made lowercase.
    tipo = models.CharField(max_length=30,null=True,blank=True)
    domicilio = models.CharField(max_length=250,null=True,blank=True)
    otras_referencias = models.CharField(max_length=250,null=True,blank=True)
    serief =models.CharField(max_length=10,null=True,blank=True)
    serieb = models.CharField(max_length=10, null=True, blank=True)
    ncbole = models.CharField(max_length=10, null=True, blank=True)
    ncfact = models.CharField(max_length=10, null=True, blank=True)
    codigo_original = models.CharField(max_length=10, null=True, blank=True)


    def __str__(self):
        return self.codigo


class PadronRuc(models.Model):
    ruc = models.CharField(primary_key=True,max_length=15)
    nombre_razon_social = models.CharField(max_length=250,blank=True,null=True)
    estado = models.CharField(max_length=50,null=True,blank=True)
    condicion_domicilio = models.CharField(max_length=20,null=True,blank=True)
    ubigeo = models.CharField(max_length=6,null=True,blank=True)
    tipo_via = models.CharField(max_length=20,null=True,blank=True)
    nom_via = models.CharField(max_length=250, null=True, blank=True)
    zona = models.CharField(max_length=50, null=True, blank=True)
    tipo_zona = models.CharField(max_length=50, null=True, blank=True)
    numero = models.CharField(max_length=50, null=True, blank=True)
    interior = models.CharField(max_length=50, null=True, blank=True)
    lote = models.CharField(max_length=50, null=True, blank=True)
    departamento = models.CharField(max_length=250, null=True, blank=True)
    manzana = models.CharField(max_length=50, null=True, blank=True)
    kilometro = models.CharField(max_length=50, null=True, blank=True)
