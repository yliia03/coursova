document.addEventListener('DOMContentLoaded', () => {
    const burger = document.getElementById('navBurger');
    const menu = document.getElementById('navList');

    burger.addEventListener('click', () => {
        menu.classList.toggle('open');
        burger.classList.toggle('active');

        const isOpen = menu.classList.contains('open');
        burger.setAttribute('aria-expanded', isOpen);
        burger.setAttribute('aria-label', isOpen ? 'Закрити меню' : 'Відкрити меню');
    });

    const links = menu.querySelectorAll('.nav-link');
    links.forEach(link => {
        link.addEventListener('click', () => {
            menu.classList.remove('open');
            burger.classList.remove('active');
            burger.setAttribute('aria-expanded', 'false');
        });
    });
});