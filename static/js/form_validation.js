document.addEventListener('DOMContentLoaded', () => {
    const required_fields = document.getElementsByClassName('required');

    Array.from(required_fields).forEach(field => {
        field.addEventListener('focus', () => {
            field.classList.remove('is-invalid');
        });

        field.addEventListener('blur', () => {
            if(field.valueMissing) {
                field.classList.add('is-invalid');
            }
        });
    });
});