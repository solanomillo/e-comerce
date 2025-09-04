from django.urls import path
from . import views

app_name = 'ordenes_completadas'

urlpatterns = [
    path('', views.pedidosCompletados, name='pedidos_completados'),
]