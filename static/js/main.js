document.addEventListener('DOMContentLoaded', function() {
    const toggleMenuButton = document.getElementById('toggle-menu');
    const mobileMenu = document.getElementById('mobile-menu');

    if (toggleMenuButton && mobileMenu) {
        toggleMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }

    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });
});
