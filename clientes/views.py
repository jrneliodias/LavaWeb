from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse,JsonResponse
from .models import Cliente, Carro
import re, json
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import constants

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
    
    cliente_str= serialize('json',cliente)
    carros_cliente_str = serialize('json',carros_cliente)
    
    # Como cliente é apenas um com esse id, então
    cliente_json = json.loads(cliente_str)[0]['fields']
    cliente_id = json.loads(cliente_str)[0]['pk']

    # O carro temos uma lista de carros, então devemos criar um dicionário
    cliente_carros_json = json.loads(carros_cliente_str)
    cliente_carros_json = [{'id': carro['pk'], 'fields':carro['fields']} for carro in cliente_carros_json]
    data = {'cliente': cliente_json,'cliente_id': cliente_id, 'carros':cliente_carros_json}
    
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
    
    #atualizar os dados carro
    carro.carro = nome_carro
    carro.placa = placa_carro
    carro.ano = ano_carro
    carro.save()
    
    return HttpResponse('Carro atualizado com sucesso')

def excluir_carro(request,id):
    try:
        carro = Carro.objects.get(id = id)
        carro.delete()
        return redirect(reverse('clientes') + f'?aba=att_cliente&id_cliente={id}')
    
    except:
        return redirect(reverse('clientes') + f'?aba=att_cliente&id_cliente={id}')
    
def update_cliente(request,id):
    
    body        = json.loads(request.body)
    nome        = body['nome']
    sobrenome   = body['sobrenome']
    cpf         = body['cpf']
    email       = body['email']
    
    cliente = get_object_or_404(Cliente,id=id)
    try:    
        cliente.nome = nome
        cliente.sobrenome = sobrenome
        cliente.cpf = cpf
        cliente.email = email
        cliente.save()
        messages.add_message(request,constants.SUCCESS, "Cliente atualizado com sucesso!")
        
        return JsonResponse({'status':'200',
                             'nome': nome,
                             'sobrenome': sobrenome,
                             'email':email,
                             'cpf':cpf})
    except:
        return JsonResponse({'status': '500'})