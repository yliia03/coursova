/* SLIDER*/
document.addEventListener('DOMContentLoaded', () => {
    const track = document.querySelector('.testimonials-track');
    const items = document.querySelectorAll('.testimonials-item');
    const dotsContainer = document.getElementById('testimonialsDots');
    const btnPrev = document.getElementById('sliderPrev');
    const btnNext = document.getElementById('sliderNext');

    if (!track || !items.length || !dotsContainer || !btnPrev || !btnNext) return;

    let currentIndex = 0;

    function getItemsPerView() {
        if (window.innerWidth >= 992) return 2;
        return 1;
    }

    function createDots() {
        dotsContainer.innerHTML = '';
        const itemsPerView = getItemsPerView();
        const maxDots = items.length - itemsPerView + 1;

        for (let i = 0; i < maxDots; i++) {
            const dot = document.createElement('button');
            dot.classList.add('testimonials-dot');
            dot.setAttribute('type', 'button');
            dot.setAttribute('aria-label', `Перейти до слайду ${i + 1}`);
            if (i === 0) dot.classList.add('active');
            
            dot.addEventListener('click', () => {
                goToSlide(i);
            });
            dotsContainer.appendChild(dot);
        }
    }

    function updateNavButtons() {
        const itemsPerView = getItemsPerView();
        const maxIndex = items.length - itemsPerView;

        btnPrev.disabled = currentIndex === 0;
        
        btnNext.disabled = currentIndex >= maxIndex;
    }

    function goToSlide(index) {
        const itemsPerView = getItemsPerView();
        const maxIndex = items.length - itemsPerView;
        
        currentIndex = Math.max(0, Math.min(index, maxIndex));

        const itemWidth = items[0].getBoundingClientRect().width + 20; 
        track.style.transform = `translateX(-${currentIndex * itemWidth}px)`;

        const dots = dotsContainer.querySelectorAll('.testimonials-dot');
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === currentIndex);
        });

        updateNavButtons();
    }

    btnPrev.addEventListener('click', () => {
        goToSlide(currentIndex - 1);
    });

    btnNext.addEventListener('click', () => {
        goToSlide(currentIndex + 1);
    });

    createDots();
    updateNavButtons();
    
    window.addEventListener('resize', () => {
        createDots();
        goToSlide(0);
    });
});

// ADVISORS SLIDER
(function () {
    const track = document.querySelector('.advisors-track');
    const items = document.querySelectorAll('.advisors-card');
    const dotsContainer = document.getElementById('advisorsDots');
    const btnPrev = document.getElementById('advisorsPrev');
    const btnNext = document.getElementById('advisorsNext');

    if (!track || !items.length) return; // захист якщо секції немає на сторінці

    let currentIndex = 0;

    function getItemsPerView() {
        if (window.innerWidth >= 1025) return 3;
        if (window.innerWidth >= 640) return 2;
        return 1;
    }

    function createDots() {
        dotsContainer.innerHTML = '';
        const maxDots = items.length - getItemsPerView() + 1;
        for (let i = 0; i < maxDots; i++) {
            const dot = document.createElement('button');
            dot.classList.add('testimonials-dot');
            dot.setAttribute('type', 'button');
            if (i === 0) dot.classList.add('active');
            dot.addEventListener('click', () => goToSlide(i));
            dotsContainer.appendChild(dot);
        }
    }

    function goToSlide(index) {
        const maxIndex = items.length - getItemsPerView();
        currentIndex = Math.max(0, Math.min(index, maxIndex));
        const itemWidth = items[0].getBoundingClientRect().width + 24;
        track.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
        document.querySelectorAll('#advisorsDots .testimonials-dot')
            .forEach((d, i) => d.classList.toggle('active', i === currentIndex));
        btnPrev.disabled = currentIndex === 0;
        btnNext.disabled = currentIndex >= maxIndex;
    }

    btnPrev.addEventListener('click', () => goToSlide(currentIndex - 1));
    btnNext.addEventListener('click', () => goToSlide(currentIndex + 1));

    createDots();
    goToSlide(0);

    window.addEventListener('resize', () => { createDots(); goToSlide(0); });
})();

/* FOOTER SUBSCRIBE*/
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('subscribeForm');
    const messageContainer = document.getElementById('subscribeMessage');
    const emailInput = document.getElementById('subscribeEmail');

    if (!form || !messageContainer || !emailInput) return;

    form.addEventListener('submit', (event) => {
        event.preventDefault(); 

        messageContainer.textContent = 'Ви підписалися!';
        messageContainer.classList.add('success');

        form.reset();

        setTimeout(() => {
            messageContainer.textContent = '';
            messageContainer.classList.remove('success');
        }, 5000);
    });
});

/* CTA BANNER*/
document.addEventListener('DOMContentLoaded', () => {
    const phoneInput = document.getElementById('feedbackPhone');
    const feedbackForm = document.getElementById('feedbackForm');

    if (!phoneInput || !feedbackForm) return;

    phoneInput.addEventListener('input', (e) => {
        e.target.value = e.target.value.replace(/\D/g, '');
    });
    feedbackForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        alert('Дякуємо! Ваш відгук успішно надіслано.');
        feedbackForm.reset();
    });
});