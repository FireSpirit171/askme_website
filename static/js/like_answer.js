function getAnswerCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const initAnswer = () => {
    const likeButtons = document.querySelectorAll('.like-btn-answer');
    const dislikeButtons = document.querySelectorAll('.dislike-btn-answer');

    likeButtons.forEach(button => {
        button.addEventListener('click', () => handleLikeDislikeAnswer(button.getAttribute('data-answer-id'), 'like'));
    });

    dislikeButtons.forEach(button => {
        button.addEventListener('click', () => handleLikeDislikeAnswer(button.getAttribute('data-answer-id'), 'dislike'));
    });
}

const handleLikeDislikeAnswer = async (answerId, action) => {
    try {
        const csrftoken = getAnswerCookie('csrftoken');
        const response = await fetch(`/likeanswer/${answerId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ action })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        const likeCounter = document.querySelector(`#answerlike-counter-${answerId}`);
        
        // Обновляем значение счетчика лайков на странице
        if (likeCounter) {
            likeCounter.value = data.likes;
        }

        const likeButton = document.getElementById(`answerlikeButton-${answerId}`);
        const dislikeButton = document.getElementById(`answerdislikeButton-${answerId}`);

        if (data.user_status === "l") {
            likeButton.classList.remove('btn-outline-success');
            likeButton.classList.add('btn-success');
            dislikeButton.classList.remove('btn-danger');
            dislikeButton.classList.add('btn-outline-danger');
        } else if (data.user_status === "d") {
            dislikeButton.classList.remove('btn-outline-danger');
            dislikeButton.classList.add('btn-danger');
            likeButton.classList.remove('btn-success');
            likeButton.classList.add('btn-outline-success');
        } else {
            likeButton.classList.remove('btn-success');
            likeButton.classList.add('btn-outline-success');
            dislikeButton.classList.remove('btn-danger');
            dislikeButton.classList.add('btn-outline-danger');
        }
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
}

document.addEventListener('DOMContentLoaded', initAnswer);

