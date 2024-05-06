// login.js

// Получаем элементы input и кнопку
const usernameInput = document.getElementById('usernameInput');
const passwordInput = document.getElementById('passwordInput');
const loginButton = document.getElementById('loginButton');

// Функция для проверки заполнения полей
function checkInputs() {
    const usernameValue = usernameInput.value.trim();
    const passwordValue = passwordInput.value.trim();

    // Если оба поля не пустые, разблокируем кнопку
    if (usernameValue !== '' && passwordValue !== '') {
        loginButton.removeAttribute('disabled');
    } else {
        // В противном случае блокируем кнопку
        loginButton.setAttribute('disabled', 'disabled');
    }
}

// Вызываем функцию при вводе в поля ввода
usernameInput.addEventListener('input', checkInputs);
passwordInput.addEventListener('input', checkInputs);
