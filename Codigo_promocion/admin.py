from django.contrib import admin
from .models import PromoCodigo
# Register your models here.

@admin.register(PromoCodigo)
class PromoCodigoAdmin(admin.ModelAdmin):
    exclude = ('codigo',)
