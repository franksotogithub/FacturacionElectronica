from django.db import models
from mptt.models import MPTTModel ,TreeForeignKey
# Create your models here.


class Menu(MPTTModel):
    descripcion= models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=100,unique=True)
    icono= models.CharField(max_length=20,blank=True, null=True, default=None )
    estado= models.BooleanField(default=True)
    parent = TreeForeignKey('self',null=True,blank=True,related_name='children',db_index=True,on_delete=False)

    def __str__(self):
        return self.descripcion