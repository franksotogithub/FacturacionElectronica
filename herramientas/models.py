from django.db import models

# Create your models here.
class Proceso(models.Model):
    task_id = models.CharField(max_length=250,null=True,blank=True)
    descripcion = models.CharField(max_length=250,null=True,blank=True)
    fecha_ini = models.DateTimeField(null=True,blank=True)
    fecha_fin = models.DateTimeField(null=True,blank=True)
    estado = models.CharField(max_length=50,null=True,blank=True)
    icono = models.CharField(max_length=100,null=True,blank=True,default='icon-database-insert')

    def __str__(self):
        return self.descripcion

