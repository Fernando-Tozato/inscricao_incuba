document.addEventListener('DOMContentLoaded', function() {
    inputs = document.getElementsByTagName('input')
    for (let i=1;i<inputs.length;i++){
        input = inputs[i];
        input.setAttribute('id', input.name);
        input.setAttribute('class', 'form-control');
    }
});