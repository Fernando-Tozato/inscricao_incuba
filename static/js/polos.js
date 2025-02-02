// Ativa as animações quando a página carrega
document.addEventListener('DOMContentLoaded', function() {
    const animatedElements = document.querySelectorAll('.animate-card');

    animatedElements.forEach((element, index) => {
        setTimeout(() => {
            element.style.opacity = 1;
        }, index * 150);
    });
});