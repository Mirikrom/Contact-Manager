// Sessiya vaqtini yangilash
let sessionTimeout;
const SESSION_TIMEOUT = 30 * 60 * 1000; // 30 daqiqa

function resetTimer() {
    clearTimeout(sessionTimeout);
    sessionTimeout = setTimeout(logout, SESSION_TIMEOUT);
}

function logout() {
    document.getElementById('logoutForm').submit();
}

// Foydalanuvchi harakatlarini kuzatish
document.addEventListener('mousemove', resetTimer);
document.addEventListener('mousedown', resetTimer);
document.addEventListener('keypress', resetTimer);

// Dastlabki timer ni o'rnatish
resetTimer();
