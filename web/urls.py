from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('categoria/<int:categoria_id>/', views.producto_categoria, name='producto_categoria'),
    path('buscar/', views.productosPorNombre, name='productos_por_nombre'),
    path('producto/<int:producto_id>/', views.productoDetalle, name= 'producto_detalle'),
    path('carrito/', views.carrito, name='carrito'),
    path('agregar/<int:producto_id>', views.agregarProducto, name='agregar_producto'),
    path('eliminar/<int:producto_id>', views.eliminarProducto, name='eliminar_producto'),
    path('vaciar',views.vaciarCarrito, name='vaciar_carrito')
    
]