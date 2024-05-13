const init = () => {
    const questions = document.querySelectorAll('.card')

    for (const question of questions) {
        const likeButton = question.querySelector('like-btn')
        const dislikeButton = question.querySelector('dislike-btn')
        const likeCounter = question.querySelector('like-counter')
    }
}