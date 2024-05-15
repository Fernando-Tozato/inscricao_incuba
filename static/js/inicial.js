function mascara(){
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

function enviar() {
    var formulario = document.getElementById("meuFormulario");
    var formData = new FormData(formulario);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", formulario.action);
    xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                // Processar resposta de sucesso aqui
                console.log("Formulário enviado com sucesso!");
            } else {
                // Processar resposta de erro aqui
                console.error("Erro ao enviar formulário!");
            }
        }
    };
    xhr.send(formData);
}

function exibir(){

}

function principal(){
    mascara();
    enviar();
    exibir();
}