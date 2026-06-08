document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('modal');
    const openBtn = document.getElementById('openModalBtn');
    const closeBtn = document.getElementById('modalClose');
    const overlay = document.getElementById('modalOverlay');
    const modalForm = document.getElementById('modalForm');
    const modalPhone = document.getElementById('modalPhone');

    openBtn.addEventListener('click', () => {
        modal.classList.add('open');
        document.body.style.overflow = 'hidden';
    });

    function closeModal() {
        modal.classList.remove('open');
        document.body.style.overflow = '';
    }

    closeBtn.addEventListener('click', closeModal);
    overlay.addEventListener('click', closeModal);

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('open')) {
            closeModal();
        }
    });

    modalPhone.addEventListener('input', (e) => {
        e.target.value = e.target.value.replace(/\D/g, '');
    });

    modalForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        alert('Дякуємо! Заявку успішно відправлено. Ми зв’яжемося з вами!');
        
        modalForm.reset();
        closeModal();
    });
});