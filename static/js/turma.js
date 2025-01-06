let cursos;
let unidades;
let select_curso;
let select_unidade;
let selected_curso;

document.addEventListener('DOMContentLoaded', function () {
    cursos = window.cursos;
    unidades = window.unidades;
    select_curso = document.getElementById('id_curso');
    select_unidade = document.getElementById('id_unidade');

    console.log(typeof cursos)

    adicionar_validacao([select_curso, select_unidade]);

    select_curso.addEventListener('blur', () => {
        selected_curso = parseInt(select_curso.value);

        if(selected_curso==='') {
            select_curso.classList.add('is-invalid');
            invalid_message(select_curso, 'Curso  é um campo obrigatório.');
            return;
        }

        definir_unidades();
    });
});

function definir_unidades() {
    let unidades_validas = [];

    for (let i = 0; i < cursos.length; i++) {
        let curso = cursos[i];

        if (curso.id === selected_curso) {
            if (!unidades_validas.includes(curso.unidades__id)) {
                unidades_validas.push(curso.unidades__id);
            }
        }
    }

    add_options(select_unidade, unidades_validas);
}

function add_options(select, options){
    select.innerHTML = '<option value selected>Selecione...</option>';

    for(let i = 0; i < options.length; i++) {
        let option = options[i];
        let new_opt = document.createElement('option');
        new_opt.text = unidades[option-1].nome;
        new_opt.value = option;
        select.appendChild(new_opt);
    }

    if (options.length === 1) {
        select.childNodes[-1].selected = true;
    }

    select.disabled = false;
}