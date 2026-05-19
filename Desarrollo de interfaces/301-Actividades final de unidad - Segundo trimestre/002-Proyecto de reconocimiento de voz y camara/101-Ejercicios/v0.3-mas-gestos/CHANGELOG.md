# v0.3 - Más gestos de mano

## Nuevas características

✅ **Dos nuevos gestos**
- 👍 **Pulgar arriba**: Completa la primera tarea pendiente
- 🖐️ **Mano abierta** (5 dedos): Muestra resumen de tareas por voz

✅ **Función mostrarResumen()**
- Cuenta total de tareas, completadas y pendientes
- Lee el resumen por voz

✅ **Mejoras en detección de gestos**
- Algoritmo mejorado para detectar dedos extendidos
- Función `dedoExtendido()` para mayor precisión
- Detección de pulgar extendido (eje X)

✅ **Feedback mejorado**
- Nuevo elemento `#statusGestos` para feedback en tiempo real
- Mensajes específicos para cada gesto detectado

✅ **Array de tareas aleatorias**
- Lista predefinida de tareas de ejemplo
- Gesto "dos dedos" ahora añade tareas aleatorias

## Cambios técnicos

- Mejorado `detectarGesto()` con 4 gestos diferentes
- Añadida función `mostrarResumen()` con estadísticas
- Actualizado `ejecutarGesto()` para manejar 4 acciones
- Array `tareasAleatorias` con tareas de ejemplo
- Status de gestos independiente del status de voz
