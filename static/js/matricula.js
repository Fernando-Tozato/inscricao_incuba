function renderizar_turma() {
    let id_turma = document.getElementById('id_turma').value - 112;
    let turma = window.turmas[id_turma];

    let select_curso = document.getElementById('id_curso')
    let select_dias = document.getElementById('id_dias')
    let select_horario = document.getElementById('id_horario')

    let curso = turma.curso
    let dias = turma.dias
    let horario = turma.horario

    select_curso.value = curso

    select_curso.dispatchEvent(new Event('change'))

    select_dias.value = dias

    select_dias.dispatchEvent(new Event('change'))

    select_horario.value = horario
}