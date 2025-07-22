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
        'cart': cart,
        'cart_items': list(cart.items()),  # Convertimos a lista para evitar problemas
        'cart_total_quantity': sum(item['cantidad'] for item in cart.items()),
        'cart_total_price': cart.montoTotal,
    }
