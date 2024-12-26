function adicionar_mascaras(is_turmas = false) {
    if(is_turmas === false) {
        Inputmask("999.999.999-99").mask(document.getElementById('id_cpf'));

        Inputmask("99.999.999-9").mask(document.getElementById('id_rg'));

        Inputmask("99/99/9999").mask(document.getElementById('id_nascimento'));

        Inputmask("99/99/9999").mask(document.getElementById('id_data_emissao'));

        Inputmask("(99) 9999-9999").mask(document.getElementById('id_telefone'));

        Inputmask("(99) 9 9999-9999").mask(document.getElementById('id_celular'));

        Inputmask("99.999-999").mask(document.getElementById('id_cep'));
    }
    else{
        /*horario_entrada = document.getElementById('id_horario_entrada').value;

        Inputmask("hh:mm", {placeholder: "HH:MM", insertMode: false, showMaskOnHover:false})
            .mask(document.getElementById('id_horario_saida'));*/
    }
}
