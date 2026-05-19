# v0.2 - Sistema de completar tareas + estado visual

## Nuevas características

✅ **Función completar tarea**
- Nueva función `completar(indice)` que marca tareas como completadas
- Comando de voz: "completar [número]" o "terminar [número]"

✅ **Columna de estado en tabla**
- Nueva columna que muestra el estado de cada tarea
- ✅ para tareas completadas (verde)
- ⏳ para tareas pendientes (naranja)

✅ **Estilos visuales mejorados**
- `.completada` - Tachado y opacidad reducida
- `.estado-completada` - Color verde para completadas
- `.estado-pendiente` - Color naranja para pendientes

## Cambios técnicos

- Añadido atributo `completada: false` a objetos de tarea
- Actualizado `mostrarTabla()` para incluir columna de estado
- Actualizado procesador de comandos de voz con "completar"
- Documentación actualizada en la interfaz
