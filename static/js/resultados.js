let turmas;
let select_turma;
let select_unidade;
let select_curso;
let select_dias;
let select_horario;

document.addEventListener('DOMContentLoaded', function () {
    turmas = window.turmas;
    select_turma = document.getElementById('id_turma');
    select_unidade = document.getElementById('id_unidade');
    select_curso = document.getElementById('id_curso');
    select_dias = document.getElementById('id_dias');
    select_horario = document.getElementById('id_horario');

    definir_unidades();

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

            if (unidade === turma['unidade_nome']) {
                let curso = turma['curso_nome'];

                if (!cursos.includes(curso)) {
                    cursos.push(curso)
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

            if (unidade === turma['unidade_nome']) {
                if (curso === turma['curso_nome']) {
                    let dia = turma['turma_dias'];

                    if (!dias.includes(dia)) {
                        dias.push(dia)
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
        let unidade = turma['unidade_nome'];

        if(!unidades.includes(unidade)){
            unidades.push(unidade);
        }
    }
    add_options(select_unidade, unidades);
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

    select_unidade.value = unidade;

    select_unidade.dispatchEvent(new Event('change'));

    select_curso.value = curso

    select_curso.dispatchEvent(new Event('change'))

    select_dias.value = dias

    select_dias.dispatchEvent(new Event('change'))

    select_horario.value = horario

    select_horario.dispatchEvent(new Event('change'))
}