from django.db import models
from mptt.models import MPTTModel ,TreeForeignKey
# Create your models here.


class Menu(MPTTModel):
    descripcion= models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=100,unique=True)
    icono= models.CharField(max_length=20,blank=True, null=True, default=None )
    estado= models.BooleanField(default=True)
    parent = TreeForeignKey('self',null=True,blank=True,related_name='children',db_index=True,on_delete=False)
    requiere_autenticacion=models.BooleanField(default=True)
    def __str__(self):
        return self.descripcion

class Rol(models.Model):
    descripcion= models.CharField(max_length=100,blank=True, null=True)
    def __str__(self):
        return self.descripcion

class Permiso(models.Model):
    menu=models.ForeignKey(Menu,blank=True, null=True,on_delete=False)
    rol = models.ForeignKey(Rol,blank=True, null=True,on_delete=False)
    estado= models.BooleanField(default=True)
    def __str__(self):
        return self.menu.descripcion +' '+self.rol.descripcion