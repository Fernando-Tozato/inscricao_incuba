let form_vazio = true;
let url_envio = '/interno/turma/criar/'
let csrftoken;

function verifica_form(){
    let vazio = true;
    const inputs = document.getElementsByClassName('required');
    const placeholder = document.getElementById('preenchido_placeholder');

    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].value !== '') {
            vazio = false;
        } else {
            vazio = true;
        }   
    }
        
    if(vazio && placeholder.innerHTML.length == 0){
        placeholder.innerHTML = [
            '<div class="alert alert-danger d-flex align-items-center mt-3" role="alert">',
                '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-3" role="img" aria-label="Danger:" style="color: #b20101;"></i>',
                '<div>Preencha todos os campos antes de enviar o formulário!</div>',
            '</div>'
        ].join('');
        form_vazio = true;
    } 
    else {
        placeholder.innerHTML = '';
        form_vazio = false;
    }
}

function enviar_dados(){
    const placeholder = document.getElementById('cima_placeholder');

    if(!form_vazio){
        const dados = {
            "curso": document.getElementById('curso').value,
            "professor": document.getElementById('professor').value,
            "dias": document.getElementById('dias').value,
            "entrada": document.getElementById('entrada').value,
            "saida": document.getElementById('saida').value,
            "vagas": parseInt(document.getElementById('vagas').value),
            "idade": parseInt(document.getElementById('idade').value),
            "escolaridade": parseInt(document.getElementById('escolaridade').value )
        };
        
        fetch(url_envio, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(dados)
        })
        .then(response => {
            if (!response.ok) {
                if(placeholder.innerHTML == ''){
                    placeholder.innerHTML = [
                        '<div class="alert alert-danger d-flex align-items-center mt-3" role="alert">',
                            '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-3" role="img" aria-label="Danger:" style="color: #b20101;"></i>',
                            '<div>Atenção! A turma não foi criada. Verifique se está com internet e tente novamente. Caso o problema persista, contate a equipe de TI.</div>',
                        '</div>'
                    ].join('');

                    document.getElementById('navbar').scrollIntoView({behavior: 'instant', block: 'start'})
                }
            } else {
                sucesso();
            }
        })
        .catch(error => {
            console.error('Erro:', error);
        });
    }
    else {
        placeholder.innerHTML = [
            '<div class="alert alert-danger d-flex align-items-center mt-3" role="alert">',
                '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-3" role="img" aria-label="Danger:" style="color: #b20101;"></i>',
                '<div>Atenção! A turma não foi criada. Corrija os erros antes do envio.</div>',
            '</div>'
        ].join('');

        document.getElementById('navbar').scrollIntoView({behavior: 'instant', block: 'start'})
    }
}

function mascara_hora(input){
    const hora = input.value;

    if(isNaN(hora[hora.length-1])){
        input.value = hora.substring(0, hora.length-1);
        return;
    }

    input.setAttribute("maxlength", "5");
    if (hora.length == 2){
        input.value += ":";
    }
}

function verifica_horas(input){
    const hora = input.value;

    if(hora.includes(':')){
        h = hora.split(':')[0];
        m = hora.split(':')[1];

        if(h>=24){
            h = '00';
        }
        if(m>=60){
            h = String(Number(h) + 1);
            m = String(Number(m) - 60);
        }
        input.value = `${h}:${m}`
    }
}

function sucesso(){
    const placeholder = document.getElementById('cima_placeholder');

    placeholder.innerHTML = [
        '<div class="alert alert-success d-flex align-items-center mt-3" role="alert">',
            '<i class="fa-solid fa-circle-check bi flex-shrink-0 me-3" role="img" aria-label="Success:" style="color: #248449;"></i>',
            '<div>Sucesso! A turma já está no banco de dados.</div>',
        '</div>'
    ].join('');
}

document.addEventListener('DOMContentLoaded', function() {
    csrftoken = document.getElementById('token').children[0].value;
});