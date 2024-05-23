let url_cpf = '/interno/pagina_inicial/pesquisa_cpf/?cpf=';
let url_nome = '/interno/pagina_inicial/pesquisa_nome/?nome=';
let csrftoken;

function buscar(busca){
    const resultado_placeholder = document.getElementById('resultado_pesquisa');
    value = busca.value;
    if(value.length === 0){
        resultado_placeholder.innerHTML = '<h3>Faça uma busca para começar a mostrar resultados.</h3>';
        return;
    }

    resultado_placeholder.innerHTML = [
        '<div class="spinner-border justify-content-center align-content-center" role="status">',
            '<span class="visually-hidden">Loading...</span>',
        '</div>'
    ].join('');

    if(isNaN(value)){
        nome = value.replace(/[^a-zà-ú'-,. ]+$/i, '');
        nome = nome.toLowerCase().split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
        busca.value = nome;

        value = value.replace(/[ÀÁÂÃÄÅ]/gi,'A');
        value = value.replace(/[ÈÉÊË]/gi,'E');
        value = value.replace(/[ÌÍÎÏ]/gi,'I');
        value = value.replace(/[ÒÓÔÕ]/gi,'O');
        value = value.replace(/[ÙÚÛÜ]/gi,'U');
        value = value.replace(/[Ç]/gi,'C');
        value = value.replace(/[Ñ]/gi,'N');
        value = value.replace(/[ÝŸ]/gi,'Y');
        value = value.toUpperCase();
        value = value.replace(/[^A-Z ]/g,'');
        
        fetch(url_nome + value, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao buscar nome');
            }
            return response.json();
        })
        .then(data => {
            exibir_resultado(data);
        })
        .catch(error => {
            document.getElementById('resultado_pesquisa').innerHTML = 'Nome não encontrado.';
            console.error(error);
        });
    } else {
        if(isNaN(value[value.length-1])){
            busca.value = value.substring(0, value.length-1);
            return;
        }
        
        busca.setAttribute("maxlength", "14");
        if (value.length == 3 || value.length == 7){
            busca.value += ".";
        }
        
        if (value.length == 11){
            busca.value += "-";
        }

        fetch(url_cpf + value, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao buscar CPF');
            }
            return response.json();
        })
        .then(data => {
            exibir_resultado(data);
        })
        .catch(error => {
            document.getElementById('resultado_pesquisa').innerHTML = 'CPF não encontrado.';
            console.error(error);
        });
    }
}

function exibir_resultado(data){
    const resultado_placeholder = document.getElementById('resultado_pesquisa');
    resultado_placeholder.innerHTML = '';
    if(data.hasOwnProperty('0')){
        for(const chave in data){
            const resultado = data[chave];
            const nasc = resultado.nascimento.split('-');
            const li = document.createElement('li');
            li.className = 'list-group-item';
            li.innerHTML = [
                '<a href="#" style="text-decoration: none;" class="text-body-secondary">',
                    `<h1>${resultado.nome_social.length == 0 ? resultado.nome : resultado.nome_social}</h1>`,
                    '<div class="row">',
                        '<div class="col-md">',
                            `<h4>${resultado.filiacao}</h4>`,
                        '</div>',
                        '<div class="col-md">',
                            `<h4>${resultado.cpf}</h4>`,
                        '</div>',
                        '<div class="col-md">',
                            `<h4>${nasc[2]}/${nasc[1]}/${nasc[0]}</h4>`,
                        '</div>',
                    '</div>',
                '</a>'
            ].join('');
            resultado_placeholder.appendChild(li);
        }
    } else {
        resultado_placeholder.innerHTML = data.error;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    csrftoken = document.getElementById('token').children[0].value;
});