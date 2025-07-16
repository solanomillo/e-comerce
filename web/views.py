from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria

# Create your views here.
""" Vistas para mostrar el catalogo de productos"""

def index(request):
    listProductos = Producto.objects.all()
    listCategorias = Categoria.objects.all()
    
    return render(request, 'index.html', {
        'productos': listProductos,
        'categorias': listCategorias
    })


def producto_categoria(request, categoria_id):
    """Vista para mostrar productos por categoria"""
    objectsCategoria = Categoria.objects.get(pk=categoria_id)
    listProductos = objectsCategoria.producto_set.all()
    
    listCategorias = Categoria.objects.all()
    
    return render(request, 'index.html',{
        'productos': listProductos,
        'categorias': listCategorias
    })


def productosPorNombre(request):
    """ Vista para mostrar productos por nombre"""
    nombre = request.POST['nombre']
    
    listProductos = Producto.objects.filter(nombre__icontains=nombre)
    listCategorias = Categoria.objects.all()

    return render(request, 'snippets/busqueda.html',{
        'productos': listProductos,
        'categorias': listCategorias,
        'nombre': nombre,
    })


def productoDetalle(request, producto_id):
    """ Vista para mostrar el detalle de un producto """
    #producto = Producto.objects.get(pk=producto_id)
    
    producto = get_object_or_404(Producto, pk=producto_id)
    listCategorias = Categoria.objects.all()
    
    return render(request, 'snippets/producto_detalle.html',{
        'producto': producto,
        'categorias': listCategorias
    })