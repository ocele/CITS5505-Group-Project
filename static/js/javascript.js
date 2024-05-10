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
        event.preventDefault(); // 阻止表单默认提交行为

        const email = document.getElementById('email').value;
        if (!email.includes('@') || !email.includes('.')) {
            alert('请输入有效的电子邮件地址。');
        } else {
            // 模拟异步发送请求到服务器
            fetch('/send-reset-password-link', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: email })
            })
            .then(response => response.json())
            .then(data => {
                // 假设服务器返回一个消息告知邮件发送成功
                alert('已经发送重置链接到你的邮箱');
            })
            .catch(error => {
                // 错误处理
                alert('发送邮件时出错，请稍后再试');
            });
        }
    });
});
