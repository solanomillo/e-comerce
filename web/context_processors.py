from .models import Categoria
from .carts import Cart
from datetime import datetime


def categorias_disponibles(request):
    return {
        'categorias': Categoria.objects.all()
    }




def year_context(request):
    return {'year': str(datetime.now().year)}




def cart_context(request):
    cart = Cart(request)
    
    return {
        'cart': cart,  # Objeto Cart completo para acceder a todos sus métodos
        'cart_items': cart.items(),  # Lista de items en el carrito
        'cart_total_quantity': sum(int(item['cantidad']) for item in cart.items()),
        'cart_total_price': cart.montoTotal,  # Usamos el montoTotal que ya calcula la clase Cart
        'cart_subtotal': cart.montoTotal  # Alias para compatibilidad (opcional)
    }
