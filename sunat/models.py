from django.db import models

# Create your models here.

class Documento(models.Model):
    num_ruc = models.CharField(db_column='NUM_RUC', max_length=11)  # Field name made lowercase.
    tip_docu = models.CharField(db_column='TIP_DOCU', max_length=2)  # Field name made lowercase.
    num_docu = models.CharField(db_column='NUM_DOCU', max_length=60,primary_key=True)  # Field name made lowercase.
    fec_carg = models.DateTimeField(db_column='FEC_CARG', blank=True, null=True)  # Field name made lowercase.
    fec_gene = models.DateTimeField(db_column='FEC_GENE', blank=True, null=True)  # Field name made lowercase.
    fec_envi = models.DateTimeField(db_column='FEC_ENVI', blank=True, null=True)  # Field name made lowercase.
    des_obse = models.CharField(db_column='DES_OBSE', max_length=250, blank=True, null=True)  # Field name made lowercase.
    nom_arch = models.CharField(db_column='NOM_ARCH', max_length=250, blank=True, null=True)  # Field name made lowercase.
    ind_situ = models.CharField(db_column='IND_SITU', max_length=2, blank=True, null=True)  # Field name made lowercase.
    tip_arch = models.CharField(db_column='TIP_ARCH', max_length=6, blank=True, null=True)  # Field name made lowercase.
    firm_digital = models.CharField(db_column='FIRM_DIGITAL', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DOCUMENTO'
        unique_together = (('num_ruc', 'tip_docu', 'num_docu'),)


class Parametro(models.Model):
    id_para = models.CharField(db_column='ID_PARA', max_length=10,primary_key=True)  # Field name made lowercase.
    cod_para = models.CharField(db_column='COD_PARA', max_length=10)  # Field name made lowercase.
    nom_para = models.CharField(db_column='NOM_PARA', max_length=30)  # Field name made lowercase.
    tip_para = models.CharField(db_column='TIP_PARA', max_length=10)  # Field name made lowercase.
    val_para = models.CharField(db_column='VAL_PARA', max_length=20)  # Field name made lowercase.
    ind_esta_para = models.CharField(db_column='IND_ESTA_PARA', max_length=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PARAMETRO'
        unique_together = (('id_para', 'cod_para'),)

class Error(models.Model):
    cod_cataerro = models.CharField(db_column='COD_CATAERRO', primary_key=True, max_length=4)  # Field name made lowercase.
    nom_cataerro = models.CharField(db_column='NOM_CATAERRO', max_length=120)  # Field name made lowercase.
    ind_estado = models.CharField(db_column='IND_ESTADO', max_length=1)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'ERROR'

