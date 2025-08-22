from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.ProductoListView.as_view(), name='index'),
    path('categoria/<slug:slug>/', views.ProductoCategoriaListView.as_view(), name='producto_categoria'),
    path('buscar/', views.BuscarProductoListView.as_view(), name='productos_por_nombre'),
    path('producto/<slug:slug>/', views.ProductoDetailView.as_view(), name= 'producto_detalle'),
    path('carrito/', views.carrito, name='carrito'),
    path('agregar/<int:producto_id>', views.agregarProducto, name='agregar_producto'),
    path('eliminar/<int:producto_id>', views.eliminarProducto, name='eliminar_producto'),
    path('vaciar',views.vaciarCarrito, name='vaciar_carrito'),
    path('carrito/aumentar/<int:producto_id>/', views.aumentar_producto, name='aumentar_producto'),
    path('carrito/disminuir/<int:producto_id>/', views.disminuir_producto, name='disminuir_producto'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('pedido/', views.registrarPedido, name='registrar_pedido'),
    path('confirmar_pedido/', views.confirmarPedido, name='confirmar_pedido'),
    path('gracias/', views.gracias, name='gracias')
]