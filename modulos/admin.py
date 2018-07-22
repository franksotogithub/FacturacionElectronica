from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from .models import Menu
# Register your models here.

@admin.register(Menu)
class MenuAdmin(DraggableMPTTAdmin):
    pass
