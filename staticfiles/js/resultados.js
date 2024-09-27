let turmas;
let select_curso;
let select_dias;
let select_horario;

document.addEventListener('DOMContentLoaded', function () {
    turmas = window.turmas;
    select_curso = document.getElementById('id_curso');
    select_dias = document.getElementById('id_dias');
    select_horario = document.getElementById('id_horario');

    definir_cursos();

    select_curso.addEventListener('change', () => {
        let curso = select_curso.value;
        let dias = [];

        if(curso==='') {
            select_curso.classList.add('is-invalid');
            invalid_message(select_curso, 'Curso  é um campo obrigatório.');
            return;
        }

        for (let i = 0; i < turmas.length; i++) {
            let turma = turmas[i];
            if (curso === turma['curso']) {
                let dia = turma['dias'];

                if(!dias.includes(dia)){
                    dias.push(dia);
                }
            }
        }
        add_options(select_dias, dias);
    });

    select_dias.addEventListener('change', () => {
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
            if (curso === turma['curso']) {
                if (dias === turma['dias']) {
                    let horario = turma['horario'];

                    if(!horarios.includes(horario)){
                        horarios.push(horario);
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
        let curso = turma['curso'];

        if(!cursos.includes(curso)){
            cursos.push(curso);
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
}