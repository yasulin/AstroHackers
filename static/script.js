document.addEventListener('DOMContentLoaded', () => {
    const questionElement = document.getElementById('question');
    const answersElement = document.getElementById('answers');
    const modal = document.getElementById('quiz-modal');
    const closeModalButton = document.getElementById('close-modal');
    let correctAnswer = '';
    let description = '';

    async function fetchQuiz() {
        try {
            const response = await fetch('/get-quiz');
            const data = await response.json();
            displayQuiz(data.quiz);
        } catch (error) {
            console.error('Error fetching quiz:', error);
        }
    }

    // Expose fetchQuiz to the global scope
    window.fetchQuiz = fetchQuiz;

    function displayQuiz(data) {
        questionElement.textContent = data.question;
        correctAnswer = data.correct_answer;
        description = data.description;
        answersElement.innerHTML = data.answers.map((answer, index) => {
            const letter = String.fromCharCode(65 + index); // A, B, C, D
            return `<button onclick="selectAnswer('${letter}')">${answer}</button>`;
        }).join('');
        modal.style.display = 'block';
        closeModalButton.style.display = 'none';
    }

    window.selectAnswer = function(answer) {
        console.log(answer)
        console.log(correctAnswer)
        if (answer === correctAnswer) {
            questionElement.textContent = "Congratulations!";
            answersElement.innerHTML = '';
            closeModalButton.style.display = 'block';
        } else {
            questionElement.textContent = `Incorrect! The correct answer is ${correctAnswer}. ${description}`;
            answersElement.innerHTML = '<button onclick="fetchQuiz()">Next Question</button>';
        }
    };

    closeModalButton.onclick = function() {
        modal.style.display = 'none';
        window.close();
    };

    function blockAccess() {
        // Placeholder for blocking access logic
        // Consider using fullscreen mode or other methods to keep the user focused on the quiz
    }

    window.onload = blockAccess;
    fetchQuiz();
});
