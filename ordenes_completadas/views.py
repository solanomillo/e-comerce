from django.core.paginator import Paginator
from django.shortcuts import render
from web.models import Pedido

def pedidosCompletados(request):
    pedidos_list = Pedido.objects.filter(estado='1').order_by('-fecha_pedido')  # 1 = Pagado
    paginator = Paginator(pedidos_list, 6)  # 👉 6 pedidos por página

    page_number = request.GET.get('page')
    pedidos = paginator.get_page(page_number)

    return render(request, 'ordenes_completadas/pedidos_completados.html', {
        'pedidos': pedidos
    })
