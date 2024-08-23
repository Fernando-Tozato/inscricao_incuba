let turmas;
let input_nascimento;
let select_escolaridade;
let select_curso;
let select_dias;
let select_horario;
let idade;
let escolaridade;

document.addEventListener('DOMContentLoaded', () => {
    turmas = window.turmas;
    input_nascimento = document.getElementById('id_nascimento');
    select_escolaridade = document.getElementById('id_escolaridade');
    select_curso = document.getElementById('id_curso');
    select_dias = document.getElementById('id_dias');
    select_horario = document.getElementById('id_horario');

    input_nascimento.addEventListener('change', () => {
        let data = input_nascimento.value.split('/');

        try {
            idade = moment().diff(moment(data, 'DD/MM/YYYY'), 'years');
        } finally {
            if (idade && escolaridade) {
                definir_cursos();
            }
        }
    });

    select_escolaridade.addEventListener('change', () => {
        escolaridade = select_escolaridade.value;
        if (idade && escolaridade) {
            definir_cursos();
        }
    });

    select_curso.addEventListener('change', () => {
        let curso = select_curso.value;
        let dias = [];

        for (let i=0; i < turmas.length; i++) {
            let turma = turmas[i];
            if (idade >= turma['idade'] && escolaridade >= turma['escolaridade']) {
                if (curso === turma['curso']) {
                    dias.push(turma['dias']);
                }

            }
        }
        add_options(select_dias, dias);
    });

    select_dias.addEventListener('change', () => {
        let curso = select_curso.value;
        let dias = select_dias.value;
        let horarios = [];

        for (let i=0; i < turmas.length; i++) {
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

    for (let i=0; i < turmas.length; i++) {
        let turma = turmas[i];
        if (idade >= turma['idade'] && escolaridade >= turma['escolaridade']) {
            cursos.push(turma['curso']);
        }
    }
    add_options(select_curso, cursos);
}

function add_options(select, options){
    for(let i=0; i<options.length; i++) {
        let option = options[i];
        let new_opt = document.createElement('option');
        new_opt.text = option;
        new_opt.value = option;
        select.appendChild(new_opt);
    }
    select.disabled = false;
}