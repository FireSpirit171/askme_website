const text = document.getElementById('answer');
const answerButton = document.getElementById('answerButton');

function checkInputs() {
    const textValue = text.value.trim();

    if (textValue !== '') {
        answerButton.removeAttribute('disabled');
    } else {
        answerButton.setAttribute('disabled', 'disabled');
    }
}

text.addEventListener('input', checkInputs);