function add_carro() {
    container = document.getElementById("form-carro");

    html = `<br />
            <div class="row">
            <div class="col-md">
                <input type="text"o" class="form-control" name="carro" />
            </div>
            <div class="col-md">
                <input type="text"a" class="form-control" name="placa" />
            </div>
            <div class="col-md">
                <input type="number" class="form-control" name="ano" />
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
                                    <div class="col-md">
                                    <input type="submit" class="btn btn-success" value ="Atualizar"></input>
                                    </div>
                                    </div>
                                    </form>`
        }
    })
}