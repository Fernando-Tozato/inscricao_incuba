let dados;
let input_nascimento;
let input_cpf;
let select_escolaridade;
let input_cep;
let select_unidade;
let select_curso;
let select_dias;
let select_horario;
let select_turma;
let idade;
let escolaridade;

const hierarchy = {
    'N_ALF': 0,
    'ALF': 1,
    'EF1_INC': 2,
    'EF1_COM': 3,
    'EF2_INC': 4,
    'EF2_COM': 5,
    'EM_INC': 6,
    'EM_COM': 7,
    'ES_INC': 8,
    'ES_COM': 9,
    'PG_COM': 10,
};

document.addEventListener('DOMContentLoaded', function ()  {
    turmas = window.turmas;
    input_nascimento = document.getElementById('id_nascimento');
    input_cpf = document.getElementById('id_cpf');
    select_escolaridade = document.getElementById('id_escolaridade');
    input_cep = document.getElementById('id_cep');
    select_unidade = document.getElementById('id_unidade');
    select_curso = document.getElementById('id_curso');
    select_dias = document.getElementById('id_dias');
    select_horario = document.getElementById('id_horario');
    select_turma = document.getElementById('id_turma');

    adicionar_mascaras();
    adicionar_validacao([input_nascimento, input_cpf, select_escolaridade,
            input_cep, select_unidade, select_curso, select_dias]);

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

        let data = value.split('-');

        try {
            idade = moment().diff(moment(data, 'YYYY/MM/DD'), 'years');
        } finally {
            if (idade && escolaridade) {
                definir_unidades();
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

        if(escolaridade==='') {
            select_escolaridade.classList.add('is-invalid');
            invalid_message(select_escolaridade, 'Escolaridade  é um campo obrigatório.');
            return;
        }

        if (idade && escolaridade) {
            definir_unidades();
        }
    });

    input_cep.addEventListener('blur', () => {
        let cep = input_cep.value.replace(/\D/g, '');

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
            }
            else {
                input_cep.classList.add('is-invalid');
                invalid_message(input_cep, 'CEP inválido, verifique se foi escrita da maneira correta.');

                $("#id_rua").val('');
                $("#id_bairro").val('');
                $("#id_cidade").val('');
                $("#id_uf").val('');
            }
            document.getElementById('id_rua').disabled = false
            document.getElementById('id_bairro').disabled = false
            document.getElementById('id_cidade').disabled = false
            document.getElementById('id_uf').disabled = false

            document.getElementById('spinner_cep').hidden = true;
        });
    });

    select_unidade.addEventListener('change', () => {
        let unidade = select_unidade.value;
        let cursos = [];

        if (unidade==='') {
            select_unidade.classList.add('is-invalid');
            invalid_message(select_curso, 'Unidade é um campo obrigatório.')
            return;
        }

        for (let i=0; i<turmas.length; i++) {
            let turma = turmas[i];
            if (idade >= turma['curso_idade'] && hierarchy[escolaridade] >= hierarchy[turma['curso_escolaridade']]) {
                if (unidade === turma['unidade_nome']) {
                    let curso = turma['curso_nome'];

                    if (!cursos.includes(curso)) {
                        cursos.push(curso)
                    }
                }
            }
        }
        add_options(select_curso, cursos);
    });

    select_curso.addEventListener('change', () => {
        let unidade = select_unidade.value;
        let curso = select_curso.value;
        let dias = [];

        if(curso==='') {
            select_curso.classList.add('is-invalid');
            invalid_message(select_curso, 'Curso  é um campo obrigatório.');
            return;
        }

        for (let i = 0; i < turmas.length; i++) {
            let turma = turmas[i];
            if (idade >= turma['curso_idade'] && hierarchy[escolaridade] >= hierarchy[turma['curso_escolaridade']]) {
                if (unidade === turma['unidade_nome']) {
                    if (curso === turma['curso_nome']) {
                        let dia = turma['turma_dias'];

                        if (!dias.includes(dia)) {
                            dias.push(dia)
                        }
                    }
                }
            }
        }
        add_options(select_dias, dias);
    });

    select_dias.addEventListener('change', () => {
        let unidade = select_unidade.value;
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
            if (idade >= turma['curso_idade'] && hierarchy[escolaridade] >= hierarchy[turma['curso_escolaridade']]) {
                if (unidade === turma['unidade_nome']) {
                    if (curso === turma['curso_nome']) {
                        if (dias === turma['turma_dias']) {
                            let horario = turma['turma_horario'];

                        if (!horarios.includes(horario)) {
                            horarios.push(horario)
                        }
                        }
                    }
                }
            }
        }
        add_options(select_horario, horarios);
    });

    select_horario.addEventListener('change', () => {
        let unidade = select_unidade.value;
        let curso = select_curso.value;
        let dias = select_dias.value;
        let horario = select_horario.value;
        let turma_id = 0;

        for (let i = 0; i < turmas.length; i++) {
            let turma = turmas[i];

            if (idade >= turma['curso_idade'] && hierarchy[escolaridade] >= hierarchy[turma['curso_escolaridade']]) {
                if (unidade === turma['unidade_nome']) {
                    if (curso === turma['curso_nome']) {
                        if (dias === turma['turma_dias']) {
                            if (horario === turma['turma_horario']) {
                                turma_id = turma['turma_id'];
                            }
                        }
                    }
                }
            }
        }

        select_turma.selectedIndex = turma_id;
    });

    if(document.getElementById('id_turma').value !== '') {
        renderizar_turma();
    }
});

function definir_unidades(){
    let unidades = [];

    for (let i = 0; i < turmas.length; i++) {
        let turma = turmas[i];

        if (idade >= turma['curso_idade'] && hierarchy[escolaridade] >= hierarchy[turma['curso_escolaridade']]) {
            let unidade = turma['unidade_nome'];

            if(!unidades.includes(unidade)){
                unidades.push(unidade);
            }
        }
    }
    add_options(select_unidade, unidades);
    document.getElementById('curso_container').classList.remove('d-none');
}

function add_options(select, options){
   select.innerHTML = '<option value selected>---------</option>';

    for(let i = 0; i < options.length; i++) {
        let option = options[i];
        let new_opt = document.createElement('option');
        new_opt.text = option;
        new_opt.value = option;
        select.appendChild(new_opt);
    }

    select.parentElement.classList.remove('d-none');
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

function renderizar_turma() {
    let turma;

    for (let i = 0; i < turmas.length; i++) {
        if (select_turma.value === turmas[i]['turma_id'].toString()){
            turma = turmas[i];
        }
    }

    let unidade = turma['unidade_nome'];
    let curso = turma['curso_nome'];
    let dias = turma['turma_dias'];
    let horario = turma['turma_horario'];

    input_nascimento.dispatchEvent(new Event('blur'));
    select_escolaridade.dispatchEvent(new Event('blur'));

    select_unidade.value = unidade;

    select_unidade.dispatchEvent(new Event('change'));

    select_curso.value = curso

    select_curso.dispatchEvent(new Event('change'))

    select_dias.value = dias

    select_dias.dispatchEvent(new Event('change'))

    select_horario.value = horario

    select_horario.dispatchEvent(new Event('change'))
}