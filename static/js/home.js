document.addEventListener('DOMContentLoaded', function() {
  const cards = document.querySelectorAll('.card');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const card = entry.target;
        const imgPosition = card.querySelector('.col-xl-4') ? 'left' : 'right';

        if(imgPosition === 'left') {
          card.querySelector('.col-xl-4').classList.add('slide-in-left');
          card.querySelector('.col-xl-8').classList.add('slide-in-right', 'delay-animation');
        } else {
          card.querySelector('.col-xl-4').classList.add('slide-in-right');
          card.querySelector('.col-xl-8').classList.add('slide-in-left', 'delay-animation');
        }

        observer.unobserve(card);
      }
    });
  }, {
    threshold: 0.1
  });

  cards.forEach(card => {
    card.classList.add('card-container');
    if(card.querySelector('.col-xl-4')) {
      card.classList.add('card-animation-left');
    } else {
      card.classList.add('card-animation-right');
    }
    observer.observe(card);
  });
});