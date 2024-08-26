function renderizar_turma() {
    let id_turma = document.getElementById('id_turma').value - 1;
    let turma = window.turmas[id_turma];

    let select_curso = document.getElementById('id_curso')
    let select_dias = document.getElementById('id_dias')
    let select_horario = document.getElementById('id_horario')

    let curso = turma.curso
    let dias = turma.dias
    let horario = turma.horario

    select_curso.value = curso
    console.log(select_curso.value)

    select_curso.dispatchEvent(new Event('change'))
    console.log(select_dias.children)

    select_dias.value = dias
    console.log(select_dias.value)

    select_dias.dispatchEvent(new Event('change'))
    console.log(select_horario.children)

    select_horario.value = horario
    console.log(select_horario.value)
}