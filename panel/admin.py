from django.contrib import admin
from .models import Producto, ContenidoInstitucional, PuntoVenta

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'usuario', 'activo','temporadas')
    list_filter = ('activo', 'usuario')
    search_fields = ('nombre', 'descripcion')

@admin.register(ContenidoInstitucional)
class ContenidoInstitucionalAdmin(admin.ModelAdmin):
    list_display = ('actualizado',)
    readonly_fields = ('actualizado',)


@admin.register(PuntoVenta)
class PuntoVentaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ciudad', 'region', 'activo')
    list_filter = ('activo', 'ciudad', 'region')
    search_fields = ('nombre', 'direccion', 'ciudad', 'region')
