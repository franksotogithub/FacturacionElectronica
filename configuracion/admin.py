from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from configuracion.models import PadronRuc ,Local
# Register your models here.
@admin.register(PadronRuc)
class PadronAdmin(ImportExportActionModelAdmin):
    pass

class LocalResource(resources.ModelResource):
    class Meta:
        model = Local
        exclude = ('id','codigo_original' )
        import_id_fields = ('codigo',)


@admin.register(Local)
class LocalAdmin(ImportExportActionModelAdmin):
    resource_class = LocalResource

    list_display = ('codigo','tipo','domicilio')