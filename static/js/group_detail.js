// Global o'zgaruvchilar
let deleteMode = false;
let selectAllPages = false;
let allContactIds = [];
let selectedIds = new Set();

// DOMContentLoaded event listener
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
});

function initializeEventListeners() {
    console.log('Initializing event listeners');
    const deleteButton = document.getElementById('deleteMode');
    if (deleteButton) {
        // Eski event listenerlarni tozalash
        deleteButton.removeEventListener('click', toggleDeleteMode);
        // Yangi event listener qo'shish
        deleteButton.addEventListener('click', toggleDeleteMode);
    }
    
    const selectAllCheckbox = document.getElementById('selectAll');
    if (selectAllCheckbox) {
        selectAllCheckbox.removeEventListener('change', toggleAllContacts);
        selectAllCheckbox.addEventListener('change', toggleAllContacts);
    }
    
    const selectAllPagesCheckbox = document.getElementById('selectAllPages');
    if (selectAllPagesCheckbox) {
        selectAllPagesCheckbox.removeEventListener('change', toggleAllPages);
        selectAllPagesCheckbox.addEventListener('change', toggleAllPages);
    }
    
    // Kontakt checkboxlariga event listener qo'shish
    const checkboxes = document.querySelectorAll('.contact-checkbox');
    checkboxes.forEach(cb => {
        cb.removeEventListener('change', updateSelectedCount);
        cb.addEventListener('change', updateSelectedCount);
    });
}

function toggleDeleteMode(event) {
    // Default xatti-harakatni to'xtatish
    if (event) {
        event.preventDefault();
    }
    
    console.log('toggleDeleteMode called');
    deleteMode = !deleteMode;
    console.log('Delete mode:', deleteMode);
    
    selectAllPages = false;
    allContactIds = [];
    selectedIds.clear();
    
    const controls = document.getElementById('deleteModeControls');
    const checkboxes = document.querySelectorAll('.contact-checkbox');
    const deleteButton = document.getElementById('deleteMode');
    
    if (deleteMode) {
        console.log('Enabling delete mode');
        if (controls) {
            controls.classList.remove('hidden');
            console.log('Controls shown');
        }
        if (deleteButton) {
            deleteButton.classList.remove('bg-red-600', 'hover:bg-red-700');
            deleteButton.classList.add('bg-gray-600', 'hover:bg-gray-700');
        }
        checkboxes.forEach(cb => {
            cb.classList.remove('hidden');
        });
    } else {
        console.log('Disabling delete mode');
        if (controls) {
            controls.classList.add('hidden');
            console.log('Controls hidden');
        }
        if (deleteButton) {
            deleteButton.classList.remove('bg-gray-600', 'hover:bg-gray-700');
            deleteButton.classList.add('bg-red-600', 'hover:bg-red-700');
        }
        checkboxes.forEach(cb => {
            cb.classList.add('hidden');
            cb.checked = false;
        });
        
        const selectAllCheckbox = document.getElementById('selectAll');
        const selectAllPagesCheckbox = document.getElementById('selectAllPages');
        if (selectAllCheckbox) selectAllCheckbox.checked = false;
        if (selectAllPagesCheckbox) selectAllPagesCheckbox.checked = false;
    }
    updateSelectedCount();
}

async function toggleAllPages() {
    console.log('toggleAllPages called');
    const selectAllPagesCheckbox = document.getElementById('selectAllPages');
    selectAllPages = selectAllPagesCheckbox.checked;
    
    const selectAllCheckbox = document.getElementById('selectAll');
    const checkboxes = document.querySelectorAll('.contact-checkbox');
    
    if (selectAllPages) {
        try {
            const groupId = document.querySelector('[data-group-id]').dataset.groupId;
            console.log('Group ID:', groupId);
            
            // To'g'ri URL manzili
            const response = await fetch(`/groups/${groupId}/contact-ids/`);
            if (!response.ok) {
                console.error('Server response:', response.status, response.statusText);
                throw new Error('Failed to fetch contact IDs');
            }
            
            const data = await response.json();
            console.log('Received contact IDs:', data.contact_ids);
            
            allContactIds = data.contact_ids;
            selectedIds = new Set(data.contact_ids.map(String));
            
            checkboxes.forEach(cb => cb.checked = true);
            if (selectAllCheckbox) selectAllCheckbox.checked = true;
            
            updateHiddenInputs(allContactIds);
            
            const countDisplay = document.getElementById('selectedCount');
            const deleteButtonCount = document.getElementById('deleteButtonCount');
            if (countDisplay) countDisplay.textContent = `${data.contact_ids.length} ta kontakt`;
            if (deleteButtonCount) deleteButtonCount.textContent = data.contact_ids.length;
            
        } catch (error) {
            console.error('Kontaktlar ID larini olishda xatolik:', error);
            selectAllPages = false;
            selectAllPagesCheckbox.checked = false;
            if (selectAllCheckbox) selectAllCheckbox.checked = false;
        }
    } else {
        allContactIds = [];
        selectedIds.clear();
        checkboxes.forEach(cb => cb.checked = false);
        if (selectAllCheckbox) selectAllCheckbox.checked = false;
        updateHiddenInputs([]);
        updateSelectedCount();
    }
}

function toggleAllContacts() {
    console.log('toggleAllContacts called');
    if (selectAllPages) {
        const selectAllPagesCheckbox = document.getElementById('selectAllPages');
        if (selectAllPagesCheckbox) {
            selectAllPagesCheckbox.checked = false;
            toggleAllPages();
        }
        return;
    }
    
    const selectAllCheckbox = document.getElementById('selectAll');
    const isChecked = selectAllCheckbox.checked;
    const checkboxes = document.querySelectorAll('.contact-checkbox');
    
    checkboxes.forEach(cb => {
        cb.checked = isChecked;
        if (isChecked) {
            selectedIds.add(cb.value);
        } else {
            selectedIds.delete(cb.value);
        }
    });
    
    updateSelectedCount();
}

function updateSelectedCount() {
    if (selectAllPages) return;
    
    const checkboxes = document.querySelectorAll('.contact-checkbox:checked');
    const count = checkboxes.length;
    
    const countDisplay = document.getElementById('selectedCount');
    const deleteButtonCount = document.getElementById('deleteButtonCount');
    
    if (countDisplay) countDisplay.textContent = `${count} ta kontakt`;
    if (deleteButtonCount) deleteButtonCount.textContent = count;
    
    const selectedIdsArray = Array.from(checkboxes).map(cb => parseInt(cb.value));
    updateHiddenInputs(selectedIdsArray);
}

function updateHiddenInputs(ids) {
    const form = document.getElementById('bulkDeleteForm');
    if (!form) return;
    
    form.querySelectorAll('input[name="contact_ids[]"]').forEach(input => input.remove());
    
    ids.forEach(id => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'contact_ids[]';
        input.value = id;
        form.appendChild(input);
    });
}

function confirmBulkDelete() {
    const form = document.getElementById('bulkDeleteForm');
    if (!form) return false;
    
    const contactIds = form.querySelectorAll('input[name="contact_ids[]"]');
    if (contactIds.length === 0) {
        alert("Iltimos, o'chirish uchun kontaktlarni tanlang");
        return false;
    }
    
    return confirm(`${contactIds.length} ta kontaktni guruhdan o'chirishni tasdiqlaysizmi?`);
}

// HTMX events
document.body.addEventListener('htmx:afterSwap', function(evt) {
    console.log('htmx:afterSwap event fired');
    if (deleteMode) {
        const checkboxes = document.querySelectorAll('.contact-checkbox');
        checkboxes.forEach(cb => {
            cb.classList.remove('hidden');
            if (selectAllPages || selectedIds.has(cb.value)) {
                cb.checked = true;
            }
        });
        
        if (selectAllPages && allContactIds.length > 0) {
            updateHiddenInputs(allContactIds);
        }
        
        // Event listenerlarni qayta qo'shish
        initializeEventListeners();
    }
});

// Modal functions
// Modal oynani ochish
function openModal() {
    document.getElementById('contactModal').classList.remove('hidden');
    document.getElementById('searchContact').value = '';
    searchContacts();
    // Modal ochilganda qo'shish tugmasini yashirish
    document.getElementById('addButton').classList.add('hidden');
}

// Modal oynani yopish
function closeModal() {
    document.getElementById('contactModal').classList.add('hidden');
}

// Kontaktlarni qidirish
function searchContacts() {
    const searchText = document.getElementById('searchContact').value.toLowerCase();
    const contacts = document.getElementsByClassName('contact-item');
    
    Array.from(contacts).forEach(function(contact) {
        const label = contact.getElementsByTagName('label')[0];
        const text = label.textContent.toLowerCase();
        
        if (text.includes(searchText)) {
            contact.style.display = "";
        } else {
            contact.style.display = "none";
        }
    });
}

// Checkbox holatini tekshirish
function checkSelectedContacts() {
    const checkboxes = document.querySelectorAll('input[type="checkbox"][name="contacts"]');
    const addButton = document.getElementById('addButton');
    
    // Kamida bitta checkbox tanlangan bo'lsa
    const hasSelected = Array.from(checkboxes).some(checkbox => checkbox.checked);
    
    // Qo'shish tugmasini ko'rsatish yoki yashirish
    if (hasSelected) {
        addButton.classList.remove('hidden');
    } else {
        addButton.classList.add('hidden');
    }
}
