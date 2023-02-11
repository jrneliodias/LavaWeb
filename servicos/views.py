from django.shortcuts import render
from .forms import FormServico
from django.http import HttpResponse
from django.contrib.messages import add_message, constants

# Create your views here.
def novo_servico(request):
    if request.method == "GET":
        form = FormServico()
        return render(request, 'novo_servico.html',{'form':form})
    elif request.method == "POST":
        form = FormServico(request.POST)
        if form.is_valid():
            form.save()
            add_message(request,constants.SUCCESS, "Cliente atualizado com sucesso!")
            form2 = FormServico()
            return render(request, 'novo_servico.html',{'form':form2})
        
        else:
            add_message(request,constants.ERROR, "Campo preenchido incorretamente!")
            return render(request, 'novo_servico.html',{'form':form})

    
