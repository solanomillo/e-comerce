from django.contrib import admin
from .models import Categoria, Producto, Pedido, PedidoDetalle
from django.utils.safestring import mark_safe

# Register your models here.

@admin.register(Categoria)
class AdminCategoria(admin.ModelAdmin):
    list_display = ('nombre','fecha_registro')
    readonly_fields = ('fecha_registro',)


@admin.register(Producto)
class AdminProducto(admin.ModelAdmin):
    list_display = ('categoria', 'nombre', 'precio','imagen')
    list_editable = ('precio',)
    list_filter = ('categoria__nombre',)
    search_fields = ('categoria__nombre', 'nombre')
    readonly_fields = ('fecha_registro',)

class PedidoDetalleInline(admin.TabularInline):  # o admin.StackedInline si preferís en bloque
    model = PedidoDetalle
    extra = 0
    readonly_fields = ('producto_imagen',)
    fields = ('producto', 'producto_imagen', 'cantidad', 'subtotal')  # orden personalizado

    def producto_imagen(self, obj):
        if obj.producto.imagen:
            return mark_safe(f'<img src="{obj.producto.imagen.url}" width="60" height="60" style="object-fit: cover;" />')
        return '(Sin imagen)'
    
    producto_imagen.allow_tags = True
    producto_imagen.short_description = 'Imagen'

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('nro_pedido', 'cliente', 'estado', 'fecha_pedido', 'monto_total')
    list_filter = ('estado', 'fecha_pedido')
    search_fields = ('nro_pedido', 'cliente__usuario__username')
    inlines = [PedidoDetalleInline]


@admin.register(PedidoDetalle)
class AdminPedidoDetalle(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'subtotal')
    list_filter = ('pedido__nro_pedido', 'producto__nombre')
    search_fields = ('pedido__nro_pedido', 'producto__nombre')
    def has_add_permission(self, request, obj=None):
        return False
