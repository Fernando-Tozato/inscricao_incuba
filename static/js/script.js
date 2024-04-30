let form_vazio = true;
let cpf_invalido = true;
let data_nasc_invalida = true;
let data_emissao_invalida = true;
let email_invalido = true;
let cep_invalido = true;
let ddd_tel_invalido = true;
let ddd_cel_invalido = true;
let idade;
let escolaridade;
let turma;
let curso;
let dias;
let horario;

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
    
    if(parseInt(ano) < 1900){
        aviso = 'Essa data é muito antiga. Verifique se foi digitada corretamente.';
    } 
    else if(!moment(data, 'DD/MM/YYYY').isValid()){
        aviso = 'A data não é válida. Verifique se foi digitada corretamente.';
    } 
    else if(idade < 12){
        aviso = 'A idade mínima para se inscrever é 12 anos.';
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
        idade = moment().diff(moment(data, 'DD/MM/YYYY'), 'years');
        if(escolaridade){
            console.log('1')
            habilitar_cursos();
        }
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
        invalido = false;

        $.getJSON("https://viacep.com.br/ws/"+ cep +"/json/?callback=?", function(dados) {

            if (!("erro" in dados)) {
                $("#rua").val(dados.logradouro);
                $("#bairro").val(dados.bairro);
                $("#cidade").val(dados.localidade);
                $("#uf").val(dados.uf);
                placeholder.innerHTML = '';
                cep_invalido = false;
            }
            else {
                placeholder.innerHTML = [
                    '<div class="alert alert-warning d-flex align-items-center mt-3" role="alert">',
                        '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-2" role="img" aria-label="Danger:" style="color: #cfac2a;"></i>',
                        '<div>O CEP digitado não é válido. Verifique se foi digitado corretamente.</div>',
                    '</div>'
                ].join('');
                cep_invalido = true;
            }
        });
    }

    if(invalido){
        placeholder.innerHTML = [
            '<div class="alert alert-warning d-flex align-items-center mt-3" role="alert">',
                '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-2" role="img" aria-label="Danger:" style="color: #cfac2a;"></i>',
                '<div>O CEP digitado não é válido. Verifique se foi digitado corretamente.</div>',
            '</div>'
        ].join('');
        cep_invalido = true;
    } else {
        placeholder.innerHTML = '';
        cep_invalido = false;
    }
}

function verifica_ddd_tel(ddd){
    const placeholder = document.getElementById('tel_placeholder');

    fetch('https://brasilapi.com.br/api/ddd/v1/' + ddd)
    .then(response => {
        if (!response.ok) {
            placeholder.innerHTML = [
                '<div class="alert alert-warning d-flex align-items-center mt-3" role="alert">',
                    '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-2" role="img" aria-label="Danger:" style="color: #cfac2a;"></i>',
                    '<div>O DDD inserido não é válido. Verifique se foi digitado corretamente.</div>',
                '</div>'
            ].join('');
            cep_invalido = true;
        } else {
            placeholder.innerHTML = '';
            cep_invalido = false;
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
}

function verifica_ddd_cel(ddd){
    const placeholder = document.getElementById('cel_placeholder');

    fetch('https://brasilapi.com.br/api/ddd/v1/' + ddd)
    .then(response => {
        if (!response.ok) {
            placeholder.innerHTML = [
                '<div class="alert alert-warning d-flex align-items-center mt-3" role="alert">',
                    '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-2" role="img" aria-label="Danger:" style="color: #cfac2a;"></i>',
                    '<div>O DDD inserido não é válido. Verifique se foi digitado corretamente.</div>',
                '</div>'
            ].join('');
            cep_invalido = true;
        } else {
            placeholder.innerHTML = '';
            cep_invalido = false;
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
}

function set_escolaridade(v){
    escolaridade = v;
    habilitar_cursos();
}

function set_horario(v){
    horario = v;
    console.log(curso, dias, horario)
}

function habilitar_cursos(){
    const select_curso = document.getElementById('curso');
    const placeholder = document.getElementById('curso_placeholder');

    let cursos = [];

    select_curso.innerHTML = '<option selected disabled hidden></option>';
    document.getElementById('dias').innerHTML = '<option selected disabled hidden></option>';
    document.getElementById('horario').innerHTML = '<option selected disabled hidden></option>';

    fetch(window.location.href + 'api/turma/?format=json')
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao carregar o arquivo JSON');
        }
        return response.json();
    })
    .then(data => {
        turmas = data;
        if(escolaridade && idade){
            turmas.forEach(turma => {
                if(!cursos.includes(turma.curso) && parseInt(turma.idade) <= idade && parseInt(turma.escolaridade) <= escolaridade){
                    cursos.push(turma.curso);
                }
            });
        }
        else {
            turmas.forEach(turma => {
                if(!cursos.includes(turma.curso)){
                    cursos.push(turma.curso);
                }
            });
        }

        if(cursos.length == 0){
            placeholder.innerHTML = [
                '<div class="alert alert-warning d-flex align-items-center mt-3" role="alert">',
                    '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-2" role="img" aria-label="Danger:" style="color: #cfac2a;"></i>',
                    '<div>Não temos nenhum curso disponível para a sua idade ou escolaridade.</div>',
                '</div>'
            ].join('');
            select_curso.disabled = true;
        } else {
            placeholder.innerHTML = '';
            cursos.forEach(opt_curso => {
                let new_opt = document.createElement("option");
                new_opt.text = opt_curso;
                new_opt.value = opt_curso;
                select_curso.appendChild(new_opt);
            });
            select_curso.disabled = false;
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
}

function habilitar_dias(selected){
    const select_dias = document.getElementById('dias');
    let dias = [];
    curso = selected.value;

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
}

function habilitar_horarios(selected){
    const select_horario = document.getElementById('horario');
    let horarios = [];
    dias = selected.value;

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

function mascara_palavras(i){
    let nome = i.value;

    nome = nome.replace(/[^a-zà-ú'-,. ]+$/i, '');

    nome = nome.toLowerCase().split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');

    i.value = nome;
}