// O'chirish tasdiqlash funksiyasi
function confirmDelete(type) {
    const messages = {
        'contact': 'Haqiqatan ham bu kontaktni o\'chirmoqchimisiz?',
        'group': 'Are you sure you want to delete this group?',
        'group_contact': 'Haqiqatan ham bu kontaktni guruhdan o\'chirmoqchimisiz?'
    };
    return confirm(messages[type]);
}
