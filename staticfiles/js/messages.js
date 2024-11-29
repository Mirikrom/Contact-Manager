document.addEventListener('DOMContentLoaded', function() {
    // Xabarlarni avtomatik yopish
    const messages = document.querySelectorAll('#messages > div > div');
    messages.forEach(message => {
        setTimeout(() => {
            message.classList.replace('opacity-100', 'opacity-0');
            message.classList.replace('translate-y-0', '-translate-y-4');
            setTimeout(() => message.remove(), 500);
        }, 5000);
    });

    // Yopish tugmasini ishlatish
    document.querySelectorAll('.message-close').forEach(button => {
        button.addEventListener('click', () => {
            const message = button.closest('[role="alert"]');
            message.classList.replace('opacity-100', 'opacity-0');
            message.classList.replace('translate-y-0', '-translate-y-4');
            setTimeout(() => message.remove(), 500);
        });
    });
});
