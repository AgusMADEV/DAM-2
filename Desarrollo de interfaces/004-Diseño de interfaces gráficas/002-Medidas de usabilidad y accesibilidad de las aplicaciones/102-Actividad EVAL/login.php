<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Backoffice Empresarial</title>
    <style>
      body{
        margin: 0;
        padding: 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      
      #login{
        width: 450px;
        min-height: 550px;
        background: white;
        padding: 30px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.3);
        border-radius: 15px;
        margin: 50px auto;
      }
      #login h2{
        text-align: center;
        color: #333;
        margin-bottom: 30px;
        font-size: 24px;
      }
      #login .form-group{
        margin-bottom: 20px;
      }
      #login label{
        display: block;
        margin-bottom: 8px;
        color: #555;
        font-weight: bold;
        font-size: 14px;
      }
      #login input[type="text"],
      #login input[type="password"],
      #login select{
        width: 100%;
        padding: 12px;
        border: 2px solid #ddd;
        border-radius: 8px;
        font-size: 14px;
        box-sizing: border-box;
        transition: border-color 0.3s;
      }
      #login input[type="text"]:focus,
      #login input[type="password"]:focus,
      #login select:focus{
        outline: none;
        border-color: #4CAF50;
      }
      #login button{
        width: 100%;
        padding: 14px;
        background: #4CAF50;
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: background 0.3s;
        margin-top: 10px;
      }
      #login button:hover{
        background: #45a049;
      }
      #login .error-message{
        color: #d32f2f;
        font-size: 13px;
        margin-top: 5px;
        display: none;
      }
      #login .error-message.show{
        display: block;
      }
      #login .optional-label{
        font-weight: normal;
        color: #888;
        font-size: 12px;
        font-style: italic;
      }
      #login .social-login{
        margin-top: 25px;
        padding-top: 20px;
        border-top: 1px solid #ddd;
      }
      #login .social-login p{
        text-align: center;
        color: #666;
        font-size: 14px;
        margin-bottom: 15px;
      }
      #login .social-buttons{
        display: flex;
        gap: 10px;
        justify-content: space-between;
      }
      #login .social-btn{
        flex: 1;
        padding: 12px;
        border: none;
        border-radius: 8px;
        font-size: 14px;
        font-weight: bold;
        cursor: pointer;
        transition: opacity 0.3s;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
      }
      #login .social-btn:hover{
        opacity: 0.85;
      }
      #login .social-btn.facebook{
        background: #1877f2;
        color: white;
      }
      #login .social-btn.google{
        background: #ea4335;
        color: white;
      }
      #login .social-btn.steam{
        background: #171a21;
        color: white;
      }
      #login .hobby-section{
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin: 20px 0;
      }
      #login .hobby-section h3{
        font-size: 16px;
        color: #333;
        margin-top: 0;
        margin-bottom: 15px;
      }
    </style>
  </head>
  <body>
    <section id="login">
      <h2>Inicio de Sesión</h2>
      <form id="loginForm">
        <div class="form-group">
          <label for="usuario">Usuario:</label>
          <input type="text" id="usuario" name="usuario" required placeholder="Ingrese su usuario">
          <div class="error-message" id="errorUsuario">El usuario es requerido</div>
        </div>
        
        <div class="form-group">
          <label for="contrasena">Contraseña:</label>
          <input type="password" id="contrasena" name="contrasena" required placeholder="Ingrese su contraseña">
          <div class="error-message" id="errorContrasena">La contraseña es requerida</div>
        </div>
        
        <!-- Sección de Hobbies e Intereses -->
        <div class="hobby-section">
          <h3>🎯 Intereses Personales <span class="optional-label">(Opcional)</span></h3>
          
          <div class="form-group">
            <label for="deporte">Deporte favorito:</label>
            <select id="deporte" name="deporte">
              <option value="">Seleccione un deporte</option>
              <option value="futbol">⚽ Fútbol</option>
              <option value="baloncesto">🏀 Baloncesto</option>
              <option value="tenis">🎾 Tenis</option>
              <option value="natacion">🏊 Natación</option>
              <option value="ciclismo">🚴 Ciclismo</option>
              <option value="atletismo">🏃 Atletismo</option>
              <option value="otros">🏋️ Otros</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="nivelDeporte">Nivel de experiencia en deportes:</label>
            <select id="nivelDeporte" name="nivelDeporte">
              <option value="">Seleccione su nivel</option>
              <option value="principiante">🌱 Principiante</option>
              <option value="intermedio">⭐ Intermedio</option>
              <option value="avanzado">🏆 Avanzado</option>
              <option value="profesional">💎 Profesional</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="videojuego">Videojuego favorito:</label>
            <select id="videojuego" name="videojuego">
              <option value="">Seleccione un videojuego</option>
              <option value="fifa">⚽ FIFA/EA Sports FC</option>
              <option value="fortnite">🎮 Fortnite</option>
              <option value="minecraft">⛏️ Minecraft</option>
              <option value="lol">🎭 League of Legends</option>
              <option value="valorant">🔫 Valorant</option>
              <option value="cod">🎯 Call of Duty</option>
              <option value="gta">🚗 GTA</option>
              <option value="otros">🎲 Otros</option>
            </select>
          </div>
        </div>
        
        <button type="submit">Iniciar Sesión</button>
        
        <!-- Sección de inicio de sesión con redes sociales -->
        <div class="social-login">
          <p>O inicia sesión con:</p>
          <div class="social-buttons">
            <button type="button" class="social-btn facebook" onclick="loginConRedSocial('facebook')">
              <span>f</span> Facebook
            </button>
            <button type="button" class="social-btn google" onclick="loginConRedSocial('google')">
              <span>G</span> Google
            </button>
            <button type="button" class="social-btn steam" onclick="loginConRedSocial('steam')">
              <span>🎮</span> Steam
            </button>
          </div>
        </div>
      </form>
    </section>
    
    <script>
      // Función para login con redes sociales
      function loginConRedSocial(redSocial){
        alert(`Iniciando sesión con ${redSocial.charAt(0).toUpperCase() + redSocial.slice(1)}...`);
        console.log("Login con red social:", redSocial);
        // Aquí se integraría con la API de la red social correspondiente
        // window.location.href = "maestro.php?login=" + redSocial;
      }
      
      // Validación del formulario de login
      let formulario = document.querySelector("#loginForm");
      
      formulario.onsubmit = function(evento){
        evento.preventDefault(); // Prevenir envío por defecto
        
        let usuario = document.querySelector("#usuario").value;
        let contrasena = document.querySelector("#contrasena").value;
        let errorUsuario = document.querySelector("#errorUsuario");
        let errorContrasena = document.querySelector("#errorContrasena");
        
        // Obtener datos opcionales de hobbies
        let deporte = document.querySelector("#deporte").value;
        let nivelDeporte = document.querySelector("#nivelDeporte").value;
        let videojuego = document.querySelector("#videojuego").value;
        
        // Resetear errores
        errorUsuario.classList.remove("show");
        errorContrasena.classList.remove("show");
        
        let esValido = true;
        
        // Validar usuario
        if(usuario.trim() === ""){
          errorUsuario.classList.add("show");
          esValido = false;
        }
        
        // Validar contraseña
        if(contrasena.trim() === ""){
          errorContrasena.classList.add("show");
          esValido = false;
        }
        
        // Si es válido, procesar login
        if(esValido){
          console.log("Login exitoso para usuario:", usuario);
          
          // Mostrar información de hobbies si fueron proporcionados
          if(deporte || nivelDeporte || videojuego){
            console.log("Hobbies del usuario:");
            if(deporte) console.log("- Deporte:", deporte);
            if(nivelDeporte) console.log("- Nivel deportivo:", nivelDeporte);
            if(videojuego) console.log("- Videojuego:", videojuego);
          }
          
          // Construir URL con parámetros
          let url = "maestro.php?usuario=" + encodeURIComponent(usuario);
          if(deporte) url += "&deporte=" + encodeURIComponent(deporte);
          if(nivelDeporte) url += "&nivel=" + encodeURIComponent(nivelDeporte);
          if(videojuego) url += "&videojuego=" + encodeURIComponent(videojuego);
          
          // Aquí se puede redirigir al maestro con el usuario y sus hobbies
          window.location.href = url;
        }
      }
    </script>
  </body>
</html>
