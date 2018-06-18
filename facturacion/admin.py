from django.contrib import admin
from .models import FacturaElectronica , DetalleFacturaElectronica , Usuario , TipoComprobante

# Register your models here.
@admin.register(FacturaElectronica)
class FacturaElectronicaAdmin(admin.ModelAdmin):
    list_display = ('idComprobante','rznSocialUsuario','numDocUsuario')

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('numDocUsuario','rznSocialUsuario')

@admin.register(DetalleFacturaElectronica)
class DetalleFacturaElectronicaAdmin(admin.ModelAdmin):
    list_display = ('idComprobante','desItem','mtoValorVentaItem')

@admin.register(TipoComprobante)
class TipoComprobanteAdmin(admin.ModelAdmin):
    list_display = ('descripcion',)