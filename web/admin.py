from django.contrib import admin
from .models import Categoria, Producto, Pedido, PedidoDetalle
from django.urls import reverse
from django.utils.html import format_html
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

class PedidoDetalleInline(admin.TabularInline):
    model = PedidoDetalle
    extra = 0
    readonly_fields = ('producto_imagen',)
    fields = ('producto', 'producto_imagen', 'cantidad', 'subtotal')

    def producto_imagen(self, obj):
        if obj.producto.imagen:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover;" />',
                obj.producto.imagen.url
            )
        return '(Sin imagen)'
    producto_imagen.short_description = 'Imagen'


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        'nro_pedido',
        'cliente_link',
        'cliente_email',
        'cliente_telefono',
        'cliente_direccion',
        'estado',
        'fecha_pedido',
        'total_productos_display',
        'descuento_display',
        'envio_display',
        'total_final_display',
    )
    list_filter = ('estado', 'fecha_pedido')
    search_fields = (
        'nro_pedido',
        'cliente__usuario__username',
        'cliente__usuario__first_name',
        'cliente__usuario__last_name',
        'cliente__telefono',
    )
    inlines = [PedidoDetalleInline]

    # === Cliente ===
    def cliente_link(self, obj):
        """Nombre completo con link al perfil del usuario en admin"""
        url = reverse('admin:auth_user_change', args=[obj.cliente.usuario.id])
        return format_html('<a href="{}">{}</a>', url, obj.cliente.usuario.get_full_name())
    cliente_link.short_description = 'Cliente'

    def cliente_email(self, obj):
        return obj.cliente.usuario.email
    cliente_email.short_description = 'Email'

    def cliente_telefono(self, obj):
        return getattr(obj.cliente, 'telefono', '(No disponible)')
    cliente_telefono.short_description = 'Teléfono'

    def cliente_direccion(self, obj):
        return f"{obj.cliente.direccion}, {obj.cliente.localidad}, {obj.cliente.provincia}, CP: {obj.cliente.codigo_postal}"
    cliente_direccion.short_description = 'Dirección completa'

    # === Totales ===
    def total_productos_display(self, obj):
        return f"${obj.total_productos():,.2f}"
    total_productos_display.short_description = "Productos"

    def descuento_display(self, obj):
        if obj.promo_codigo:
            return f"{obj.promo_codigo.descuento}% (-${obj.calcular_descuento():,.2f})"
        return "-"
    descuento_display.short_description = "Descuento"

    def envio_display(self, obj):
        return f"${obj.envio_total:,.2f}"
    envio_display.short_description = "Envío"

    def total_final_display(self, obj):
        return f"${obj.total_final():,.2f}"
    total_final_display.short_description = "Total Final"


@admin.register(PedidoDetalle)
class AdminPedidoDetalle(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'subtotal')
    list_filter = ('pedido__nro_pedido', 'producto__nombre')
    search_fields = ('pedido__nro_pedido', 'producto__nombre')

    def has_add_permission(self, request, obj=None):
        return False