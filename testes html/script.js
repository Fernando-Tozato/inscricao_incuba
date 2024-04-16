function mascara_cpf(i){
    const v = i.value;
    
    if(isNaN(v[v.length-1])){ // impede entrar outro caractere que não seja número
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

function mascara_cep(i) {
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
    if (!("erro" in conteudo)) {
        document.getElementById('rua').value=(conteudo.logradouro);
        document.getElementById('bairro').value=(conteudo.bairro);
        document.getElementById('cidade').value=(conteudo.localidade);
        document.getElementById('uf').value=(conteudo.uf);

        document.getElementById('rua').disabled=true;
        document.getElementById('bairro').disabled=true;
        document.getElementById('cidade').disabled=true;
        document.getElementById('uf').disabled=true;
    } else {
        alert("CEP não encontrado.");
    }
}

function achar_cep(i){
    const cep = i.replace(/\D/g, '');

    if (cep != ""){
        const validacep = /^[0-9]{8}$/;

        if(validacep.test(cep)){
            const script = document.createElement('script');

            script.src = 'https://viacep.com.br/ws/'+ cep + '/json/?callback=callback';
            
            document.body.appendChild(script);
        } else {
            alert("Formato de CEP inválido.")
        }
    }
}