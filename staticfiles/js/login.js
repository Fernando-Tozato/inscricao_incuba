document.addEventListener('DOMContentLoaded', function() {
    inputs = document.getElementsByTagName('input')
    for (let i=1;i<inputs.length;i++){
        input = inputs[i];
        if (input.type != 'checkbox'){
            input.setAttribute('id', input.name);
            input.setAttribute('class', 'form-control');
        }
    }
});

function togglePassword(fieldId) {
    let field = document.getElementById(fieldId);
    if (field.type === 'password') {
        field.type = 'text';
    } else {
        field.type = 'password';
    }
}