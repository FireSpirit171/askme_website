// Получаем элементы input и кнопку
const usernameInput = document.getElementById('username');
const emailInput = document.getElementById('email');
const nicknameInput = document.getElementById('nickname');
const avatarInput = document.getElementById('avatar');
const saveButton = document.getElementById('saveButton');

// Функция для проверки заполнения полей
function checkInputs() {
    const usernameValue = usernameInput.value.trim();
    const emailValue = emailInput.value.trim();
    const nicknameValue = nicknameInput.value.trim();

    // Если хотя бы одно поле не пустое, активируем кнопку сохранения
    if (usernameValue !== '' || emailValue !== '' || nicknameValue !== '') {
        saveButton.removeAttribute('disabled');
    } else {
        // В противном случае, делаем кнопку неактивной
        saveButton.setAttribute('disabled', 'disabled');
    }
}

// Вызываем функцию при вводе в поля ввода
usernameInput.addEventListener('input', checkInputs);
emailInput.addEventListener('input', checkInputs);
nicknameInput.addEventListener('input', checkInputs);
avatarInput.addEventListener('input', checkInputs);  // Если у вас есть логика для проверки изменений в файле, добавьте это здесь
