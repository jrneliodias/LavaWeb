from django.shortcuts import render
from django.http import HttpResponse
from .models import Cliente, Carro
import re
# Create your views here.
def clientes(request):
    if request.method == "GET":
        return render(request,'clientes.html')
    
    elif request.method == "POST":
        # Receber os dados do formulário
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        carros = request.POST.getlist('carro')
        placas = request.POST.getlist('placa')
        anos = request.POST.getlist('ano')
        
        cliente = Cliente.objects.filter(cpf=cpf)
        
        if cliente.exists():
            return render(request,'clientes.html',
                                {'nome':nome,
                                 'sobrenome':sobrenome,
                                 'email': email})
        
        email_validation = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        
        if not re.fullmatch(re.compile(email_validation), email):
            return render(request,'clientes.html',
                                {'nome':nome,
                                 'sobrenome':sobrenome,
                                 'cpf': cpf})
        
        # Criar o cliente na tabela
        cliente = Cliente(
            nome = nome,
            sobrenome = sobrenome,
            email = email,
            cpf = cpf
        )
        cliente.save()
        # Inserir na tabela de carros
        for carro, placa,ano in zip(carros,placas,anos):
            carro = Carro(carro = carro, placa =placa,ano=ano,cliente =cliente)
            carro.save()
            
        return HttpResponse('Teste')