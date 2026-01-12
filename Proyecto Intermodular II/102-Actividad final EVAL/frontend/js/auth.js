// auth.js - Manejo de autenticación

// Configuración
const API_URL = 'http://localhost:5000';

// Toggle password visibility
function togglePassword() {
    const passwordInput = document.getElementById('password');
    const toggleBtn = document.querySelector('.toggle-password i');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleBtn.classList.remove('fa-eye');
        toggleBtn.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        toggleBtn.classList.remove('fa-eye-slash');
        toggleBtn.classList.add('fa-eye');
    }
}

// Manejo del formulario de login
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('loginError');
    const submitBtn = e.target.querySelector('button[type="submit"]');
    
    // Deshabilitar botón y mostrar loading
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Iniciando sesión...';
    errorDiv.style.display = 'none';
    
    // Simulación de login (en producción aquí iría la llamada al backend PHP)
    try {
        // Por ahora validamos con usuarios hardcoded
        const validUsers = {
            'admin': 'admin123',
            'vendedor1': 'admin123',
            'gerente1': 'admin123'
        };
        
        await new Promise(resolve => setTimeout(resolve, 1000)); // Simular delay
        
        if (validUsers[username] && validUsers[username] === password) {
            // Login exitoso
            const userData = {
                username: username,
                nombre: username === 'admin' ? 'Administrador Sistema' : 
                        username === 'vendedor1' ? 'Juan Pérez' : 'Laura Martínez',
                rol: username === 'admin' ? 'Administrador' : 
                     username.startsWith('vendedor') ? 'Vendedor' : 'Gerente',
                loginTime: new Date().toISOString()
            };
            
            // Guardar datos en localStorage
            localStorage.setItem('user', JSON.stringify(userData));
            localStorage.setItem('isLoggedIn', 'true');
            
            // Redireccionar al dashboard
            window.location.href = 'dashboard.html';
        } else {
            throw new Error('Credenciales incorrectas');
        }
    } catch (error) {
        errorDiv.textContent = '❌ ' + error.message;
        errorDiv.style.display = 'block';
        
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-sign-in-alt"></i> Iniciar Sesión';
    }
});

// Verificar si ya está logueado
if (window.location.pathname.includes('dashboard.html')) {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    if (!isLoggedIn) {
        window.location.href = 'index.html';
    }
}
