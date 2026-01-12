// chat.js - Lógica del chat con IA

const API_IA_URL = 'http://localhost:5000';
let conversationId = 1; // ID del usuario actual

// Abrir modal de chat
function openChat() {
    const modal = document.getElementById('chatModal');
    modal.classList.add('active');
    document.getElementById('chatInput').focus();
    
    // Mensaje de bienvenida si está vacío
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages.children.length === 0) {
        addMessage('assistant', '¡Hola! 👋 Soy tu asistente inteligente. Puedo ayudarte con información sobre productos, ventas, clientes y más. ¿En qué puedo ayudarte?');
    }
}

// Cerrar modal de chat
function closeChat() {
    const modal = document.getElementById('chatModal');
    modal.classList.remove('active');
}

// Agregar mensaje al chat
function addMessage(role, content) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    // Formatear contenido (convertir saltos de línea a <br>)
    const formattedContent = content.replace(/\n/g, '<br>');
    messageDiv.innerHTML = formattedContent;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Mostrar indicador de carga
function showLoading() {
    const chatMessages = document.getElementById('chatMessages');
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message loading';
    loadingDiv.id = 'loadingMessage';
    loadingDiv.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Pensando...';
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Ocultar indicador de carga
function hideLoading() {
    const loadingMessage = document.getElementById('loadingMessage');
    if (loadingMessage) {
        loadingMessage.remove();
    }
}

// Enviar mensaje a la IA
async function sendMessage() {
    const input = document.getElementById('chatInput');
    const mensaje = input.value.trim();
    
    if (!mensaje) return;
    
    // Agregar mensaje del usuario
    addMessage('user', mensaje);
    input.value = '';
    
    // Mostrar loading
    showLoading();
    
    try {
        // Llamar a la API del servicio IA
        const response = await fetch(`${API_IA_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mensaje: mensaje,
                usuario_id: conversationId
            })
        });
        
        if (!response.ok) {
            throw new Error('Error en la comunicación con el servicio IA');
        }
        
        const data = await response.json();
        
        // Ocultar loading
        hideLoading();
        
        // Agregar respuesta de la IA
        addMessage('assistant', data.respuesta);
        
        // Si la consulta es de stock bajo, recargar las alertas
        if (mensaje.toLowerCase().includes('stock')) {
            await cargarAlertasStock();
        }
        
    } catch (error) {
        hideLoading();
        addMessage('assistant', '❌ Lo siento, hubo un error al procesar tu solicitud. Asegúrate de que el servicio de IA esté funcionando.');
        console.error('Error:', error);
    }
}

// Preguntar directamente a la IA (desde botones)
function askIA(pregunta) {
    openChat();
    document.getElementById('chatInput').value = pregunta;
    sendMessage();
}

// Manejar Enter en el input
function handleChatEnter(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Cerrar modal al hacer clic fuera
document.getElementById('chatModal')?.addEventListener('click', (e) => {
    if (e.target.id === 'chatModal') {
        closeChat();
    }
});
