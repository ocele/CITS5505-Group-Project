document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        const email = document.getElementById('email').value;
        if (!email.includes('@') || !email.includes('.')) {
            alert('Please enter the vaild email address');
            event.preventDefault();
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const email = document.getElementById('email').value;
        if (!email.includes('@') || !email.includes('.')) {
            alert('Please Enter the correct email address');
        } else {
            fetch('/send-reset-password-link', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: email })
            })
            .then(response => response.json())
            .then(data => {
                alert('Email has been send...');
            })
            .catch(error => {
                alert('Retry');
            });
        }
    });
});
