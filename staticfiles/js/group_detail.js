let deleteMode = false;
let selectAllPagesChecked = false;
let selectedIds = new Set();

// Initialize event listeners when the page loads
document.addEventListener('DOMContentLoaded', function() {
    const selectAllCheckbox = document.getElementById('selectAll');
    const selectAllPagesCheckbox = document.getElementById('selectAllPages');
    
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', toggleAllContacts);
    }
    
    if (selectAllPagesCheckbox) {
        selectAllPagesCheckbox.addEventListener('change', toggleAllPages);
    }
    
    // Add event listener for individual checkboxes
    document.querySelectorAll('.contact-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', handleCheckboxChange);
    });
});

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
        const groupId = document.querySelector('[data-group-id]').dataset.groupId;
        fetch(`/contacts/groups/${groupId}/contact-ids/`)
            .then(response => response.json())
            .then(data => {
                selectedIds.clear(); // Clear before adding new IDs
                data.contact_ids.forEach(id => selectedIds.add(id.toString()));
                checkboxes.forEach(cb => {
                    cb.checked = true;
                });
                document.getElementById('selectAll').checked = true;
                updateSelectedCount();
            })
            .catch(error => {
                console.error('Kontaktlar ID larini olishda xatolik:', error);
                selectAllPagesChecked = false;
                document.getElementById('selectAllPages').checked = false;
            });
    } else {
        selectedIds.clear(); // Clear when unchecking all pages
        checkboxes.forEach(cb => {
            cb.checked = false;
        });
        document.getElementById('selectAll').checked = false;
        updateSelectedCount();
    }
}

function toggleAllContacts() {
    const selectAllChecked = document.getElementById('selectAll').checked;
    const checkboxes = document.querySelectorAll('.contact-checkbox');
    
    if (selectAllChecked) {
        checkboxes.forEach(cb => {
            cb.checked = true;
            selectedIds.add(cb.value);
        });
    } else {
        selectedIds.clear(); // Clear when unchecking all
        checkboxes.forEach(cb => {
            cb.checked = false;
        });
        // Also uncheck "select all pages" if it was checked
        document.getElementById('selectAllPages').checked = false;
        selectAllPagesChecked = false;
    }
    
    updateSelectedCount();
}

function handleCheckboxChange(event) {
    const checkbox = event.target;
    if (checkbox.checked) {
        selectedIds.add(checkbox.value);
    } else {
        selectedIds.delete(checkbox.value);
        // If any checkbox is unchecked, uncheck both "select all" checkboxes
        document.getElementById('selectAll').checked = false;
        document.getElementById('selectAllPages').checked = false;
        selectAllPagesChecked = false;
    }
    updateSelectedCount();
}

function updateSelectedCount() {
    const count = selectedIds.size;
    document.getElementById('selectedCount').textContent = `${count} ta kontakt`;
    document.getElementById('deleteButtonCount').textContent = count;
    
    // Update hidden inputs for form submission
    const form = document.getElementById('bulkDeleteForm');
    if (!form) return;
    
    // Remove existing hidden inputs
    form.querySelectorAll('input[name="contact_ids"]').forEach(input => input.remove());
    
    // Add new hidden inputs
    Array.from(selectedIds).forEach(id => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'contact_ids';
        input.value = id;
        form.appendChild(input);
    });
}

function confirmBulkDelete() {
    const selectedCount = selectedIds.size;
    if (selectedCount === 0) {
        alert("Iltimos, guruhdan o'chirish uchun kontaktlarni tanlang");
        return false;
    }
    return confirm(`${selectedCount} ta kontaktni guruhdan olib tashlashni tasdiqlaysizmi? (Kontaktlar o'chirilmaydi, faqat guruhdan olib tashlanadi)`);
}

// HTMX events
document.body.addEventListener('htmx:afterSwap', function(evt) {
    if (deleteMode) {
        const checkboxes = document.querySelectorAll('.contact-checkbox');
        checkboxes.forEach(cb => {
            cb.classList.remove('hidden');
            if (selectAllPagesChecked || selectedIds.has(cb.value)) {
                cb.checked = true;
            }
            // Re-attach event listener after HTMX swap
            cb.addEventListener('change', handleCheckboxChange);
        });
    } else {
        document.querySelectorAll('.contact-checkbox').forEach(cb => {
            cb.classList.add('hidden');
            cb.checked = false;
        });
    }
});
