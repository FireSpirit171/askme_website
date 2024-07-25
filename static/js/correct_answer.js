function getCookieCorrectAnswer(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const initCorrectAnswer = () => {
    const correctAnswerCheckboxes = document.querySelectorAll('.correct-answer-checkbox');

    correctAnswerCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => handleCorrectAnswer(checkbox.getAttribute('data-answer-id'), checkbox.checked));
    });
}

const handleCorrectAnswer = async (answerId, isCorrect) => {
    try {
        const csrftoken = getCookieCorrectAnswer('csrftoken');
        const response = await fetch(`/correctanswer/${answerId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ is_correct: isCorrect })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        // Обновите цвет рамки в зависимости от статуса
        const answerCard = document.getElementById(`answer-${answerId}`);
        if (data.status === 'm') {
            answerCard.classList.add('border-success');
        } else {
            answerCard.classList.remove('border-success');
        }
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
}

document.addEventListener('DOMContentLoaded', initCorrectAnswer);
