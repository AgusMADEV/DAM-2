// JavaScript para la página de login
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const errorMessage = document.getElementById('error-message');

    // Manejar el envío del formulario de login
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const submitBtn = document.querySelector('.btn-login');
        
        // Validación básica
        if (!username || !password) {
            showError('Por favor, complete todos los campos.');
            return;
        }
        
        // Mostrar estado de carga
        submitBtn.classList.add('loading');
        submitBtn.textContent = 'Iniciando sesión...';
        submitBtn.disabled = true;
        hideError();
        
        try {
            // Realizar petición de login al backend
            const response = await fetch('../backend/api/login.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Guardar token/sesión
                localStorage.setItem('erp_token', data.token);
                localStorage.setItem('erp_user', JSON.stringify(data.user));
                
                // Redirigir al dashboard
                window.location.href = 'dashboard.html';
            } else {
                showError(data.message || 'Error al iniciar sesión. Verifique sus credenciales.');
            }
            
        } catch (error) {
            console.error('Error en login:', error);
            showError('Error de conexión. Por favor, intente nuevamente.');
        } finally {
            // Restaurar estado del botón
            submitBtn.classList.remove('loading');
            submitBtn.textContent = 'Iniciar Sesión';
            submitBtn.disabled = false;
        }
    });
    
    // Función para mostrar errores
    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
    }
    
    // Función para ocultar errores
    function hideError() {
        errorMessage.style.display = 'none';
    }
    
    // Verificar si ya hay una sesión activa
    const token = localStorage.getItem('erp_token');
    if (token) {
        // Verificar token con el servidor
        fetch('../backend/api/verify-token.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.valid) {
                window.location.href = 'dashboard.html';
            } else {
                // Token inválido, limpiar storage
                localStorage.removeItem('erp_token');
                localStorage.removeItem('erp_user');
            }
        })
        .catch(error => {
            console.error('Error verificando token:', error);
        });
    }
    
    // Permitir envío con Enter
    document.getElementById('password').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            loginForm.dispatchEvent(new Event('submit'));
        }
    });
});