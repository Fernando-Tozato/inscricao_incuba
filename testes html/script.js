function mascara_cpf(i){
    const v = i.value;
    
    if(isNaN(v[v.length-1])){
        i.value = v.substring(0, v.length-1);
        return;
    }
    
    i.setAttribute("maxlength", "14");
    if (v.length == 3 || v.length == 7){
        i.value += ".";
    }
    
    if (v.length == 11){
        i.value += "-";
    }
}

function mascara_rg(i){
    const v = i.value;

    if(isNaN(v[v.length-1])){
        i.value = v.substring(0, v.length-1);
        return;
    }

    i.setAttribute("maxlength", "12");
    if (v.length == 2 || v.length == 6){
        i.value += ".";
    }

    if(v.length == 10){
        i.value += "-";
    }
}

function mascara_tel(i){
    const v = i.value;

    if(isNaN(v[v.length-1])){
        i.value = v.substring(0, v.length-1);
        return;
    }

    i.setAttribute("maxlength", "14");
    if (v.length == 2){
        i.value = '(' + i.value + ') '
    }

    if(v.length == 9){
        i.value += "-";
    }
}

function mascara_cel(i){
    const v = i.value;

    if(isNaN(v[v.length-1])){
        i.value = v.substring(0, v.length-1);
        return;
    }

    i.setAttribute("maxlength", "16");
    if (v.length == 2){
        i.value = '(' + i.value + ') '
    }

    if(v.length == 6){
        i.value+=' ';
    }

    if(v.length == 11){
        i.value += "-";
    }
}

function mascara_data(i){
    const v = i.value;

    if(isNaN(v[v.length-1])){
        i.value = v.substring(0, v.length-1);
        return;
    }

    i.setAttribute("maxlength", "10");
    if (v.length == 2 || v.length == 5){
        i.value += "/";
    }
}

function mascara_cep(i){
    const v = i.value;

    if(isNaN(v[v.length-1])){
        i.value = v.substring(0, v.length-1);
        return;
    }

    i.setAttribute("maxlength", "10");
    if (v.length == 2){
        i.value += ".";
    }

    if(v.length == 6){
        i.value += "-";
    }
}

function callback(conteudo){
    const placeholder = document.getElementById('cep_placeholder');
    if (!("erro" in conteudo)) {
        document.getElementById('rua').value=(conteudo.logradouro);
        document.getElementById('bairro').value=(conteudo.bairro);
        document.getElementById('cidade').value=(conteudo.localidade);
        document.getElementById('uf').value=(conteudo.uf);

        document.getElementById('rua').disabled=true;
        document.getElementById('bairro').disabled=true;
        document.getElementById('cidade').disabled=true;
        document.getElementById('uf').disabled=true;

        placeholder.innerHTML = '';
    } else if(placeholder.innerHTML.length == 0){
        placeholder.innerHTML = [
            '<div class="alert alert-warning d-flex align-items-center mt-3" role="alert">',
                '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-2" role="img" aria-label="Danger:" style="color: #cfac2a;"></i>',
                '<div>CEP inválido. Verifique se foi digitado corretamente.</</div>',
            '</div>'
        ].join('');
    }
}

function achar_cep(i){
    const cep = i.replace(/\D/g, '');
    const placeholder = document.getElementById('cep_placeholder');

    if(cep != ""){
        const validacep = /^[0-9]{8}$/;

        if(validacep.test(cep)){
            const script = document.createElement('script');

            script.src = 'https://viacep.com.br/ws/'+ cep + '/json/?callback=callback';
            
            document.body.appendChild(script);
        } else if(placeholder.innerHTML.length == 0){
            placeholder.innerHTML = [
                '<div class="alert alert-warning d-flex align-items-center mt-3" role="alert">',
                    '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-2" role="img" aria-label="Danger:" style="color: #cfac2a;"></i>',
                    '<div>CEP inválido. Verifique se foi digitado corretamente.</div>',
                '</div>'
            ].join('');
        }
    }
}

function enviar(){
    var preenchido = false;
    var inputs = document.getElementsByClassName('required');
    const placeholder = document.getElementById('alert_placeholder');

    for(var i = 0; i < inputs.length; i++) {
        preenchido = false;
        console.log(i)
        if(inputs[i].value.length > 0){
            preenchido = true;
        }

        

        if(preenchido == false && placeholder.innerHTML.length == 0){
            document.getElementById('danger_badge').innerHTML = ''
            placeholder.innerHTML = [
                '<div class="alert alert-danger d-flex align-items-center mt-3" role="alert">',
                    '<i class="fa-solid fa-triangle-exclamation bi flex-shrink-0 me-3" role="img" aria-label="Danger:" style="color: #b20101;"></i>',
                    '<div>Preencha todos os campos marcados como obrigatórios (*) antes de enviar o formulário!</div>',
                '</div>'
            ].join('');
            break;
        }
    }
}