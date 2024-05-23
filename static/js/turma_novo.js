let form_vazio = true;
let url_envio = '/interno/turma/criar/'

function verifica_form(){
    let vazio = true;
    const inputs = document.getElementsByClassName('required');
    const placeholder = document.getElementById('preenchido_placeholder');

    for (var i = 0; i < inputs.length - 1; i++) {
        if (inputs[i].value !== '') {
            vazio = false;
        } else {
            vazio = true;
        }
    }

    if(!vazio && document.getElementById('termos').checked != true){
        vazio = true;
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
    const placeholder = document.getElementById('erro_placeholder');

    if(!form_vazio){
        const dados = {
            "curso": document.getElementById('curso').value,
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
                window.location.pathname = url_enviado
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
                '<div>Atenção! Seu formulário de inscrição não foi enviado. Corrija os erros antes do envio.</div>',
            '</div>'
        ].join('');

        document.getElementById('navbar').scrollIntoView({behavior: 'instant', block: 'start'})
    }
}

function mascara_hora(i){
    const v = i.value;

    if(isNaN(v[v.length-1])){
        i.value = v.substring(0, v.length-1);
        return;
    }

    i.setAttribute("maxlength", "5");
    if (v.length == 2){
        i.value += ":";
    }

    if(v.contains(':')){
        h = v.split(':')[0];
        m = v.split(':')[1];

        if(h<0){
            i.value = '00:00';
        } else if(h==24){
            i.value = '00:00';
        }
    }
}