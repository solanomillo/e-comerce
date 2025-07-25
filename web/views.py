from urllib import request
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente, Producto, Categoria
from .carts import Cart
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistroForm
from django.contrib.auth.decorators import login_required

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
    
    pagina = request.GET.get('next', None)
    
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        pagina = request.POST.get('destino')
        
        usuario = authenticate(request, username=username, password=password)
        
        if usuario is not None:
            login(request, usuario)
            messages.success(request, f'Bienvenido {usuario.username}')
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
                username=data['nombre'],
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
            messages.success(request, 'Usuario registrado correctamente')
            
            # Iniciar sesión automáticamente al usuario
            if nuevoUsuario is not None:
                login(request, nuevoUsuario)
                messages.success(request,f'Bienvenido {nuevoUsuario.username}')
                return redirect('/')
            
    return render(request, 'registro.html', {
        'form': dataForm
    })       




def actualizarUsuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        provincia = request.POST.get('provincia')
        localidad = request.POST.get('localidad')
        codigo_postal = request.POST.get('codigo_postal')
        direccion = request.POST.get('direccion')
        
        if not all([nombre, apellido, provincia, localidad, codigo_postal, direccion]):
            messages.error(request, "Todos los campos son obligatorios")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        try:
            cliente = Cliente.objects.get(usuario=request.user)

            # Actualizar usuario
            user = request.user
            user.username = nombre
            user.last_name = apellido
            user.save()

            # Actualizar cliente
            cliente.provincia = provincia
            cliente.localidad = localidad
            cliente.codigo_postal = codigo_postal
            cliente.direccion = direccion
            cliente.save()

            messages.success(request, 'Datos actualizados correctamente')
            return redirect('web:registrar_pedido')

        except Cliente.DoesNotExist:
            messages.error(request, 'Cliente no encontrado')
            return redirect('/')

    return redirect('/')



""" VISTAS PARA EL PEDIDO """

@login_required(login_url='/login/')
def registrarPedido(request):
    """ Vista para registrar un pedido """
    try:
        cliente = Cliente.objects.get(usuario=request.user)

        dataCliente = {
            'nombre': cliente.usuario.username,
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


