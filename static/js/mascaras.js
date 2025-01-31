function adicionar_mascaras() {
    Inputmask("999.999.999-99").mask(document.getElementById('id_cpf'));

    Inputmask("99.999.999-9").mask(document.getElementById('id_rg'));

    Inputmask("(99) 9999-9999").mask(document.getElementById('id_telefone'));

    Inputmask("(99) 9 9999-9999").mask(document.getElementById('id_celular'));

    Inputmask("99.999-999").mask(document.getElementById('id_cep'));
}
