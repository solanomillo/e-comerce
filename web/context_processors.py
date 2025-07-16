from .models import Categoria
from carts.models import Cart
from datetime import datetime

def categorias_disponibles(request):
    return {
        'categorias': Categoria.objects.all()
    }




def year_context(request):
    return {'year': str(datetime.now().year)}
