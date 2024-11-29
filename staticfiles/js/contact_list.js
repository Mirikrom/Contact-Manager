let deleteMode = false;
let selectAllPagesChecked = false;
let selectedIds = new Set();

function toggleDeleteMode() {
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

function toggleAllPages() {
    selectAllPagesChecked = document.getElementById('selectAllPages').checked;
    const checkboxes = document.querySelectorAll('.contact-checkbox');
    
    if (selectAllPagesChecked) {
        checkboxes.forEach(cb => {
            cb.checked = true;
            selectedIds.add(cb.value);
        });
        document.getElementById('selectAll').checked = true;
    } else {
        checkboxes.forEach(cb => {
            cb.checked = false;
            selectedIds.delete(cb.value);
        });
        document.getElementById('selectAll').checked = false;
    }
    
    updateHiddenInputs(Array.from(selectedIds));
    updateSelectedCount();
}

function updateHiddenInputs(ids) {
    const form = document.getElementById('bulkDeleteForm');
    // Remove existing hidden inputs
    form.querySelectorAll('input[name="contact_ids"]').forEach(input => input.remove());
    
    // Add new hidden inputs
    ids.forEach(id => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'contact_ids';
        input.value = id;
        form.appendChild(input);
    });
}

function toggleAllContacts() {
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
    
    updateSelectedCount();
}

function updateSelectedCount() {
    const count = selectedIds.size;
    const countElement = document.getElementById('selectedCount');
    countElement.textContent = count + ' ta kontakt';
}

function confirmBulkDelete() {
    const count = selectedIds.size;
    if (count === 0) {
        alert('Iltimos, o\'chirish uchun kontaktlarni tanlang');
        return false;
    }
    return confirm(count + ' ta kontaktni o\'chirishni tasdiqlaysizmi?');
}

// HTMX events
document.body.addEventListener('htmx:afterSwap', function (evt) {
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
