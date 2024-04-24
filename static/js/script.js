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
    cpf = cpf.value.replace(/\D/g, '');
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

document.addEventListener('DOMContentLoaded', function() {
    habilitar_cursos();
});

let turmas;

function habilitar_cursos() {
    const select_curso = document.getElementById('curso');
    let cursos = [];

    fetch(window.location.href + 'api/turma/?format=json')
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao carregar o arquivo JSON');
        }
        return response.json();
    })
    .then(data => {
        turmas = data;
        turmas.forEach(turma => {
            if(!cursos.includes(turma.curso)){
                cursos.push(turma.curso);
            }
        });

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

let curso;

function habilitar_dias(selected){
    const select_dias = document.getElementById('dias');
    curso = selected.value;
    let dias = [];

    turmas.forEach(turma =>{
        if(!dias.includes(turma.dias) && turma.curso === curso){
            dias.push(turma.dias);
        }
    });

    select_dias.innerHTML = '<option selected disabled hidden></option>'
    document.getElementById('horario').innerHTML = '<option selected disabled hidden></option>'

    dias.forEach(dia => {
        let new_opt = document.createElement("option");
        new_opt.text = dia;
        new_opt.value = dia;
        new_opt.setAttribute('curso_escolhido', curso);
        select_dias.appendChild(new_opt);
    });
    select_dias.disabled = false;
}

function habilitar_horarios(selected){
    const select_horario = document.getElementById('horario');
    let dias = selected.value;
    let horarios = [];

    turmas.forEach(turma => {
        let entrada = turma.horario_entrada.split(':');
        let saida = turma.horario_saida.split(':');
        let horario = `${entrada[0]}:${entrada[1]} - ${saida[0]}:${saida[1]}`;

        if(!horarios.includes(horario) && turma.dias === dias && turma.curso === curso){
            horarios.push(horario);
        }
    });

    select_horario.innerHTML = '<option selected disabled hidden></option>'

    horarios.forEach(horario => {
        let new_opt = document.createElement("option");
        new_opt.text = horario;
        new_opt.value = horario;
        select_horario.appendChild(new_opt);
    });
    select_horario.disabled = false;
}

function verificar_inputs(){
    var preenchido = false;
    var inputs = document.getElementsByClassName('required');
    const placeholder = document.getElementById('alert_placeholder');

    for (var i = 0; i < inputs.length - 1; i++) {
        if (inputs[i].value === '') {
            console.log(i)
            preenchido = false;
            break;
        } else {
            preenchido = true
        }
    }

    if(document.getElementById('termos').checked != true){
        preenchido = false;
    }

    if(!preenchido && placeholder.innerHTML.length == 0){
        document.getElementById('danger_badge').innerHTML = ''
        placeholder.innerHTML = [
            '<div class="alert alert-danger d-flex align-items-center mt-3" role="alert">',
                '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-3" role="img" aria-label="Danger:" style="color: #b20101;"></i>',
                '<div>Preencha todos os campos marcados como obrigatórios (*) antes de enviar o formulário!</div>',
            '</div>'
        ].join('');
        console.log('erro dados');
    } else if(preenchido){
        placeholder.innerHTML = '';
        console.log('dados ok');
        enviar_dados();
    } else {
        console.log('erro dados');
    }
}

function enviar_dados(){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    let nasc = document.getElementById('nascimento').value.split('/');
    let dt_emissao = document.getElementById('data_emissao').value.split('/')

    let id_turma;
    const dias = document.getElementById('dias').value;
    const horario_escolhido = document.getElementById('horario').value;
    turmas.forEach(turma => {
        let entrada = turma.horario_entrada.split(':');
        let saida = turma.horario_saida.split(':');
        let horario = `${entrada[0]}:${entrada[1]} - ${saida[0]}:${saida[1]}`;

        if(turma.curso === curso && turma.dias === dias && horario === horario_escolhido){
            id_turma = turma.id;
        }
    });

    const dados = {
        "nome": document.getElementById('nome').value,
        "nascimento": `${nasc[2]}-${nasc[1]}-${nasc[0]}`,
        "cpf": document.getElementById('cpf').value,
        "rg": document.getElementById('rg').value,
        "data_emissao": `${dt_emissao[2]}-${dt_emissao[1]}-${dt_emissao[0]}`,
        "orgao_emissor": document.getElementById('orgao_emissor').value,
        "uf_emissao": document.getElementById('uf_emissao').value,
        "nome_mae": document.getElementById('nome_mae').value,
        "nome_pai": document.getElementById('nome_pai').value,
        "escolaridade": document.getElementById('escolaridade').value,
        "email": document.getElementById('email').value,
        "telefone": document.getElementById('telefone').value,
        "celular": document.getElementById('celular').value,
        "cep": document.getElementById('cep').value,
        "rua": document.getElementById('rua').value,
        "numero": document.getElementById('numero').value,
        "complemento": document.getElementById('complemento').value,
        "bairro": document.getElementById('bairro').value,
        "cidade": document.getElementById('cidade').value,
        "uf": document.getElementById('uf').value,
        "id_turma": id_turma
    };

    console.log(dados);

    fetch(window.location.href + 'api/aluno/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dados)
    })
    .then(response => {
        if (!response.ok) {
            const placeholder = document.getElementById('erro_placeholder');
            if(placeholder.innerHTML == ''){
                placeholder.innerHTML = [
                    '<div class="alert alert-danger d-flex align-items-center mt-3" role="alert">',
                        '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-3" role="img" aria-label="Danger:" style="color: #b20101;"></i>',
                        '<div>Atenção! Seu formulário de inscrição não pôde ser enviado. Tente novamente mais tarde.</div>',
                    '</div>'
                ].join('');
            }
            console.log(response);
            throw new Error('Erro ao enviar o formulário');
        } else {
            console.log('dados enviados');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
}