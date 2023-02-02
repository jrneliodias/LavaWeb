from django.contrib import admin
from .models import Cliente,Carro


# Register your models here.
@admin.register(Cliente,Carro)
class ClientesAdmin(admin.ModelAdmin):
    pass