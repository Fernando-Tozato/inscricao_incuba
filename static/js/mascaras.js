function adicionar_mascaras() {
    Inputmask("999.999.999-99").mask(document.getElementById('id_cpf'));

    // Máscara para o campo RG
    Inputmask("99.999.999-9").mask(document.getElementById('id_rg'));

    // Máscara para o campo data de nascimento
    Inputmask("99/99/9999").mask(document.getElementById('id_nascimento'));

    // Máscara para o campo data de emissão
    Inputmask("99/99/9999").mask(document.getElementById('id_data_emissao'));

    // Máscara para o campo telefone
    Inputmask("(99) 9999-9999").mask(document.getElementById('id_telefone'));

    // Máscara para o campo celular
    Inputmask("(99) 9 9999-9999").mask(document.getElementById('id_celular'));

    // Máscara para o campo CEP
    Inputmask("99.999-999").mask(document.getElementById('id_cep'));
}
