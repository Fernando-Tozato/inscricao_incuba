function adicionar_validacao(no_blur_fields) {
    no_blur_fields = new Set(no_blur_fields);

    let required_fields = document.querySelectorAll('.required');

    for(let i = 0; i < required_fields.length; i++) {
        let field = required_fields[i];

        field.addEventListener('focus', () => {
            field.classList.remove('is-invalid');
        });

        if(!no_blur_fields.has(field)) {
            field.addEventListener('blur', () => {
                if (field.value === '') {
                    field.classList.add('is-invalid');
                    let name = field.name;
                    invalid_message(field, `${name.charAt(0).toUpperCase() + name.slice(1)} é um campo obrigatório.`);
                }
            });
        }
    }
}

function invalid_message(field_element, message) {
    let message_div = document.getElementById(field_element.id + '_feedback');
    message_div.innerText = message;
}