document.addEventListener('DOMContentLoaded', () => {
    const questionElement = document.getElementById('question');
    const answersElement = document.getElementById('answers');
    const submitButton = document.getElementById('submit-button');

    async function fetchQuiz() {
        try {
            const response = await fetch('/get-quiz');
            const data = await response.json();
            displayQuiz(data);
        } catch (error) {
            console.error('Error fetching quiz:', error);
        }
    }

    function displayQuiz(data) {
        questionElement.textContent = data.question;
        answersElement.innerHTML = data.answers.map(answer => `<button>${answer}</button>`).join('');
    }

    submitButton.addEventListener('click', () => {
        // Add logic to handle answer submission and validation
        alert('The answer has been sent!');
    });

    fetchQuiz();
});
