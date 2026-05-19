# 🎯 Proyecto de Interfaces Naturales - Guía Rápida

## 🚀 Inicio Rápido

1. Abre el archivo `proyecto-interfaces-naturales.html` en tu navegador (Chrome/Edge recomendado)
2. Concede permisos de cámara y micrófono cuando se soliciten
3. ¡Empieza a usar la aplicación con voz o gestos!

## � Archivos del Proyecto

### Aplicaciones Completas
- **`proyecto-interfaces-naturales.html`** - 🌟 **Aplicación principal completa**
  - Integra voz + gestos + síntesis
  - Sistema completo de gestión de tareas
  - Interfaz profesional con diseño moderno

### Demos Simplificadas (para aprender)
- **`demo-voz-simplificada.html`** - 🎤 **Solo reconocimiento de voz**
  - Código más simple y comentado
  - Ideal para entender la Web Speech API
  - Gestión básica de tareas por voz

- **`demo-gestos-simplificada.html`** - 👋 **Solo reconocimiento de gestos**
  - Código enfocado solo en MediaPipe
  - Contador de gestos detectados
  - Visualización clara de landmarks

### Documentación
- **`ejercicio.md`** - 📚 Documentación técnica completa
- **`README.md`** - 📖 Esta guía rápida

## 📢 Comandos de Voz

| Comando | Ejemplo | Acción |
|---------|---------|---------|
| **agregar [tarea]** | "agregar estudiar matemáticas" | Añade nueva tarea |
| **eliminar [número]** | "eliminar dos" | Elimina tarea específica |
| **completar [número]** | "completar uno" | Marca tarea como completada |
| **leer tareas** | "leer tareas" | Lee todas las tareas |
| **limpiar todo** | "limpiar todo" | Elimina todas las tareas |

## 👋 Gestos con las Manos

| Gesto | Descripción | Acción |
|-------|-------------|---------|
| ✌️ | Dos dedos arriba | Añade tarea aleatoria |
| 👍 | Pulgar arriba | Completa primera tarea pendiente |
| ✊ | Puño cerrado | Elimina última tarea |
| 🖐️ | Mano abierta | Lee tareas por voz |

## 💡 Consejos de Uso

### Para Voz:
- Habla claro y con volumen normal
- Pulsa el botón "Escuchar" antes de hablar
- Espera a que termine de procesar el comando

### Para Gestos:
- Mantén tu mano visible en el centro de la cámara
- Haz el gesto claramente durante 1-2 segundos
- Espera 2 segundos entre gestos (cooldown)
- Asegúrate de tener buena iluminación

## 📚 Rutas de Aprendizaje Sugeridas

### Si eres principiante:
1. Empieza con `demo-voz-simplificada.html`
   - Entiende cómo funciona el reconocimiento de voz
   - Prueba los comandos básicos
   - Lee el código comentado

2. Continúa con `demo-gestos-simplificada.html`
   - Aprende sobre MediaPipe Hands
   - Observa cómo se detectan los gestos
   - Experimenta con los contadores

3. Finalmente usa `proyecto-interfaces-naturales.html`
   - Observa cómo se integran ambas tecnologías
   - Analiza la arquitectura del código
   - Personaliza según tus necesidades

### Si tienes experiencia:
- Ve directamente a `proyecto-interfaces-naturales.html`
- Revisa el código fuente para entender la arquitectura
- Consulta `ejercicio.md` para detalles técnicos

## ⚠️ Solución de Problemas

**La cámara no se activa:**
- Verifica los permisos del navegador
- Asegúrate de que ninguna otra aplicación esté usando la cámara
- Prueba en modo incógnito si hay problemas de permisos

**El micrófono no funciona:**
- Comprueba los permisos del navegador
- Verifica que el micrófono esté conectado y configurado
- Revisa el nivel de volumen del micrófono

**Los gestos no se detectan:**
- Mejora la iluminación de la habitación
- Acércate o aléjate de la cámara (distancia ideal: 30-50cm)
- Asegúrate de que tu mano está completamente visible
- Fondo uniforme ayuda a la detección

**La voz no se reconoce:**
- Chrome y Edge tienen mejor soporte que Firefox
- Safari también funciona pero puede tener limitaciones
- Habla más despacio y claro
- Revisa los ajustes de idioma del navegador (debe ser es-ES)

## 🎓 Contexto Académico

Este proyecto fue desarrollado como parte de la asignatura **Desarrollo de Interfaces** del ciclo formativo DAM-2, cumpliendo con los requisitos de crear una aplicación con interfaces naturales que integre:

✅ Reconocimiento de voz (Web Speech API)  
✅ Síntesis de voz (Text-to-Speech)  
✅ Reconocimiento de gestos (MediaPipe Hands)  
✅ Interacción natural con el usuario  
✅ Procesamiento de lenguaje natural básico  
✅ Feedback multimodal  

## 🛠️ Tecnologías Utilizadas

- **HTML5** - Estructura y semántica
- **CSS3** - Diseño y animaciones
- **JavaScript ES6+** - Lógica de aplicación
- **Web Speech API** - Reconocimiento y síntesis de voz
- **MediaPipe Hands** - Detección de manos y gestos
- **Canvas API** - Renderizado de visualizaciones

## 🔗 Recursos Adicionales

- [Web Speech API - MDN](https://developer.mozilla.org/es/docs/Web/API/Web_Speech_API)
- [MediaPipe Hands - Google](https://google.github.io/mediapipe/solutions/hands.html)
- [Canvas API - MDN](https://developer.mozilla.org/es/docs/Web/API/Canvas_API)

---

**¿Necesitas ayuda?** Consulta el archivo `ejercicio.md` para documentación técnica completa.

**¿Tienes una idea para mejorar el proyecto?** ¡Experimenta y personalízalo!
