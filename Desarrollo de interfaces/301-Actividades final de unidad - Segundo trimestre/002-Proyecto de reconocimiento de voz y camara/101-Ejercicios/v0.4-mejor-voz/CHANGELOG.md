# v0.4 - Mejorar síntesis de voz + comando "leer tareas"

## Nuevas características

✅ **Sistema de voces mejorado**
- Función `cargarVoces()` que carga voces disponibles del sistema
- Función `elegirVozEspañola()` que selecciona la mejor voz en español
- Soporte para voces es-ES, es-MX y Spanish
- Configuración de rate, pitch y volume

✅ **Nueva función leerTodasLasTareas()**
- Lee cada tarea con su número y estado (completada/pendiente)
- Maneja el caso de lista vacía
- Integrada con el gesto de mano abierta

✅ **Comando de voz "leer tareas"**
- Nuevo comando: "leer" o "leer tareas"
- Lee todas las tareas en voz alta con detalles

✅ **Feedback de voz mejorado**
- Mensajes más descriptivos al agregar tareas (incluye nombre)
- Mensajes al eliminar tareas (incluye nombre eliminada)
- Mensajes al completar tareas (incluye nombre completada)
- Validación con mensaje de error para índices no válidos
- Cancelación de síntesis anterior antes de hablar

✅ **Actualización de gestos**
- 🖐️ Mano abierta ahora lee todas las tareas (antes mostraba resumen corto)

## Cambios técnicos

- Variable `voices` para almacenar voces disponibles
- Event listener `speechSynthesis.onvoiceschanged` para cargar voces
- `speechSynthesis.cancel()` antes de cada síntesis para evitar solapamientos
- Mejor manejo de casos edge (lista vacía, índices inválidos)
- Mensajes más descriptivos en todas las operaciones CRUD
