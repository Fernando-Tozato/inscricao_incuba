function mascara_cpf(i){
    const v = i.value;
    
    if(isNaN(v[v.length-1])){
        i.value = v.substring(0, v.length-1);
        return;
    }
    
    i.setAttribute("maxlength", "14");
    if (v.length == 3 || v.length == 7){
        i.value += ".";
    }
    
    if (v.length == 11){
        i.value += "-";
    }
}

function mascara_rg(i){
    const v = i.value;

    if(isNaN(v[v.length-1])){
        i.value = v.substring(0, v.length-1);
        return;
    }

    i.setAttribute("maxlength", "12");
    if (v.length == 2 || v.length == 6){
        i.value += ".";
    }

    if(v.length == 10){
        i.value += "-";
    }
}

function mascara_tel(i){
    const v = i.value;

    if(isNaN(v[v.length-1])){
        i.value = v.substring(0, v.length-1);
        return;
    }

    i.setAttribute("maxlength", "14");
    if (v.length == 2){
        i.value = '(' + i.value + ') '
    }

    if(v.length == 9){
        i.value += "-";
    }
}

function mascara_cel(i){
    const v = i.value;

    if(isNaN(v[v.length-1])){
        i.value = v.substring(0, v.length-1);
        return;
    }

    i.setAttribute("maxlength", "16");
    if (v.length == 2){
        i.value = '(' + i.value + ') '
    }

    if(v.length == 6){
        i.value+=' ';
    }

    if(v.length == 11){
        i.value += "-";
    }
}

function mascara_data(i){
    const v = i.value;

    if(isNaN(v[v.length-1])){
        i.value = v.substring(0, v.length-1);
        return;
    }

    i.setAttribute("maxlength", "10");
    if (v.length == 2 || v.length == 5){
        i.value += "/";
    }
}

function mascara_cep(i){
    const v = i.value;

    if(isNaN(v[v.length-1])){
        i.value = v.substring(0, v.length-1);
        return;
    }

    i.setAttribute("maxlength", "10");
    if (v.length == 2){
        i.value += ".";
    }

    if(v.length == 6){
        i.value += "-";
    }
}

function callback(conteudo){
    const placeholder = document.getElementById('cep_placeholder');
    if (!("erro" in conteudo)) {
        document.getElementById('rua').value=(conteudo.logradouro);
        document.getElementById('bairro').value=(conteudo.bairro);
        document.getElementById('cidade').value=(conteudo.localidade);
        document.getElementById('uf').value=(conteudo.uf);

        document.getElementById('rua').disabled=true;
        document.getElementById('bairro').disabled=true;
        document.getElementById('cidade').disabled=true;
        document.getElementById('uf').disabled=true;

        placeholder.innerHTML = '';
    } else if(placeholder.innerHTML.length == 0){
        placeholder.innerHTML = [
            '<div class="alert alert-warning d-flex align-items-center mt-3" role="alert">',
                '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-2" role="img" aria-label="Danger:" style="color: #cfac2a;"></i>',
                '<div>CEP inválido. Verifique se foi digitado corretamente.</</div>',
            '</div>'
        ].join('');
    }
}

function achar_cep(cep){
    const placeholder = document.getElementById('cep_placeholder');

    if(cep != ""){
        const validacep = /^[0-9]{8}$/;

        if(validacep.test(cep)){
            const script = document.createElement('script');

            script.src = 'https://viacep.com.br/ws/'+ cep + '/json/?callback=callback';
            
            document.body.appendChild(script);
        } else if(placeholder.innerHTML.length == 0){
            placeholder.innerHTML = [
                '<div class="alert alert-warning d-flex align-items-center mt-3" role="alert">',
                    '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-2" role="img" aria-label="Danger:" style="color: #cfac2a;"></i>',
                    '<div>CEP inválido. Verifique se foi digitado corretamente.</div>',
                '</div>'
            ].join('');
        }
    }
}

function validar_cpf(cpf){
    const placeholder = document.getElementById('cpf_placeholder');
    
    if (cpf.length === 0){
        return;
    } else if (cpf.length === 11){
        let soma = 0;
        for(let i=0; i<9; i++){
            soma += parseInt(cpf.charAt(i)) * (10 - i);
        }
        let resto = 11 - (soma % 11);
        if (resto === 10 || resto === 11) {
            resto = 0;
        }
        if (resto === parseInt(cpf.charAt(9))) {
            soma = 0;
            for (let i = 0; i < 10; i++) {
                soma += parseInt(cpf.charAt(i)) * (11 - i);
            }
            resto = 11 - (soma % 11);
            if (resto === 10 || resto === 11) {
                resto = 0;
            }
            if (resto === parseInt(cpf.charAt(10))) {
                placeholder.innerHTML = ''
                return;
            }
        }
    }
    placeholder.innerHTML = [
        '<div class="alert alert-warning d-flex align-items-center mt-3" role="alert">',
            '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-2" role="img" aria-label="Danger:" style="color: #cfac2a;"></i>',
            '<div>CPF inválido. Verifique se foi digitado corretamente.</div>',
        '</div>'
    ].join('');
}

function verificar_email(email){
    const placeholder = document.getElementById('contatos_placeholder');

    usuario = email.value.substring(0, email.value.indexOf("@"));
    dominio = email.value.substring(email.value.indexOf("@") + 1, email.value.length);

    if ((usuario.length >= 1) &&
        (dominio.length >= 3) &&
        (usuario.search("@") == -1) &&
        (dominio.search("@") == -1) &&
        (usuario.search(" ") == -1) &&
        (dominio.search(" ") == -1) &&
        (dominio.search(".") != -1) &&
        (dominio.indexOf(".") >= 1) &&
        (dominio.lastIndexOf(".") < dominio.length - 1))
    {
        placeholder.innerHTML = '';
    } else {
        placeholder.innerHTML = [
            '<div class="alert alert-warning d-flex align-items-center mt-3" role="alert">',
                '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-2" role="img" aria-label="Danger:" style="color: #cfac2a;"></i>',
                '<div>E-mail inválido. Verifique se foi digitado corretamente.</div>',
            '</div>'
        ].join('');
    }
}

function enviar(){
    var preenchido = false;
    var inputs = document.getElementsByClassName('required');
    const placeholder = document.getElementById('alert_placeholder');

    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].value === '') {
            preenchido = false;
            break;
        }
    }

    if(!preenchido && placeholder.innerHTML.length == 0){
        document.getElementById('danger_badge').innerHTML = ''
        placeholder.innerHTML = [
            '<div class="alert alert-danger d-flex align-items-center mt-3" role="alert">',
                '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-3" role="img" aria-label="Danger:" style="color: #b20101;"></i>',
                '<div>Preencha todos os campos marcados como obrigatórios (*) antes de enviar o formulário!</div>',
            '</div>'
        ].join('');
    }

    return preenchido;
}

document.addEventListener('DOMContentLoaded', function() {
    habilitar_cursos();
    document.getElementById('form').addEventListener('submit', function(event) {
        if (!enviar()) {
            event.preventDefault();
            console.log('não enviado');
            return;
        }
        console.log('enviado');
    });
});

function habilitar_cursos() {
    let cursos = [];

    fetch(window.location.href + 'api/turma/?format=json')
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao carregar o arquivo JSON');
        }
        return response.json();
    })
    .then(data => {
        const turmas = data;
        turmas.forEach(turma => {
            if(!cursos.includes(turma.curso)){
                cursos.push(turma.curso);
            }
        });

        const select_curso = document.getElementById('curso');
        cursos.forEach(curso => {
            let new_opt = document.createElement("option");
            new_opt.text = curso;
            new_opt.value = curso;
            select_curso.appendChild(new_opt);
        });
        select_curso.disabled = false;
    })
    .catch(error => {
        console.error('Erro:', error);
    });
}