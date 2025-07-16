from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('categoria/<int:categoria_id>/', views.producto_categoria, name='producto_categoria'),
    path('buscar/', views.productosPorNombre, name='productos_por_nombre'),
    path('producto/<int:producto_id>/', views.productoDetalle, name= 'producto_detalle'),
]