from django.db import models
from clientes.models import Cliente
from .choices import ChoicesCategoriaManutencao
from datetime import datetime
from secrets import token_hex

class CategoriaManutencao(models.Model):
    titulo = models.CharField(max_length=3,choices = ChoicesCategoriaManutencao.choices)
    preco = models.DecimalField(max_digits= 8, decimal_places= 2)
    def __str__(self) -> str:
        return self.titulo
    
    
class Servico(models.Model):
    titulo = models.CharField(max_length=50)
    cliente = models.ForeignKey(Cliente,on_delete= models.SET_NULL,null = True)
    categoria_manutencao = models.ManyToManyField(CategoriaManutencao)
    data_inicio = models.DateField(null=True)
    data_entrega = models.DateField(null=True)
    finalizado = models.BooleanField(default= False)
    protocol = models.CharField(max_length=47, null = True, blank = True)
    
    def __str__(self) -> str:
        return self.titulo
    
    def save(self,*args, **kwargs):
        if not self.protocol:
            self.protocol = datetime.now().strftime("%d%m%Y_%H%M%S")+token_hex(12)
        super(Servico,self).save(*args,**kwargs)
    
    def preco_total(self):
        preco_total = float(0)
        for categoria in self.categoria_manutencao.all():
            preco_total+= float(categoria.preco)
            
        return preco_total