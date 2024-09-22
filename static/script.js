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
            openFullScreen();
            showLoadingMessage();
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
        descriptionElement.textContent = '';
        correctAnswer = data.correct_answer;
        description = data.description;
        answersElement.innerHTML = data.answers.map((answer, index) => {
            const letter = String.fromCharCode(65 + index); // A, B, C, D
            return `<button onclick="selectAnswer('${letter}')">${answer}</button>`;
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

    function openFullScreen() {
        // Get the document element to enter full screen
        let elem = document.documentElement;

        if (elem.requestFullscreen) {
            elem.requestFullscreen();
        } else if (elem.mozRequestFullScreen) { // Firefox
            elem.mozRequestFullScreen();
        } else if (elem.webkitRequestFullscreen) { // Chrome, Safari, and Opera
            elem.webkitRequestFullscreen();
        } else if (elem.msRequestFullscreen) { // Internet Explorer / Edge
            elem.msRequestFullscreen();
        }
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
        window.close();
        // Start background transition
        startBackgroundTransition();
    };

    window.onload = function() {
        openFullScreen();
        fetchQuiz();
    };

    // Function to handle background transitions
    function startBackgroundTransition() {
        const originalBackground = document.body.style.backgroundImage;
        const firstImageUrl = 'url("static/closed-hatch.png")'; // Replace with the actual path to the first image
        const secondImageUrl = 'url("static/open-hatch.png")'; // Replace with the actual path to the second image

        // Set the first image as the background
        document.body.style.backgroundImage = firstImageUrl;
        document.body.classList.add('transition-background-1');

        // Display the first image for a configurable time
        setTimeout(() => {
            // Fade out the first image and fade in the second image
            document.body.classList.remove('transition-background-1');
            document.body.classList.add('transition-background-2');
            document.body.style.backgroundImage = secondImageUrl;

            // Display the second image for 1 seconds
            setTimeout(() => {
                // Revert to the original background
                document.body.classList.remove('transition-background-2');
                document.body.classList.add('transition-background-original');
                document.body.style.backgroundImage = originalBackground;
            }, 3000); // Display the second image for 1 seconds
        }, 1900); // Configurable time to display the first image
    }
});
