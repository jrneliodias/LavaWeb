from django.shortcuts import render
from .forms import FormServico

# Create your views here.
def novo_servico(request):
    form = FormServico()
    return render(request, 'novo_servico.html',{'form':form})

