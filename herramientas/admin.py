from django.contrib import admin
from herramientas.models import Proceso
# Register your models here.
@admin.register(Proceso)
class ProcesoAdmin(admin.ModelAdmin):
    list_display = ('id','descripcion','estado',)
    pass