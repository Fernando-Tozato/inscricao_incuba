let turmas;
let input_nascimento;
let input_cpf;
let select_escolaridade;
let input_cep;
let select_curso;
let select_dias;
let select_horario;
let idade;
let escolaridade;

document.addEventListener('DOMContentLoaded', function ()  {
    turmas = window.turmas;
    input_nascimento = document.getElementById('id_nascimento');
    input_cpf = document.getElementById('id_cpf');
    select_escolaridade = document.getElementById('id_escolaridade');
    input_cep = document.getElementById('id_cep');
    select_curso = document.getElementById('id_curso');
    select_dias = document.getElementById('id_dias');
    select_horario = document.getElementById('id_horario');

    adicionar_mascaras();
    adicionar_validacao([input_nascimento, input_cpf, select_escolaridade,
            input_cep, select_curso, select_dias]);

    input_nascimento.addEventListener('blur', () => {
        let value = input_nascimento.value;

        if(value==='') {
            input_nascimento.classList.add('is-invalid');
            invalid_message(input_nascimento,'Data de nascimento é um campo obrigatório.');
            return;
        } else if(value.replace(/\D/g, '').length !== 8) {
            input_nascimento.classList.add('is-invalid');
            invalid_message(input_nascimento, 'Data inválida, verifique se foi escrita da maneira correta.');
            return
        }

        let data = value.split('/');

        try {
            idade = moment().diff(moment(data, 'DD/MM/YYYY'), 'years');
        } finally {
            if (idade && escolaridade) {
                definir_cursos();
            }
        }
    });

    input_cpf.addEventListener('blur', () => {
        let cpf = input_cpf.value.replace(/\D/g, '');

        if(cpf==='') {
            input_cpf.classList.add('is-invalid');
            invalid_message(input_cpf,'CPF é um campo obrigatório.');
        } else if(cpf.length !== 11 || !validar_cpf(cpf)) {
            input_cpf.classList.add('is-invalid');
            invalid_message(input_cpf, 'CPF inválido, verifique se foi escrita da maneira correta.');
        }
    });

    select_escolaridade.addEventListener('blur', () => {
        escolaridade = select_escolaridade.value;
        if (idade && escolaridade) {
            definir_cursos();
        }
    });

    input_cep.addEventListener('blur', () => {
        let cep = input_cep.value.replace(/\D/g, '');
        console.log('cep', cep);

        if(cep.length===0) {
            input_cep.classList.add('is-invalid');
            invalid_message(input_cep,'CEP é um campo obrigatório.');
            return;
        } else if(cep.length!==8) {
            input_cep.classList.add('is-invalid');
            invalid_message(input_cep, 'CEP inválido, verifique se foi escrita da maneira correta.');
            return;
        }

        preparar_campos();

        $.getJSON("https://viacep.com.br/ws/"+ cep +"/json/?callback=?", function(dados) {
            if (!("erro" in dados)) {
                $("#id_rua").val(dados.logradouro);
                $("#id_bairro").val(dados.bairro);
                $("#id_cidade").val(dados.localidade);
                $("#id_uf").val(dados.uf);
                document.getElementById('rua').disabled = true;
                document.getElementById('bairro').disabled = true;
                document.getElementById('cidade').disabled = true;
                document.getElementById('uf').disabled = true;
                cep_invalido = false;
            }
            else {
                input_cep.classList.add('is-invalid');
                invalid_message(input_cep, 'CEP inválido, verifique se foi escrita da maneira correta.');

                $("#id_rua").val('');
                $("#id_bairro").val('');
                $("#id_cidade").val('');
                $("#id_uf").val('');

                document.getElementById('id_rua').disabled = false
                document.getElementById('id_bairro').disabled = false
                document.getElementById('id_cidade').disabled = false
                document.getElementById('id_uf').disabled = false
            }
            document.getElementById('spinner_cep').hidden = true;
        });
    });

    select_curso.addEventListener('blur', () => {
        let curso = select_curso.value;
        let dias = [];

        if(curso==='') {
            select_curso.classList.add('is-invalid');
            invalid_message(select_curso, 'Curso  é um campo obrigatório.');
            return;
        }

        for (let i = 0; i < turmas.length; i++) {
            let turma = turmas[i];
            if (idade >= turma['idade'] && escolaridade >= turma['escolaridade']) {
                if (curso === turma['curso']) {
                    dias.push(turma['dias']);
                }
            }
        }
        add_options(select_dias, dias);
    });

    select_dias.addEventListener('blur', () => {
        let curso = select_curso.value;
        let dias = select_dias.value;
        let horarios = [];

        if(dias==='') {
            select_dias.classList.add('is-invalid');
            invalid_message(select_dias, 'Dias  é um campo obrigatório.');
            return;
        }

        for (let i = 0; i < turmas.length; i++) {
            let turma = turmas[i];
            if (idade >= turma['idade'] && escolaridade >= turma['escolaridade']) {
                if (curso === turma['curso']) {
                    if (dias === turma['dias']) {
                        horarios.push(turma['horario']);
                    }
                }
            }
        }
        add_options(select_horario, horarios);
    });
});

function definir_cursos(){
    let cursos = [];

    for (let i = 0; i < turmas.length; i++) {
        let turma = turmas[i];
        if (idade >= turma['idade'] && escolaridade >= turma['escolaridade']) {
            cursos.push(turma['curso']);
        }
    }
    add_options(select_curso, cursos);
}

function add_options(select, options){
    select.innerHTML = '<option value selected>Selecione...</option>';
    for(let i = 0; i < options.length; i++) {
        let option = options[i];
        let new_opt = document.createElement('option');
        new_opt.text = option;
        new_opt.value = option;
        select.appendChild(new_opt);
    }
    select.disabled = false;
    console.log(select.disabled)
}

function preparar_campos() {
    let spinner = document.getElementById('spinner_cep');
    let input_rua = document.getElementById('id_rua');
    let input_bairro = document.getElementById('id_bairro');
    let input_cidade = document.getElementById('id_cidade');
    let input_uf = document.getElementById('id_uf');

    spinner.hidden = false

    input_rua.disabled = true
    input_bairro.disabled = true
    input_cidade.disabled = true
    input_uf.disabled = true

    input_rua.value = '...'
    input_bairro.value = '...'
    input_cidade.value = '...'
    input_uf.value = '...'
}

function validar_cpf(cpf) {
  let Soma = 0
  let Resto

  if (cpf.length !== 11)
     return false

  if ([
    '00000000000',
    '11111111111',
    '22222222222',
    '33333333333',
    '44444444444',
    '55555555555',
    '66666666666',
    '77777777777',
    '88888888888',
    '99999999999',
    ].indexOf(cpf) !== -1)
    return false

  for (let i=1; i<=9; i++)
    Soma = Soma + parseInt(cpf.substring(i-1, i)) * (11 - i);

  Resto = (Soma * 10) % 11

  if ((Resto === 10) || (Resto === 11))
    Resto = 0

  if (Resto !== parseInt(cpf.substring(9, 10)) )
    return false

  Soma = 0

  for (let i=1; i<=10; i++)
    Soma = Soma + parseInt(cpf.substring(i-1, i)) * (12 - i)

  Resto = (Soma * 10) % 11

  if ((Resto === 10) || (Resto === 11))
    Resto = 0

  return Resto === parseInt(cpf.substring(10, 11));
}