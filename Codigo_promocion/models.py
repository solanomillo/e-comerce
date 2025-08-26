from django.db import models
import string
import random
from django.utils import timezone
from django.db.models.signals import pre_save

# Create your models here.
class PromoCodigo(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descuento = models.FloatField(default=0.0)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_final = models.DateTimeField(default=timezone.now)
    usado = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.codigo

def set_codigo(sender, instance, *args, **kwargs):
    if not instance.codigo:
        instance.codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

pre_save.connect(set_codigo, sender=PromoCodigo)
