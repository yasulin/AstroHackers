document.addEventListener('DOMContentLoaded', () => {
    const questionElement = document.getElementById('question');
    const descriptionElement = document.getElementById('description');
    console.log(questionElement)
    console.log(descriptionElement)
    const answersElement = document.getElementById('answers');
    const modal = document.getElementById('quiz-modal');
    const closeModalButton = document.getElementById('close-modal');
    let correctAnswer = '';
    let description = '';

    async function fetchQuiz() {
        try {
            showLoadingMessage();
            const response = await fetch('/get-quiz');
            const data = await response.json();
            displayQuiz(data);
        } catch (error) {
            console.error('Error fetching quiz:', error);
        }
    }

    // Expose fetchQuiz to the global scope
    window.fetchQuiz = fetchQuiz;

    function displayQuiz(data) {
        questionElement.textContent = data.question;
        descriptionElement.textContent = '';
        correctAnswer = data.correct_answer;
        description = data.description;
        answersElement.innerHTML = data.answers.map((answer) => {
            return `<button onclick="selectAnswer('${answer}')">${answer}</button>`;
        }).join('');
        modal.style.display = 'flex';
        closeModalButton.style.display = 'none';
    }

    function showLoadingMessage() {
        questionElement.textContent = "Loading question...";
        descriptionElement.textContent = '';
        answersElement.innerHTML = '';
        modal.style.display = 'flex';
        closeModalButton.style.display = 'none';
    }

    window.selectAnswer = function(answer) {
        console.log(answer);
        console.log(correctAnswer);
        if (answer === correctAnswer) {
            questionElement.textContent = "Congratulations!";
            descriptionElement.textContent = '';
            answersElement.innerHTML = '';
            closeModalButton.style.display = 'flex';

        } else {
            questionElement.textContent = `Incorrect! The correct answer is ${correctAnswer}.`;
            descriptionElement.textContent = description;
            answersElement.innerHTML = '<button onclick="fetchQuiz()">Next Question</button>';
        }
    };

    closeModalButton.onclick = function() {
        modal.style.display = 'none';
        // window.close();
    };

    window.onload = function() {
        fetchQuiz();
    };

});
