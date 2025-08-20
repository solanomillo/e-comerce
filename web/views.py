import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente, Producto, Categoria, Pedido, PedidoDetalle
from .carts import Cart
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistroForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


# Create your views here.

class ProductoListView(ListView):
    """Vistas para mostrar el catalogo de productos"""
    template_name = 'index.html'
    queryset = Producto.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['mostrar_hero'] = True
        return context

def producto_categoria(request, categoria_id):
    """Vista para mostrar productos por categoria"""
    objectsCategoria = Categoria.objects.get(pk=categoria_id)
    listProductos = objectsCategoria.producto_set.all()
    
    listCategorias = Categoria.objects.all()
    
    return render(request, 'index.html',{
        'productos': listProductos,
        'categorias': listCategorias,
        'mostrar_hero': False,
    })


def busquedaProductoNombre(request):
    """ Vista para mostrar productos por nombre"""
    nombre = request.GET.get('nombre', '').strip()
    
    listProductos = Producto.objects.filter(nombre__icontains=nombre)
    listCategorias = Categoria.objects.all()

    return render(request, 'snippets/busqueda.html',{
        'productos': listProductos,
        'categorias': listCategorias,
        'nombre': nombre,
        'mostrar_hero': False,
    })

class ProductoDetailView(DetailView):
    """ Vista para mostrar el detalle de un producto """
    model = Producto
    template_name = 'snippets/producto_detalle.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context

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
        if item ['producto_id'] == producto_id:
            if item['cantidad'] > 1:
                cart.add(producto, -1)  # Disminuir en 1
            else:
                cart.delete(producto)  # Eliminar si la cantidad sería 0
            break
    
    if 'carrito' in request.META.get('HTTP_REFERER', ''):
        return redirect('web:carrito')
    return redirect(request.META.get('HTTP_REFERER', 'web:index'))


""" VISTAS PARA EL LOGIN Y REGISTRO DE USUARIOS """
def login_view(request):
    ''' vista para el login de usuarios'''
    if request.user.is_authenticated:
        return redirect('/')
    
    pagina = request.GET.get('next', '/')
    
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        pagina = request.POST.get('destino')
        
        usuario = authenticate(request, username=username, password=password)
        
        if usuario is not None:
            login(request, usuario)
            messages.success(request, f'Bienvenido {usuario.first_name} {usuario.last_name}')
            # Si hay un 'next' en la URL, redirigir a esa página
            if pagina:
                return HttpResponseRedirect(pagina)
            # Redirigir al index si no hay 'next' en la URL
            return redirect('/')          

            
        else:
            messages.error(request, 'Datos incorrectos')
    
    return render(request, 'login.html', {
        'destino': pagina
    })

def logout_view(request):
    ''' vista para el logout de usuarios '''
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('/')

       
def registro(request):
    ''' vista para el registro de usuarios '''
    if request.user.is_authenticated:
        return redirect('/')
    
    dataForm = RegistroForm()
    if request.method == 'POST':
        dataForm = RegistroForm(request.POST or None)
        if dataForm.is_valid():
            # limpiar los datos del formulario
            data = dataForm.cleaned_data
            # Crear el usuario
            nuevoUsuario = User.objects.create_user(
                username=data['email'],
                first_name=data['nombre'],
                last_name=data['apellido'],
                email=data['email'],
                password=data['password']
            )
            
            # Crear el cliente asociado al usuario
            Cliente.objects.create(
                usuario=nuevoUsuario,
                telefono=data['telefono'],
                provincia=data['provincia'],
                localidad=data['localidad'],
                codigo_postal=data['codigo_postal'],
                direccion=data['direccion']
            )
            
            # Iniciar sesión automáticamente al usuario
            if nuevoUsuario is not None:
                login(request, nuevoUsuario)
                messages.success(request,f'Bienvenido {nuevoUsuario.first_name} {nuevoUsuario.last_name}')
                return redirect('/')
            
    return render(request, 'registro.html', {
        'form': dataForm
    })       


""" VISTAS PARA EL PEDIDO """

@login_required(login_url='/login/')
def registrarPedido(request):
    """ Vista para registrar un pedido """
    try:
        cliente = Cliente.objects.get(usuario=request.user)

        dataCliente = {
            'nombre': cliente.usuario.first_name,
            'apellido': cliente.usuario.last_name,
            'provincia': cliente.provincia,
            'localidad': cliente.localidad,
            'codigo_postal': cliente.codigo_postal,
            'direccion': cliente.direccion
        }

        formCliente = RegistroForm(dataCliente)  # si lo seguís usando en otra parte

    except Cliente.DoesNotExist:
        messages.error(request, 'Debes completar tu perfil antes de realizar un pedido.')
        return redirect('/')

    return render(request, 'pedido.html', {
        'formCliente': formCliente,   # por si lo usás en otro lado
        'cliente': cliente,           # este es el que necesita el template
    })


""""Vista del método de pago"""
@login_required(login_url='/login/')
def confirmarPedido(request):
    if request.method == 'POST':
        # 1. Actualizamos el usuario
        actUsuario = User.objects.get(pk=request.user.id)
        actUsuario.first_name = request.POST['nombre']
        actUsuario.last_name = request.POST['apellido']
        actUsuario.save()
        
        # 2. Actualizamos el cliente
        actCliente = Cliente.objects.get(usuario=request.user)       
        actCliente.provincia = request.POST['provincia']
        actCliente.localidad = request.POST['localidad']
        actCliente.codigo_postal = request.POST['codigo_postal']
        actCliente.direccion = request.POST['direccion']
        actCliente.save()
        
        # 3. Datos del carrito y total
        cart = request.session.get('cart')
        monto_total = float(request.session.get('cartMontoTotal', 0))

        # 4. Creamos el pedido con todo completo ANTES de guardar
        fecha_actual = datetime.datetime.now()
        nuevoPedido = Pedido(
            cliente=actCliente,
            fecha_pedido=fecha_actual,
            monto_total=monto_total
        )
        nuevoPedido.save()

        # 5. Generamos el nro_pedido (usando el ID generado)
        nro_pedido = f'PED-{fecha_actual.strftime("%Y")}{nuevoPedido.id:05d}'
        nuevoPedido.nro_pedido = nro_pedido
        nuevoPedido.save()
        
        # registrar la variable de session para el pedido
        request.session['pedidoId'] = nuevoPedido.id

        # 6. Registramos los detalles del pedido
        for key, value in cart.items():
            producto = Producto.objects.get(pk=value['producto_id'])
            detalle = PedidoDetalle(
                pedido=nuevoPedido,
                producto=producto,
                cantidad=int(value['cantidad']),
                subtotal=float(value['subtotal'])
            )
            detalle.save()
        
        # 7. Configuramos PayPal
        paypal_dict = {
            "business": "sb-ii8ew38425031@business.example.com",
            "amount": monto_total,
            "item_name": f'Pedido {nuevoPedido.nro_pedido} - {nuevoPedido.cliente.usuario.username}',
            "invoice": nro_pedido,
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri('/gracias'),
            "cancel_return": request.build_absolute_uri('/'),
            "custom": "premium_plan",
        }
        formPaypal = PayPalPaymentsForm(initial=paypal_dict)
        
        # limpiar el carrito después de crear el pedido
        carrito = Cart(request)
        carrito.clear()

        return render(request, 'compra.html', {
            'pedido': nuevoPedido,
            'formPaypal': formPaypal,
        })   

    # Si no es POST, redirigimos o mostramos un error
    return render(request, 'compra.html')

@login_required(login_url='/login/')
def gracias(request):
    paypalId = request.GET.get('PayerID', None)
    
    if paypalId is not None:
        pedidoId = request.session.get('pedidoId')
        pedido = Pedido.objects.get(pk=pedidoId)
        pedido.estado = '1'
        pedido.save()
    else:
        return redirect('/')
    return render(request,'gracias.html',{
        'pedido': pedido 
    })







# def view_that_asks_for_money(request):

#     # What you want the button to do.
#     paypal_dict = {
#         "business": "sb-ii8ew38425031@business.example.com",
#         "amount": "50.00",
#         "item_name": "producto prueba",
#         "invoice": "50-ED50",
#         "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
#         "return": request.build_absolute_uri('/'),
#         "cancel_return": request.build_absolute_uri('/'),
#         "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
#     }

#     # Create the instance.
#     form = PayPalPaymentsForm(initial=paypal_dict)
#     context = {"form": form}
#     return render(request, "payment.html", context)