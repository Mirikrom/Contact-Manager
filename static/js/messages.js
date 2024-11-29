function showMessage(message, type = 'success') {
    // Eski xabarlarni o'chirish
    const existingMessages = document.querySelectorAll('.message-alert');
    existingMessages.forEach(msg => msg.remove());

    // Yangi xabar elementini yaratish
    const messageDiv = document.createElement('div');
    messageDiv.className = `message-alert fixed top-4 left-1/2 transform -translate-x-1/2 z-50 p-4 rounded-lg shadow-lg transition-all duration-300 ease-in-out opacity-0 translate-y-[-100%]`;
    
    // Xabar turi bo'yicha stil berish
    switch(type) {
        case 'success':
            messageDiv.classList.add('bg-green-100', 'text-green-800', 'border', 'border-green-200');
            break;
        case 'error':
            messageDiv.classList.add('bg-red-100', 'text-red-800', 'border', 'border-red-200');
            break;
        case 'warning':
            messageDiv.classList.add('bg-yellow-100', 'text-yellow-800', 'border', 'border-yellow-200');
            break;
        case 'info':
            messageDiv.classList.add('bg-blue-100', 'text-blue-800', 'border', 'border-blue-200');
            break;
    }

    // Xabar matnini qo'shish
    messageDiv.innerHTML = `
        <div class="flex items-center">
            <div class="flex-shrink-0">
                ${type === 'success' ? `
                    <svg class="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                    </svg>
                ` : type === 'error' ? `
                    <svg class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
                    </svg>
                ` : type === 'warning' ? `
                    <svg class="h-5 w-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
                    </svg>
                ` : `
                    <svg class="h-5 w-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
                    </svg>
                `}
            </div>
            <div class="ml-3">
                <p class="text-sm font-medium">${message}</p>
            </div>
            <div class="ml-auto pl-3">
                <div class="-mx-1.5 -my-1.5">
                    <button onclick="this.parentElement.parentElement.parentElement.parentElement.remove()" class="inline-flex rounded-md p-1.5 focus:outline-none focus:ring-2 focus:ring-offset-2 ${
                        type === 'success' ? 'text-green-500 hover:bg-green-100 focus:ring-green-600' :
                        type === 'error' ? 'text-red-500 hover:bg-red-100 focus:ring-red-600' :
                        type === 'warning' ? 'text-yellow-500 hover:bg-yellow-100 focus:ring-yellow-600' :
                        'text-blue-500 hover:bg-blue-100 focus:ring-blue-600'
                    }">
                        <span class="sr-only">Yopish</span>
                        <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    `;

    // Xabarni sahifaga qo'shish
    document.body.appendChild(messageDiv);

    // Animatsiya bilan ko'rsatish
    setTimeout(() => {
        messageDiv.classList.remove('opacity-0', 'translate-y-[-100%]');
        messageDiv.classList.add('opacity-100', 'translate-y-0');
    }, 100);

    // 5 sekunddan keyin xabarni yashirish
    setTimeout(() => {
        messageDiv.classList.add('opacity-0', 'translate-y-[-100%]');
        setTimeout(() => {
            messageDiv.remove();
        }, 300);
    }, 5000);
}

// Sahifa yuklanganda mavjud xabarlarni ko'rsatish
document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.messages .message');
    messages.forEach(message => {
        const text = message.textContent.trim();
        const type = message.classList.contains('success') ? 'success' :
                    message.classList.contains('error') ? 'error' :
                    message.classList.contains('warning') ? 'warning' : 'info';
        
        showMessage(text, type);
        message.remove();
    });
});
