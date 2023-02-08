function add_carro() {
    container = document.getElementById("form-carro");

    html = `<br />
            <div class="row">
            <div class="col-md">
                <input type="text" class="form-control" name="carro"  placeholder="Carro"/>
            </div>
            <div class="col-md">
                <input type="text" class="form-control" name="placa"  placeholder="Placa" />
            </div>
            <div class="col-md">
                <input type="number" class="form-control" name="ano"  placeholder="Ano"/>
            </div>
            </div>`;

    container.innerHTML += html;
}

function exibir_form(tipo) {
    add_cliente = document.getElementById('adicionar-cliente')
    att_cliente = document.getElementById('att_cliente')

    if (tipo == "1") {
        att_cliente.style.display = "none"
        add_cliente.style.display = "block"
    } else if (tipo == "2") {
        att_cliente.style.display = "block"
        add_cliente.style.display = "none"
    }

}

function dados_cliente() {
    cliente = document.getElementById('cliente-select')
    csrf_token = document.querySelector('[name = csrfmiddlewaretoken]').value

    id_cliente = cliente.value
    data = new FormData()
    data.append('id_cliente', id_cliente)

    fetch("/clientes/atualiza_cliente/", {
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: data
    }).then(function (result) {
        return result.json()
    }).then(function (data) {

        document.getElementById('form-att-cliente').style.display = 'block'

        id = document.getElementById('id')
        id.value = data['cliente_id']

        nome = document.getElementById('nome')
        nome.value = data['cliente']['nome']

        sobrenome = document.getElementById('sobrenome')
        sobrenome.value = data['cliente']['sobrenome']

        cpf = document.getElementById('cpf')
        cpf.value = data['cliente']['cpf']

        email = document.getElementById('email')
        email.value = data['cliente']['email']

        div_carros = document.getElementById('carros')
        // Limpar formulário
        div_carros.innerHTML = ""

        for (i = 0; i < data['carros'].length; i++) {

            carro_cliente = data['carros'][i]['fields']['carro']
            placa_carro = data['carros'][i]['fields']['placa']
            ano_carro = data['carros'][i]['fields']['ano']
            id_carro = data['carros'][i]['id']

            div_carros.innerHTML += `<br />
                                    <form action="/clientes/update_carro/${id_carro}" method = "POST">
                                    <div class="row">
                                    <div class="col-md">
                                    <input type="text" class="form-control" name="carro" value = "${carro_cliente}"/>
                                    </div>
                                    <div class="col-md">
                                    <input type="text" class="form-control" name="placa" value = "${placa_carro}"/>
                                    </div>
                                    <div class="col-md">
                                    <input type="number" class="form-control" name="ano"value = "${ano_carro}"/>
                                    </div>
                                    <div class="col-md d-flex justify-content-end pr-0">
                                    <input type="submit" class="btn btn-success"  value ="Atualizar Carro"></input>
                                    </div>
                                    </form>
                                    <div class="col-md">
                                    <a href='/clientes/excluir_carro/${id_carro}' class="btn btn-outline-danger" >Excluir</a>
                                    </div>
                                    </div>`
        }
    })
}

function update_cliente() {
    nome = document.getElementById('nome').value
    sobrenome = document.getElementById('sobrenome').value
    email = document.getElementById('email').value
    cpf = document.getElementById('cpf').value
    id = document.getElementById('id').value

    fetch('/clientes/update_cliente/' + id, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({
            nome: nome,
            sobrenome: sobrenome,
            email: email,
            cpf: cpf
        })
    }).then(function (result) {
        return result.json()
    }).then(function (data) {
        console.log(data)
    })

}