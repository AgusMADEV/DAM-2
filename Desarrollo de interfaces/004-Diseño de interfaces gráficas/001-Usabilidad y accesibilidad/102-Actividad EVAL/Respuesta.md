Este proyecto aplica **principios de accesibilidad y usabilidad web** para mejorar la experiencia de todo tipo de usuarios, especialmente quienes tienen **dificultades visuales** o navegan desde **dispositivos y tamaños de pantalla diversos**.  
Se centra en: (a) **control del tamaño tipográfico**, (b) **layout adaptable a anchuras reales de uso**, (c) **convenciones de localización** (logo arriba-izquierda, navegación principal accesible), (d) **formularios simples y con validación inmediata**, y (e) **priorización del contenido “above the fold”** para que lo esencial sea visible sin hacer scroll.

---

### Definiciones clave  
- **Accesibilidad (a11y):** diseño que permite a personas con diferentes capacidades **percibir, entender, navegar e interactuar** con la web.  
- **Usabilidad:** grado en que una interfaz es **fácil de usar, eficiente y satisfactoria** para el usuario.  
- **Above the fold:** parte visible **sin scroll** al cargar la página. Es crítico ubicar ahí los elementos clave (mensaje principal y CTA).  
- **Alto contraste / tamaño de fuente:** mecanismos que facilitan la lectura y distinguen elementos de la UI.  
- **Responsive design:** CSS y estructura que **se adaptan** a distintas anchuras de pantalla.

### Terminología técnica aplicada al temario  
- **Variables CSS** (`--font-size-base`, `--primary-color`) para tematizar y ajustar tipografía y contraste.  
- **Media queries** para **layout responsive**.  
- **`position: sticky`** para mantener el header accesible.  
- **Validación en tiempo real** en formularios (clases `valid`/`invalid`, mensajes dinámicos).  
- **Medición de anchura** con `localStorage` como analítica didáctica para orientar decisiones de diseño.

### Funcionamiento paso a paso (según el código)

1) **Registrar anchura de pantalla (analítica didáctica):**  
   ```html
   <script>
     (function () {
       try {
         const w = window.innerWidth || document.documentElement.clientWidth;
         localStorage.setItem("anchura_pantalla", String(w));
       } catch (e) {}
     })();
   </script>
   ```
   - Guarda la anchura en `localStorage` → permite conocer las resoluciones más usadas y **ajustar el diseño** en futuras iteraciones.

2) **Control de tipografía y contraste (accesibilidad):**  
   - Variables CSS y clase `high-contrast`:
     ```css
     :root { --font-size-base: 16px; }
     body { font-size: var(--font-size-base); }
     body.high-contrast { --bg-color: #ffff00; --text-color: #000; }
     ```
   - Controles de UI:
     ```js
     let currentFontSize = 16;
     function increaseFontSize(){ if(currentFontSize<24){ currentFontSize+=2; document.documentElement.style.setProperty('--font-size-base', currentFontSize+'px'); } }
     function decreaseFontSize(){ if(currentFontSize>12){ currentFontSize-=2; document.documentElement.style.setProperty('--font-size-base', currentFontSize+'px'); } }
     function toggleContrast(){ document.body.classList.toggle('high-contrast'); }
     function resetAccessibility(){ currentFontSize=16; document.documentElement.style.setProperty('--font-size-base','16px'); document.body.classList.remove('high-contrast'); }
     ```
   - **Para qué sirve:** permitir a cualquier usuario **ajustar legibilidad** y **mejorar visibilidad**.

3) **Estructura y localización de elementos clave:**  
   - **Logo arriba a la izquierda** y **navegación superior**:
     ```html
     <header class="header-content"> <div class="logo">🎓 Academia Digital</div> <nav>…</nav> </header>
     ```
   - **Header sticky** para acceso constante a navegación:
     ```css
     header { position: sticky; top: 0; z-index: 1000; }
     ```
   - **Hero “above the fold”** con título, texto y CTA visibles:
     ```html
     <section class="hero"> <h1>Aprende a Tu Ritmo…</h1> <button class="cta-button">Comienza Gratis</button> </section>
     ```

4) **Buscador prominente y resultados en tiempo real (usabilidad):**  
   ```js
   function performSearch(){
     const query = document.getElementById('searchInput').value.toLowerCase();
     // … filtra array cursos y muestra resultados en #searchResults
   }
   ```
   - **Objetivo:** ofrecer **feedback inmediato** y reducir fricción en la búsqueda.

5) **Formulario simple y con validación en tiempo real:**  
   - Mensajes de validación y estados visuales:
     ```js
     function validateEmail(input){
       const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
       // añade clases .valid / .invalid y mensajes .success / .error
     }
     function handleSubmit(e){ e.preventDefault(); /* alerta y reseteo limpio */ }
     ```
   - **Objetivo:** **minimizar errores** y **agilizar el registro**, evitando formularios largos.

### Ejemplos reales (del propio código)

- **Botones de accesibilidad (A+/A-/Alto Contraste/Resetear)** en `.accessibility-tools`.  
- **Medición de anchura** con `localStorage` para orientar el **diseño responsive**.  
- **CTA visible** sin scroll en `.hero` para mejorar conversión.  
- **Validación en vivo** (`validateName`, `validateEmail`) con feedback visual inmediato.

---

### Cómo se aplica en la página
- Un usuario con baja visión puede pulsar **A+** (o activar **alto contraste**) y **leer cómodamente** sin plugins externos.  
- En móviles, el **layout se reordena** con media queries (`@media (max-width: 768px)`) para mantener la navegabilidad y evitar zoom manual.  
- Lo esencial (mensaje y CTA) está **“above the fold”** en la sección `.hero`.  
- El **buscador** da **resultados en tiempo real**, reduciendo clics y tiempo.  
- El **formulario** es **corto**, con **validación inmediata** y **mensajes claros**.

### Fragmentos que ejemplifican las mejoras
- **Accesibilidad tipográfica y contraste:**
  ```js
  increaseFontSize(); decreaseFontSize(); toggleContrast(); resetAccessibility();
  ```
- **Priorizar “above the fold”:**
  ```html
  <section class="hero"> … <button class="cta-button">Comienza Gratis</button> </section>
  ```
- **Validación inmediata:**
  ```js
  function validateName(input){ /* añade .valid / .invalid y mensaje */ }
  function validateEmail(input){ /* regex + feedback */ }
  ```

---

**Puntos clave:**  
- Accesibilidad práctica: **tamaño de letra ajustable**, **alto contraste**, **estructura clara** y **formularios simples**.  
- Usabilidad aplicada: **contenido crítico above the fold**, **búsqueda con feedback inmediato**, **navegación persistente**.

**Conexión con la unidad:**  
Este proyecto integra **buenas prácticas de diseño centrado en el usuario**, **responsive design**, **control visual accesible** y **validación usable**, todos **contenidos nucleares** de la unidad de **Accesibilidad y Usabilidad en Desarrollo de Interfaces**.  
El resultado es una base sólida que se puede **reutilizar y extender** en otros proyectos (p. ej., paneles de cursos, landings educativas o intranets) manteniendo **consistencia, legibilidad y eficiencia**.
