Este proyecto fusiona **reconocimiento de voz y síntesis de voz** para crear una experiencia interactiva que combine mis intereses personales: **los deportes, viajar y dibujar**.  
La idea es ofrecer una aplicación capaz de **escuchar comandos hablados** (por ejemplo, “eliminar uno”) y **responder de forma hablada**, generando así una **interfaz natural de usuario**.  
El contexto del ejercicio pertenece al módulo de **Desarrollo de Interfaces Naturales de Usuario**, donde se busca crear entornos web más humanos y accesibles mediante el uso del micrófono y el altavoz como medios de entrada y salida.

---

El código implementa correctamente las dos partes clave:  
- **Reconocimiento de voz** mediante la API `SpeechRecognition`.  
- **Síntesis de voz** usando `SpeechSynthesisUtterance`.

### Detalle técnico  
1. **Datos iniciales**  
   Se define un array de clientes con sus datos personales y su deporte favorito:
   ```js
   clientes = [
     {"nombre":"Agustín","apellidos":"Morcillo Aguado","email":"info@agusmadev.com","deporte":"baloncesto"},
     {"nombre":"Elena","apellidos":"Botezatu","email":"info@elena.com","deporte":"voleybol"},
     {"nombre":"Lilo","apellidos":"Aguado","email":"info@lilo.com","deporte":"atletismo"}
   ]
   ```
   Estos datos se muestran dinámicamente en una tabla HTML mediante la función `pintaTabla()`.

2. **Reconocimiento de voz**  
   El objeto `SpeechRecognition` escucha el micrófono y detecta lo que el usuario dice:
   ```js
   const rec = new SpeechRecognition();
   rec.lang = "es-ES";
   rec.onresult = function(e){ 
     let reconocido = e.results[0][0].transcript;
     document.getElementById("out").textContent = reconocido;
   }
   ```
   El texto reconocido se muestra en pantalla dentro del `<div id="out">`.

3. **Síntesis de voz**  
   Una vez reconocida la frase, el sistema **repite en voz alta** lo que ha entendido:
   ```js
   const u = new SpeechSynthesisUtterance(reconocido);
   const v = pickVoice();
   if (v) u.voice = v;
   u.lang = (v && v.lang) || 'es-ES';
   speechSynthesis.speak(u);
   ```

4. **Ejecución de comandos hablados**  
   Dependiendo del verbo inicial (por ejemplo, “eliminar uno”), el sistema actúa sobre los datos del array:
   ```js
   var operacion = reconocido.split(" ")[0];
   switch(operacion){
     case "eliminar":
       let numero = reconocido.split(" ")[1];
       if(numero === "uno") clientes.splice(1,1);
       pintaTabla();
       break;
   }
   ```
   Esto demuestra el **uso práctico del reconocimiento de voz como controlador lógico** dentro de una interfaz web.

---

### Ejemplo de uso paso a paso  
1. El usuario pulsa el botón 🎙️ **“Escuchar”**.  
2. Dice:  
   > “Eliminar uno”  
3. La aplicación reconoce el comando, lo muestra en pantalla y **responde con voz** repitiendo la orden.  
4. El registro correspondiente se elimina de la tabla automáticamente.

Este ejemplo demuestra cómo el sistema **procesa lenguaje natural**, **ejecuta acciones concretas** y **responde mediante voz**, creando una interacción similar a hablar con un asistente.

### Conceptos vistos en clase aplicados
- **Eventos asincrónicos (`onresult`)**.  
- **Objetos del API Web Speech (`SpeechRecognition`, `SpeechSynthesis`)**.  
- **Manipulación del DOM** para actualizar tablas dinámicamente.  
- **Interacción multimodal**: entrada por voz, salida visual y respuesta hablada.

---

Este ejercicio me ha permitido comprender cómo **combinar el reconocimiento y la síntesis de voz** para crear interfaces web más naturales y humanas.  
He aprendido a conectar las APIs del navegador con elementos dinámicos del DOM, a manejar eventos asincrónicos y a implementar **comandos hablados funcionales**.  

Además, veo cómo estos conceptos se pueden aplicar a **futuros proyectos interactivos**, como asistentes virtuales, aplicaciones educativas o sistemas de información en tiempo real.  
En definitiva, el proyecto demuestra cómo la voz puede ser una **forma eficiente, accesible y divertida de interactuar** con la web.
