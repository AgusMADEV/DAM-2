# Ejemplos de Preguntas para Probar el Sistema

## 📚 Guía de Pruebas

Este archivo contiene ejemplos de preguntas que puedes usar para probar el sistema `consulta_blog.py`.

---

## 🎯 Preguntas Básicas sobre Estructura

### 1. Información sobre tablas
```
¿Qué tablas tiene la base de datos?
```

### 2. Estructura de tabla entradas
```
¿Qué campos tiene la tabla entradas?
```

### 3. Estructura de tabla usuarios
```
¿Qué campos tiene la tabla usuarios?
```

### 4. Tipos de datos
```
¿Qué tipo de dato es el campo contenido de la tabla entradas?
```

---

## 📊 Consultas SQL Simples

### 5. Todos los registros
```
Dame una consulta SQL para obtener todas las entradas
```

### 6. Campos específicos
```
Cómo selecciono solo el título y la fecha de las entradas
```

### 7. Ordenamiento
```
Dame los títulos ordenados por fecha descendente
```

### 8. Filtrado por fecha
```
¿Cómo obtengo las entradas de este año?
```

---

## 🔍 Consultas Avanzadas

### 9. Últimos N registros
```
¿Cuáles son los últimos 5 artículos publicados?
```

### 10. Búsqueda de texto
```
Cómo busco entradas que contengan una palabra específica en el título
```

### 11. Conteo de registros
```
¿Cuántas entradas hay en total?
```

### 12. Rango de fechas
```
Dame las entradas entre dos fechas específicas
```

---

## 🔗 Consultas con JOINs (si hay relaciones)

### 13. Relación entre tablas
```
¿Hay alguna relación entre las tablas entradas y usuarios?
```

### 14. Si existe campo usuario_id en entradas
```
¿Quién ha escrito más entradas?
```

### 15. Entradas por autor
```
Dame todas las entradas de un usuario específico
```

---

## 📈 Consultas Analíticas

### 16. Agrupamiento
```
Muéstrame cuántas entradas hay por año
```

### 17. Estadísticas
```
¿Cuál es la entrada más reciente?
```

### 18. Ordenamiento complejo
```
Dame los 10 artículos más antiguos
```

---

## 🛠️ Consultas de Mantenimiento

### 19. Estructura completa
```
Muéstrame la estructura completa de la base de datos
```

### 20. Claves primarias
```
¿Qué campos son claves primarias?
```

### 21. Índices
```
¿Qué índices tiene la base de datos?
```

---

## 💡 Preguntas Creativas

### 22. Inserción de datos
```
¿Cómo inserto una nueva entrada en el blog?
```

### 23. Actualización
```
Dame un ejemplo de cómo actualizar el título de una entrada
```

### 24. Eliminación
```
¿Cómo borro una entrada específica?
```

### 25. Validaciones
```
¿Qué validaciones debería tener el campo de email si existiera?
```

---

## 🎓 Preguntas Educativas

### 26. Buenas prácticas
```
¿Qué buenas prácticas de SQL se aplican en este esquema?
```

### 27. Optimización
```
¿Cómo podría optimizar las consultas en esta base de datos?
```

### 28. Seguridad
```
¿Por qué no es buena idea guardar contraseñas en texto plano?
```

---

## 🧪 Cómo Usar Este Archivo

1. **Ejecuta el programa**: `python consulta_blog.py`
2. **Copia una pregunta** de este archivo
3. **Pégala** cuando el programa te lo solicite
4. **Analiza la respuesta** del modelo

## 💡 Consejos

- Empieza con preguntas simples (1-8)
- Prueba consultas más complejas (9-18)
- Experimenta con preguntas creativas (22-28)
- Modifica las preguntas para aprender más

## 📝 Notas

- Todas estas preguntas están diseñadas para el esquema `blog.sql`
- El modelo generará consultas SQL válidas basándose en el esquema
- Algunas preguntas sobre relaciones pueden no aplicar si no existen foreign keys
- Puedes hacer preguntas propias siguiendo estos ejemplos como guía

## 🎯 Preguntas Recomendadas para Demostración

Si tienes que demostrar el programa, usa estas 5 preguntas:

1. **Pregunta básica**: "¿Qué tablas tiene la base de datos?"
2. **Consulta simple**: "Dame todas las entradas ordenadas por fecha"
3. **Consulta con LIMIT**: "¿Cuáles son los últimos 5 artículos publicados?"
4. **Consulta analítica**: "¿Cuántas entradas hay en total?"
5. **Pregunta de estructura**: "¿Qué campos tiene la tabla usuarios?"

---

## ✨ Resultado Esperado

Para cada pregunta, el modelo debería devolver:

1. ✅ **Explicación clara** de lo que hace la consulta
2. ✅ **Código SQL** en un bloque ```sql```
3. ✅ **Descripción paso a paso** de la consulta
4. ✅ **Consideraciones** o buenas prácticas si aplica

---

**¡Feliz experimentación! 🚀**
