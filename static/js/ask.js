const title= document.getElementById('title');
const text = document.getElementById('text');
const tags = document.getElementById('tags');
const askButton = document.getElementById('askButton');

function checkInputs() {
    const titleValue = title.value.trim();
    const textValue = text.value.trim();
    const tagsValue = tags.value.trim();

    if (titleValue !== '' && textValue !== '' && tagsValue !== '') {
        askButton.removeAttribute('disabled');
    } else {
        askButton.setAttribute('disabled', 'disabled');
    }
}

title.addEventListener('input', checkInputs);
text.addEventListener('textarea', checkInputs);
tags.addEventListener('input', checkInputs);