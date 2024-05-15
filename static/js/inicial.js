function mascara(){
    const cpf = document.getElementById('cpf');
    const value = cpf.value;

    if(isNaN(value[value.length-1])){
        cpf.value = value.substring(0, value.length-1);
        return;
    }
    
    cpf.setAttribute("maxlength", "14");
    if (value.length == 3 || value.length == 7){
        cpf.value += ".";
    }
    
    if (value.length == 11){
        cpf.value += "-";
    }
    console.log();
}

function enviar() {
    const cpf = document.getElementById('cpf');
    const resultado_placeholder = document.getElementById('resultado_pesquisa');

    if(resultado_placeholder.innerHTML.length > 0){
        resultado_placeholder.innerHTML = '';
    }

    resultado_placeholder.innerHTML = [
        '<div class="spinner-border justify-content-center align-content-center" role="status">',
            '<span class="visually-hidden">Loading...</span>',
        '</div>'
    ].join('');

    fetch(`/interno/pesquisa_cpf?cpf=${cpf.value}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao buscar CPF');
        }
        return response.json();
    })
    .then(data => {
        resultado_placeholder.innerHTML = '';
        console.log(data);
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
        
    })
    .catch(error => {
        document.getElementById('resultado_pesquisa').innerHTML = 'CPF não encontrado.';
        console.error(error);
    });
}

function exibir(){

}

function principal(){
    mascara();
    enviar();
    exibir();
}