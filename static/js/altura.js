function muda_footer() {
    const viewportHeight = window.innerHeight;
    const pageHeight = document.documentElement.scrollHeight;
    const footer = document.getElementById('footer');

    if (pageHeight > viewportHeight) {
        footer.classList.remove('fixed-bottom');
    } else {
        footer.classList.add('fixed-bottom');
    }
}

window.onload = muda_footer;
window.onresize = muda_footer;