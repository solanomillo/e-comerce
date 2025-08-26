from django.urls import path
from . import views

app_name = 'codigo_promocion'

urlpatterns = [
    path("pedido/<int:pedido_id>/aplicar-codigo/", views.aplicar_codigo, name="aplicar_codigo"),

]
