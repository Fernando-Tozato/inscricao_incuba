function compareHeights() {
    const viewportHeight = window.innerHeight;
    const pageHeight = document.documentElement.scrollHeight;
    const footer = document.getElementById('footer');

    if (pageHeight > viewportHeight) {
        footer.classList.add('fixed-bottom');
    } else {
        footer.classList.remove('fixed-bottom');
    }
}

window.onload = compareHeights;