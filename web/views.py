from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Categoria
from .carts import Cart
from django.http import JsonResponse
from django.template.loader import render_to_string

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
    

""" VISTAS PARA EL CARRITO DE COMPRAS """
def carrito(request):
    cart = Cart(request)
    return render(request, 'snippets/cart.html', {
        'cart_items': cart.items(),
        'cart_total_price': cart.montoTotal
    })
    

def agregarProducto(request, producto_id):
    """ Agregar los productos al carrito """
    if request.method == 'POST':
        cantidad = int(request.POST['cantidad'])
    else:
        cantidad = 1
        
    objectProducto = Producto.objects.get(pk=producto_id)
    cart = Cart(request)
    cart.add(objectProducto, cantidad)
    
    # comprueba la ruta de donde vino y redirige a la misma
    if 'carrito' in request.META.get('HTTP_REFERER', ''):
            return redirect('web:carrito')
    return redirect(request.META.get('HTTP_REFERER', 'web:index'))


def eliminarProducto(request, producto_id):
    """ Eliminar productos del carrito """
    objectProducto = Producto.objects.get(pk=producto_id)
    cart = Cart(request)
    cart.delete(objectProducto)
    
    # comprueba la ruta de donde vino y redirige a la misma
    if 'carrito' in request.META.get('HTTP_REFERER', ''):
            return redirect('web:carrito')
    return redirect(request.META.get('HTTP_REFERER', 'web:index'))
    


def vaciarCarrito(request):
    """ Vaciar el carrito de compras """
    cart = Cart(request)  
    cart.clear()
    return render(request, 'snippets/cart.html')

def aumentar_producto(request, producto_id):
    """ Aumentar la cantidad de un producto en 1 """
    producto = Producto.objects.get(pk=producto_id)
    cart = Cart(request)
    cart.add(producto, 1)  # Aumenta en 1 la cantidad
    
    if 'carrito' in request.META.get('HTTP_REFERER', ''):
        return redirect('web:carrito')
    return redirect(request.META.get('HTTP_REFERER', 'web:index'))

def disminuir_producto(request, producto_id):
    """ Disminuir la cantidad de un producto en 1 """
    producto = Producto.objects.get(pk=producto_id)
    cart = Cart(request)
    
    # Buscar el producto en el carrito
    for item in cart.items():
        if item['producto_id'] == producto_id:
            if item['cantidad'] > 1:
                cart.add(producto, -1)  # Disminuir en 1
            else:
                cart.delete(producto)  # Eliminar si la cantidad sería 0
            break
    
    if 'carrito' in request.META.get('HTTP_REFERER', ''):
        return redirect('web:carrito')
    return redirect(request.META.get('HTTP_REFERER', 'web:index'))
