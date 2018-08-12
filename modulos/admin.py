from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from .models import Menu ,Rol, Permiso
# Register your models here.

@admin.register(Menu)
class MenuAdmin(DraggableMPTTAdmin):
    pass

class PermisoAdmin(admin.TabularInline):
    model =  Permiso
    extra = 0

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    inlines = [
        PermisoAdmin,
    ]


