document.addEventListener('DOMContentLoaded', function() {
    // إدارة رسائل الخطأ
    const errorMessage = document.querySelector('.error-message');
    
    if (errorMessage && errorMessage.textContent.trim() !== '') {
        errorMessage.style.display = 'block';
        
        // إخفاء رسالة الخطأ تلقائياً بعد 5 ثواني
        setTimeout(() => {
            errorMessage.style.opacity = '0';
            setTimeout(() => {
                errorMessage.style.display = 'none';
            }, 300);
        }, 5000);
    }

    // إضافة تأثيرات للحقول عند التركيز
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.style.boxShadow = '0 0 0 2px #ff66b2';
        });
        
        input.addEventListener('blur', function() {
            this.style.boxShadow = 'none';
        });
    });

    // التحقق من صحة المدخلات قبل الإرسال
    const loginForm = document.querySelector('form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const username = this.querySelector('input[name="username"]');
            const password = this.querySelector('input[name="password"]');
            
            if (username.value.trim() === '' || password.value.trim() === '') {
                e.preventDefault();
                showError('Please fill in all fields');
            }
        });
    }
});

function showError(message) {
    let errorDiv = document.querySelector('.error-message');
    
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        const form = document.querySelector('form');
        form.insertBefore(errorDiv, form.querySelector('.login-btn'));
    }
    
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    errorDiv.style.opacity = '1';
    
    // إخفاء رسالة الخطأ تلقائياً بعد 5 ثواني
    setTimeout(() => {
        errorDiv.style.opacity = '0';
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 300);
    }, 5000);
}