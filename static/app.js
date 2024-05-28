document.addEventListener('DOMContentLoaded', function () {
    // Get elements
    const form = document.getElementById('loginForm');
    const messagesDiv = document.getElementById('messages');
    const loader = document.getElementById('loadingIndicator');

    form.onsubmit = async function (event) {
        event.preventDefault();

        // Clear old messages
        messagesDiv.innerHTML = '';

        // Show loader
        loader.style.display = 'inline';

        const action = form.getAttribute('action');
        const method = form.getAttribute('method');
        const formData = new FormData(form);

        try {
            const response = await fetch(action, {
                method: method.toUpperCase(),
                body: formData,
            });

            const data = await response.json();

            // Hide loader
            loader.style.display = 'none';

            if (response.ok) {
                messagesDiv.classList.remove('alert-danger');
                messagesDiv.classList.add('alert-success');
                messagesDiv.innerText = data.message;
            } else {
                messagesDiv.classList.remove('alert-success');
                messagesDiv.classList.add('alert-danger');
                messagesDiv.innerText = data.message || 'An error occurred';
            }
        } catch (error) {
            console.error('Error:', error);

            // Hide loader
            loader.style.display = 'none';

            messagesDiv.classList.remove('alert-success');
            messagesDiv.classList.add('alert-danger');
            messagesDiv.innerText = 'An error occurred. Check the browser console for more details.'
        }
    };
});
document.addEventListener('DOMContentLoaded', function () {
    const recordButton = document.getElementById('recordButton');
    const status = document.getElementById('status');
    const attendanceForm = document.getElementById('attendanceForm');
    const textInput = document.getElementById('text');

    if (window.SpeechRecognition || window.webkitSpeechRecognition) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recordButton.onclick = function () {
            status.textContent = 'Listening...';
            recognition.start();
        };

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript.trim().toLowerCase();
            status.textContent = `You said: ${transcript}`;
            textInput.value = transcript;

            console.log('Transcript:', transcript);
        };

        recognition.onerror = function (event) {
            console.error('Recognition error:', event);
            status.textContent = 'Error occurred in recognition: ' + event.error;
        };

        recognition.onend = function () {
            console.log('Recognition ended.');
            status.textContent = 'Click the button to record again.';
        };
    } else {
        status.textContent = 'Your browser does not support speech recognition.';
        recordButton.disabled = true;
    }

    attendanceForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default form submission

        const formData = new FormData(attendanceForm);
        fetch(attendanceForm.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                status.textContent = data.message;

                if (data.message === 'Attendance recorded successfully') {
                    // Optionally clear the form or redirect
                    attendanceForm.reset();
                    recordButton.disabled = true; // Disable the record button
                }
            } else {
                status.textContent = 'An unexpected error occurred.';
            }
        })
        .catch(error => {
            console.error('Submission error:', error);
            status.textContent = 'An error occurred: ' + error.message;
        });
    });
});
