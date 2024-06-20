let url_cpf = '/interno/?parametro=cpf&valor=';
let url_nome = '/interno/?parametro=nome&valor=';
let csrftoken;

function buscar(busca){
    value = busca.value;

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
    
        window.location.href = url_nome + encodeURIComponent(value);
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

        window.location.href = url_cpf + encodeURIComponent(value);
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
                '<a href="" style="text-decoration: none;" class="text-body-secondary">',
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

            muda_footer();
        }
    } else {
        resultado_placeholder.innerHTML = data.error;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    csrftoken = document.getElementById('token').children[0].value;
    input = document.getElementById('busca');
    input.focus();
    input.setSelectionRange(input.value.length, input.value.length);
});
