# 🚀 Guía de Inicio Rápido

## Abrir el proyecto

1. **Navegador recomendado:** Chrome, Firefox, o Edge (última versión)

2. **Opción A - Doble click:**
   - Abre `index.html` directamente en tu navegador

3. **Opción B - Servidor local (recomendado):**
   ```bash
   # Si tienes Python 3 instalado:
   python -m http.server 8000
   
   # Si tienes Node.js:
   npx http-server -p 8000
   
   # Si estás en el directorio de XAMPP:
   # Ya está servido en http://localhost/DAM-2/...
   ```

## Primeros pasos

1. **Haz click en "🔊 Activar Audio"** (obligatorio por políticas de navegadores)
2. **Haz click en el canvas** para crear tu primera partícula
3. **Observa** cómo rebota y genera sonido al colisionar

## Ejemplos de uso

### Crear una melodía simple
1. Selecciona nota **C4** (Do)
2. Click en el canvas
3. Selecciona **E4** (Mi)
4. Click en el canvas
5. Selecciona **G4** (Sol)
6. Click en el canvas
- **Resultado:** Acorde mayor en Do al colisionar

### Hacer una explosión musical
1. Cambia modo a **"Explosión (5 partículas)"**
2. Click en el centro del canvas
- **Resultado:** 5 partículas con notas aleatorias en patrón radial

### Crear un sistema solar musical
1. Cambia modo a **"Sistema Orbital"**
2. Click en el canvas
- **Resultado:** Sistema con 13 partículas en 3 órbitas

### Experimento: Sin gravedad
1. Crea varias partículas
2. Click en **"🌍 Gravedad: ON"** para desactivar
- **Resultado:** Movimiento caótico sin caída

## Problemas comunes

### No se escucha audio
- ✅ ¿Hiciste click en "Activar Audio"?
- ✅ ¿Está el volumen del navegador activo?
- ✅ ¿Está el "Volumen Principal" por encima de 0%?

### Las partículas no se ven
- ✅ Haz scroll si la ventana es pequeña
- ✅ Verifica que el canvas sea visible (área azul-púrpura)

### Performance baja (FPS < 30)
- ✅ Limpia partículas con "🗑️ Limpiar Todo"
- ✅ Reduce el número de partículas creadas
- ✅ Cierra otras pestañas del navegador

## Tips avanzados

- **Masa alta + velocidad baja** = Movimiento lento y majestuoso
- **Gravedad 0 + modo explosión** = Patrones simétricos permanentes
- **Duración nota larga (1000ms)** = Sonido ambiental continuo
- **Sawtooth + Reverb alto** = Sonido de sintetizador clásico

## Controles de teclado

Actualmente no hay controles de teclado, todo se hace con el mouse.

## ¿Necesitas ayuda?

Consulta el [README.md](../README.md) para documentación completa.

---

**¡Disfruta creando música visual!** 🎵🌌
