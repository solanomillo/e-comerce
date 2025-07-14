from django.contrib import admin
from .models import Categoria, Producto
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

