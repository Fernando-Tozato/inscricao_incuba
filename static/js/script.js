let form_vazio = true;
let cpf_invalido = true;
let data_nasc_invalida = true;
let data_emissao_invalida = true;
let email_invalido = true;
let cep_invalido = true;
let ddd_tel_invalido = true;
let ddd_cel_invalido = true;
let idade;

function form_valido(){
    if(form_vazio || cpf_invalido || data_invalida || email_invalido || cep_invalido || ddd_invalido){
        return false
    }
    return true
}

function verifica_form(){
    let vazio = true;
    const inputs = document.getElementsByClassName('required');
    const placeholder = document.getElementById('preenchido_placeholder');

    for (var i = 0; i < inputs.length - 1; i++) {
        if (inputs[i].value !== '') {
            vazio = false;
        } else {
            vazio = true;
        }
    }

    if(!vazio && document.getElementById('termos').checked != true){
        vazio = true;
    }

    if(vazio && placeholder.innerHTML.length == 0){
        placeholder.innerHTML = [
            '<div class="alert alert-danger d-flex align-items-center mt-3" role="alert">',
                '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-3" role="img" aria-label="Danger:" style="color: #b20101;"></i>',
                '<div>Preencha todos os campos marcados como obrigatórios (*) antes de enviar o formulário!</div>',
            '</div>'
        ].join('');
        console.log('vazio');
        form_vazio = true;
    } 
    else {
        placeholder.innerHTML = '';
        console.log('dados ok');
        form_vazio = false;
    }
}

function verifica_cpf(cpf){
    let invalido = true;
    let inscrito = true;

    const placeholder = document.getElementById('cpf_placeholder');
    const invalidos = ['00000000000', '11111111111', '22222222222', '33333333333', '44444444444', '55555555555', '66666666666', '77777777777', '88888888888', '99999999999'];

    if(cpf.length === 11){
        let soma = 0;
        let resto;
        for(let i = 0; i < 9; i++){
            soma += parseInt(cpf[i]) * (10 - i);
        }
        if((soma * 10) % 11 < 10) {
            resto = (soma * 10) % 11;
        } else {
            resto = 0;
        }

        if(resto == cpf[-2]){
            soma = 0;
            resto = 0;
            for(let i = 0; i < 10; i++){
                soma += parseInt(cpf[i]) * (11 - i);
            }
            if((soma * 10) % 11 < 10) {
                resto = (soma * 10) % 11;
            } else {
                resto = 0;
            }

            if(resto == cpf[-1]){
                invalido = false;
            }
        }
    }

    if(invalido){
        placeholder.innerHTML = [
            '<div class="alert alert-warning d-flex align-items-center mt-3" role="alert">',
                '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-2" role="img" aria-label="Danger:" style="color: #cfac2a;"></i>',
                '<div>CPF inválido! Verifique se foi digitado corretamente.</div>',
            '</div>'
        ].join('');
        cpf_invalido = true;
    } 
    else {
        placeholder.innerHTML = '';
        cpf_invalido = false;

        fetch(window.location.href + 'api/aluno/?format=json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar o arquivo JSON');
            }
            return response.json();
        })
        .then(data => {
            const alunos = data;
            alunos.forEach(aluno => {
                if(cpf.join('') === aluno.cpf.replace(/\D/g, '')){
                    inscrito = true;
                }
            });

            if(inscrito){
                placeholder.innerHTML = [
                    '<div class="alert alert-danger d-flex align-items-center mt-3" role="alert">',
                        '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-2" role="img" aria-label="Danger:" style="color: #b20101;"></i>',
                        '<div>O CPF digitado já foi cadastrado.</div>',
                    '</div>'
                ].join('');
                cpf_invalido = true;
            } else {
                placeholder.innerHTML = '';
                cpf_invalido = false;
            }
        })
        .catch(error => {
            console.error('Erro:', error);
        });
    }
}

function verifica_data_nasc(data){
    const dia = data[0];
    const mes = data[1];
    const ano = data[2];
    const placeholder = document.getElementById('data_nasc_placeholder');

    let invalido = true;
    let aviso;
    
    idade = moment().diff(moment(data, 'DD/MM/YYYY'), 'years')
    console.log(idade)
    
    if(parseInt(ano) < 1900){
        aviso = 'Essa data é muito antiga. Verifique se foi digitada corretamente.';
    } 
    else if(!moment(data, 'DD/MM/YYYY').isValid()){
        aviso = 'A data não é válida. Verifique se foi digitada corretamente.';
    } 
    else if(idade < 12){
        aviso = 'A idade mínima para se inscrever é 12 anos.'
    }
    else {
        invalido = false;
    }

    if(invalido){
        placeholder.innerHTML = [
            '<div class="alert alert-warning d-flex align-items-center mt-3" role="alert">',
                '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-2" role="img" aria-label="Danger:" style="color: #cfac2a;"></i>',
                `<div>${aviso}</div>`,
            '</div>'
        ].join('');
        data_nasc_invalida = true;
    } else {
        placeholder.innerHTML = '';
        data_nasc_invalida = false;
    }
}

function verifica_data_emissao(data){
    const dia = data[0];
    const mes = data[1];
    const ano = data[2];
    const placeholder = document.getElementById('data_emissao_placeholder');

    let invalido = true;
    let aviso;

    if(parseInt(ano) < 1900){
        aviso = 'Essa data é muito antiga. Verifique se foi digitada corretamente.';
    } 
    else if(!moment(data, 'DD/MM/YYYY').isValid()){
        aviso = 'A data não é válida. Verifique se foi digitada corretamente.';
    } 
    else {
        invalido = false
    }

    if(invalido){
        placeholder.innerHTML = [
            '<div class="alert alert-warning d-flex align-items-center mt-3" role="alert">',
                '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-2" role="img" aria-label="Danger:" style="color: #cfac2a;"></i>',
                `<div>${aviso}</div>`,
            '</div>'
        ].join('');
        data_emissao_invalida = true;
    } else {
        placeholder.innerHTML = '';
        data_emissao_invalida = false;
    }
}

function verifica_email(email){
    const placeholder = document.getElementById('email_placeholder');

    let invalido = true;

    if(email.value !== ''){
        usuario = email.substring(0, email.indexOf("@"));
        dominio = email.substring(email.indexOf("@") + 1, email.length);

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
            invalido = false;
        } else {
            invalido = true;
        }
    }
    
    placeholder.innerHTML = '';
    if(invalido){
        placeholder.innerHTML = [
            '<div class="alert alert-warning d-flex align-items-center mt-3" role="alert">',
                '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-2" role="img" aria-label="Danger:" style="color: #cfac2a;"></i>',
                '<div>E-mail inválido. Verifique se foi digitado corretamente.</div>',
            '</div>'
        ].join('');
        email_invalido = true;
    } else {
        email_invalido = false;
    }
}

function verifica_cep(cep){
    const placeholder = document.getElementById('cep_placeholder');

    let invalido = true;

    if(cep.length === 8){
        fetch('https://viacep.com.br/ws/'+ cep + '/json')
        .then(response => {
            if (!response.ok) {
                placeholder.innerHTML = [
                    '<div class="alert alert-danger d-flex align-items-center mt-3" role="alert">',
                        '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-2" role="img" aria-label="Danger:" style="color: #b20101;"></i>',
                        '<div>O CEP digitado não é válido. Verifique se foi digitado corretamente.</div>',
                    '</div>'
                ].join('');
                cef_invalido = true;
            } else {
                placeholder.innerHTML = '';
                cef_invalido = false;
            }
        })
        .then(data => {
            const conteudo = data;
            
            document.getElementById('rua').value=(conteudo.logradouro);
            document.getElementById('bairro').value=(conteudo.bairro);
            document.getElementById('cidade').value=(conteudo.localidade);
            document.getElementById('uf').value=(conteudo.uf);

            document.getElementById('rua').disabled=true;
            document.getElementById('bairro').disabled=true;
            document.getElementById('cidade').disabled=true;
            document.getElementById('uf').disabled=true;
        })
        .catch(error => {
            console.error('Erro:', error);
        });
    }

    if(invalido){
        placeholder.innerHTML = [
            '<div class="alert alert-danger d-flex align-items-center mt-3" role="alert">',
                '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-2" role="img" aria-label="Danger:" style="color: #b20101;"></i>',
                '<div>O CEP digitado não é válido. Verifique se foi digitado corretamente.</div>',
            '</div>'
        ].join('');
        cef_invalido = true;
    } else {
        placeholder.innerHTML = '';
        cef_invalido = false;
    }
}

function verifica_ddd_tel(tel){

}

function verifica_ddd_cel(cel){

}

// MÁSCARAS

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