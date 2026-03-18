document.addEventListener('DOMContentLoaded', function() {
    // إدارة رسائل الخطأ
    const errorDiv = document.querySelector('.error-message');
    
    if (errorDiv && errorDiv.textContent.trim() !== '') {
        errorDiv.style.display = 'block';
        
        // إخفاء رسالة الخطأ تلقائياً بعد 5 ثواني
        setTimeout(() => {
            errorDiv.style.opacity = '0';
            setTimeout(() => {
                errorDiv.style.display = 'none';
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
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const adminKeyInput = this.querySelector('input[name="admin_key"]');
            
            if (adminKeyInput.value.trim() === '') {
                e.preventDefault();
                showError('Please enter admin key');
            }
        });
    }
});

function showError(message) {
    const errorDiv = document.querySelector('.error-message');
    
    if (errorDiv) {
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
}