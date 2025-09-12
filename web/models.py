from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
import decimal
from Codigo_promocion.models import PromoCodigo

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='nombre', null=False, blank=False, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    

class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT, related_name='productos')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(null=True)
    precio = models.DecimalField(max_digits=9, decimal_places=2)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='productos', blank=True)
    slug = AutoSlugField(populate_from='nombre', null=False, blank=False, unique=True)
        
    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.RESTRICT)
    telefono = models.CharField(max_length=20, null=True)
    provincia = models.CharField(max_length=50)
    localidad = models.CharField(max_length=50)
    codigo_postal = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    

    def __str__(self):
        return self.usuario.username


class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('0', 'Pendiente'),
        ('1', 'Pagado'),
        ('2', 'Enviado'),        
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    nro_pedido = models.CharField(max_length=20, unique=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    envio_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    promo_codigo = models.OneToOneField(PromoCodigo, on_delete=models.RESTRICT, null=True, blank=True)

    
    def __str__(self):
        return f'Pedido {self.id} - {self.cliente.usuario.username}'

    # --- Métodos de cálculo ---
    def total_productos(self):
        """Retorna la suma de los subtotales de los detalles"""
        total = decimal.Decimal('0.00')
        for detalle in self.detalles.all():
            total += decimal.Decimal(detalle.subtotal)
        return total

    def calcular_descuento(self):
        """Calcula el descuento según el código promocional"""
        if self.promo_codigo:
            return (self.total_productos() * decimal.Decimal(self.promo_codigo.descuento)) / decimal.Decimal('100')
        return decimal.Decimal('0.00')

    def total_con_envio(self):
        """Suma productos + envío sin aplicar descuento"""
        return self.total_productos() + decimal.Decimal(str(self.envio_total))

    def total_final(self):
        """Suma productos + envío - descuento"""
        return self.total_con_envio() - self.calcular_descuento()
    
 
class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.RESTRICT, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    cantidad = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.producto.nombre