let url_dias = '/inscricao/busca_dias/';
let url_horarios = '/inscricao/busca_horarios/';
let csrftoken;
let id_turma;

function habilitar_dias(selected){
    const select_dias = document.getElementById('dias');
    const select_horario = document.getElementById('horario');
    curso = selected.value;

    select_dias.innerHTML = '<option selected disabled hidden></option>'
    select_horario.innerHTML = '<option selected disabled hidden></option>'
    select_dias.disabled = true;
    select_horario.disabled = true;

    const dados = {'curso': curso}

    fetch(url_dias, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(dados)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao carregar o arquivo JSON');
        }
        return response.json();
    })
    .then(data => {
        const dias = data.dias;
        dias.forEach(dia => {
            let new_opt = document.createElement("option");
            new_opt.text = dia;
            new_opt.value = dia;
            select_dias.appendChild(new_opt);
        });
        select_dias.disabled = false;
    })
    .catch(error => {
        console.error('Erro:', error);
    });
}

function habilitar_horarios(selected){
    const select_horario = document.getElementById('horario');
    let horarios = [];
    dias = selected.value;

    select_horario.innerHTML = '<option selected disabled hidden></option>'
    select_horario.disabled = true;

    const dados = {
        'curso': curso,
        'dias': dias
    }

    fetch(url_horarios, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(dados)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao carregar o arquivo JSON');
        }
        return response.json();
    })
    .then(data => {
        const horarios = data.horarios;
        const ids = data.ids;

        for(let i = 0; i<ids.length; i++) {
            let new_opt = document.createElement("option");
            new_opt.text = horarios[i];
            new_opt.value = horarios[i];
            new_opt.id = ids[i];
            select_horario.appendChild(new_opt);
        }
        select_horario.disabled = false;
    })
    .catch(error => {
        console.error('Erro:', error);
    });

    horarios.forEach(horario => {
        let new_opt = document.createElement("option");
        new_opt.text = horario;
        new_opt.value = horario;
        select_horario.appendChild(new_opt);
    });
    select_horario.disabled = false;
}

function set_horario(selected){
    id_turma = selected.options[selected.selectedIndex].id;
}

function buscar(){
    if (id_turma) {
        if (window.location.pathname == '/resultado/'){
            window.location.href += `${id_turma}/`
        } else {
            window.location.pathname = `/resultado/${id_turma}/`
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    csrftoken = document.getElementById('token').children[0].value;
});