from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import PromoCodigo
from web.models import Pedido
from .forms import AplicarCodigoForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal

@login_required(login_url='/login/')
def aplicar_codigo(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente__usuario=request.user)

    if request.method == 'POST':
        form = AplicarCodigoForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['codigo'].strip().upper()
            try:
                promo = PromoCodigo.objects.get(codigo=codigo, usado=False)
            except PromoCodigo.DoesNotExist:
                messages.error(request, "El código no es válido o ya fue usado")
                return redirect('web:confirmar_pedido')

            # --- Nuevo enfoque: asignamos el cupón al pedido ---
            pedido.promo_codigo = promo
            pedido.save()

            # Marcamos el código como usado
            promo.usado = True
            promo.save()

            messages.success(request, f"Cupón {codigo} aplicado correctamente")
            return redirect('web:confirmar_pedido')

    return redirect('web:confirmar_pedido')

