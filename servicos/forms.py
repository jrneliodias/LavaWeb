from django.forms import ModelForm
from .models import Servico,CategoriaManutencao

class FormServico(ModelForm):
    class Meta:
        model = Servico
        exclude = ['finalizado','protocol']
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #self.fields['titulo'].widget.attrs.update({'class':'form-control'})
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control p-2'})
            self.fields[field].widget.attrs.update({'placeholder':field})
        
        choices = list()
        for i, j in self.fields['categoria_manutencao'].choices:
            categoria = CategoriaManutencao.objects.get(titulo=j)
            choices.append((i.value,categoria.get_titulo_display()))
        
        self.fields['categoria_manutencao'].choices = choices