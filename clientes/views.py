from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Cliente, Carro
import re
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
# views here.
def clientes(request):
    if request.method == "GET":
        clientes_list = Cliente.objects.all()
        return render(request,'clientes.html',
                      {'clientes':clientes_list})
    
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
                                 'email': email,
                                 'carros': zip(carros,placas,anos)})
        
        email_validation = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        
        if not re.fullmatch(re.compile(email_validation), email):
            return render(request,'clientes.html',
                                {'nome':nome,
                                 'sobrenome':sobrenome,
                                 'cpf': cpf,
                                 'carros': zip(carros,placas,anos)})
        
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

   
def att_cliente(request):
    id_cliente = request.POST.get('id_cliente')
    cliente = Cliente.objects.filter(id = id_cliente)
    carros_cliente = Carro.objects.filter(cliente = cliente[0])
    
    cliente_str= serializers.serialize('json',cliente)
    carros_cliente_str = serializers.serialize('json',carros_cliente)
    
    # Como cliente é apenas um com esse id, então
    cliente_json = json.loads(cliente_str)[0]['fields']
    # O carro temos uma lista de carros, en
    cliente_carros_json = json.loads(carros_cliente_str)
    cliente_carros_json = [{'id': carro['pk'], 'fields':carro['fields']} for carro in cliente_carros_json]
    data = {'cliente': cliente_json,'carros':cliente_carros_json}
    
    return JsonResponse(data)


@csrf_exempt
def update_carro(request,id):
    nome_carro = request.POST.get('carro')
    placa_carro = request.POST.get('placa')
    ano_carro = request.POST.get('ano')
    
    carro = Carro.objects.get(id=id)
    list_carros = Carro.objects.exclude(id = id).filter(placa=placa_carro)
    if list_carros.exists():
        return HttpResponse('Placa do carro já existe')
    
    carro.carro = nome_carro
    carro.placa = placa_carro
    carro.ano = ano_carro
    carro.save()
    return HttpResponse('Carro atualizado com sucesso')
