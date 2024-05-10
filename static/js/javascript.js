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
                alert('已经发送重置链接到你的邮箱');
            })
            .catch(error => {
                alert('发送邮件时出错，请稍后再试');
            });
        }
    });
});
