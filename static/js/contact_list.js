let deleteMode = false;
let selectAllPagesChecked = false;
let selectedIds = new Set();

function toggleDeleteMode() {
    console.log('toggleDeleteMode called');
    deleteMode = !deleteMode;
    const controls = document.getElementById('deleteModeControls');
    const checkboxes = document.querySelectorAll('.contact-checkbox');
    const deleteButton = document.getElementById('deleteMode');

    if (deleteMode) {
        controls.classList.remove('hidden');
        checkboxes.forEach(cb => cb.classList.remove('hidden'));
        deleteButton.classList.add('bg-gray-600');
        deleteButton.classList.remove('bg-red-600');
    } else {
        controls.classList.add('hidden');
        checkboxes.forEach(cb => {
            cb.classList.add('hidden');
            cb.checked = false;
        });
        deleteButton.classList.remove('bg-gray-600');
        deleteButton.classList.add('bg-red-600');
        document.getElementById('selectAll').checked = false;
        document.getElementById('selectAllPages').checked = false;
        selectedIds.clear();
        updateSelectedCount();
    }
}

async function toggleAllPages() {
    console.log('toggleAllPages called');
    selectAllPagesChecked = document.getElementById('selectAllPages').checked;
    const checkboxes = document.querySelectorAll('.contact-checkbox');
    
    if (selectAllPagesChecked) {
        try {
            const response = await fetch('/contacts/get-all-ids/');
            const data = await response.json();
            console.log('Received contact IDs:', data.contact_ids);
            
            // Barcha kontakt ID'larini qo'shish
            data.contact_ids.forEach(id => {
                selectedIds.add(id.toString());
            });
            
            // Joriy sahifadagi checkboxlarni belgilash
            checkboxes.forEach(cb => {
                cb.checked = true;
            });
            
            document.getElementById('selectAll').checked = true;
        } catch (error) {
            console.error('Error fetching contact IDs:', error);
            alert('Kontakt ID\'larini olishda xatolik yuz berdi');
            document.getElementById('selectAllPages').checked = false;
            return;
        }
    } else {
        // Barcha tanlovlarni bekor qilish
        selectedIds.clear();
        checkboxes.forEach(cb => {
            cb.checked = false;
        });
        document.getElementById('selectAll').checked = false;
    }
    
    updateSelectedCount();
}

function toggleAllContacts() {
    console.log('toggleAllContacts called');
    const checkboxes = document.querySelectorAll('.contact-checkbox');
    const selectAllChecked = document.getElementById('selectAll').checked;
    
    checkboxes.forEach(cb => {
        cb.checked = selectAllChecked;
        if (selectAllChecked) {
            selectedIds.add(cb.value);
        } else {
            selectedIds.delete(cb.value);
        }
    });
    
    if (!selectAllChecked) {
        document.getElementById('selectAllPages').checked = false;
    }
    
    updateSelectedCount();
}

function updateSelectedCount() {
    console.log('updateSelectedCount called');
    const count = selectedIds.size;
    const countElement = document.getElementById('selectedCount');
    countElement.textContent = count + ' ta kontakt';
    console.log('Selected contacts count:', count);
    console.log('Selected IDs:', Array.from(selectedIds));
}

function confirmBulkDelete() {
    console.log('confirmBulkDelete called');
    const count = selectedIds.size;
    console.log('Selected count:', count);
    
    if (count === 0) {
        alert('Iltimos, o\'chirish uchun kontaktlarni tanlang');
        return false;
    }
    
    if (confirm(count + ' ta kontaktni o\'chirishni tasdiqlaysizmi?')) {
        console.log('User confirmed deletion');
        const form = document.getElementById('bulkDeleteForm');
        
        // Eski hidden inputlarni o'chirish
        form.querySelectorAll('input[name="contact_ids"]').forEach(input => {
            console.log('Removing existing input:', input.value);
            input.remove();
        });
        
        // Har bir tanlangan ID uchun yangi hidden input qo'shish
        selectedIds.forEach(id => {
            console.log('Adding hidden input for ID:', id);
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'contact_ids';
            input.value = id;
            form.appendChild(input);
        });
        
        console.log('Form will be submitted');
        return true;
    }
    console.log('User cancelled deletion');
    return false;
}

function toggleContact(checkbox) {
    console.log('toggleContact called for ID:', checkbox.value);
    if (checkbox.checked) {
        selectedIds.add(checkbox.value);
        console.log('Added ID:', checkbox.value);
    } else {
        selectedIds.delete(checkbox.value);
        document.getElementById('selectAllPages').checked = false;
        console.log('Removed ID:', checkbox.value);
    }
    updateSelectedCount();
}

// HTMX events
document.body.addEventListener('htmx:afterSwap', function(evt) {
    console.log('htmx:afterSwap event fired');
    if (deleteMode) {
        const checkboxes = document.querySelectorAll('.contact-checkbox');
        checkboxes.forEach(cb => {
            cb.classList.remove('hidden');
            if (selectedIds.has(cb.value)) {
                cb.checked = true;
            }
        });
    }
});
