# Actividad EVAL - Sistema de Consultas SQL para Blog

## 📋 Descripción

Este programa implementa un sistema de gestión de consultas SQL dinámicas para una base de datos de blog, utilizando el modelo de lenguaje Ollama para generar respuestas inteligentes basadas en el esquema de la base de datos.

## 🎯 Objetivos Cumplidos

1. **Carga del Esquema**: El programa carga automáticamente el esquema de la base de datos desde `blog.sql`
2. **Interacción con el Usuario**: Solicita preguntas en lenguaje natural sobre el blog
3. **Construcción del Prompt**: Integra el esquema SQL con la pregunta del usuario
4. **Ejecución del Modelo**: Realiza llamadas a Ollama usando `subprocess` y `curl`
5. **Presentación de Resultados**: Muestra respuestas estructuradas y claras

## 📁 Archivos

- `consulta_blog.py` - Programa principal
- `blog.sql` - Esquema de la base de datos (tablas `entradas` y `usuarios`)
- `README.md` - Este archivo de documentación

## 🔧 Requisitos

- Python 3.x (sin librerías externas)
- Ollama instalado y ejecutándose localmente
- Modelo `qwen2.5:7b-instruct-q4_0` descargado en Ollama
- Sistema operativo: Windows (PowerShell)

## 🚀 Uso

### Ejecutar el programa

```powershell
python consulta_blog.py
```

### Ejemplos de preguntas

- "¿Cuáles son los últimos 5 artículos publicados?"
- "¿Quién ha escrito más entradas?"
- "Dame una consulta SQL para obtener todas las entradas de este año"
- "¿Qué campos tiene la tabla usuarios?"
- "Cómo puedo obtener los títulos ordenados por fecha descendente?"

## 📖 Estructura del Código

### Funciones Principales

1. **`cargar_schema_sql(path)`**
   - Carga el contenido del archivo SQL
   - Maneja errores de lectura
   - Trunca el contenido si es demasiado largo

2. **`construir_prompt_completo(schema_sql, pregunta_usuario)`**
   - Construye el prompt con instrucciones claras
   - Integra el esquema de la base de datos
   - Añade la pregunta del usuario

3. **`ejecutar_modelo_ollama(prompt)`**
   - Ejecuta `curl` usando `subprocess.run()`
   - Envía el prompt al modelo Ollama
   - Procesa la respuesta en formato JSONL
   - Maneja timeouts y errores

4. **`mostrar_respuesta(respuesta)`**
   - Formatea y presenta la respuesta
   - Muestra la información de forma estructurada

5. **`main()`**
   - Orquesta todo el flujo del programa
   - Sigue los 5 pasos del enunciado

## 🔍 Conceptos Aplicados

### Conceptos de Clase Utilizados

- **`subprocess`**: Para ejecutar comandos del sistema (curl)
- **`json`**: Para construir payloads y parsear respuestas JSONL
- **`os`**: Para verificar existencia de archivos
- Manejo de archivos con `open()`, `read()`
- Manejo de excepciones con `try/except`
- Funciones con docstrings
- Variables de configuración (constantes en mayúsculas)

### Sin Librerías Externas

El código NO utiliza librerías externas como:
- ❌ `requests` (se usa `curl` con subprocess)
- ❌ `ollama-python` (se usa la API REST directamente)
- ❌ `pandas`, `numpy`, etc.

Solo se usan módulos de la biblioteca estándar de Python.

## 🛠️ Esquema de la Base de Datos

### Tabla: `entradas`
- `Identificador` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `titulo` (VARCHAR 255)
- `fecha` (DATE)
- `contenido` (TEXT)

### Tabla: `usuarios`
- `Identificador` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `usuario` (VARCHAR 255)
- `contrasena` (VARCHAR 255)

## 📊 Flujo de Ejecución

```
1. INICIO
   ↓
2. Cargar blog.sql
   ↓
3. Solicitar pregunta al usuario
   ↓
4. Construir prompt (esquema + pregunta)
   ↓
5. Llamar a Ollama vía curl
   ↓
6. Procesar respuesta JSONL
   ↓
7. Mostrar resultado formateado
   ↓
8. FIN
```

## ⚙️ Configuración

Las constantes del programa se pueden ajustar al inicio de `consulta_blog.py`:

```python
SCHEMA_PATH = "blog.sql"              # Ruta al archivo SQL
MAX_SCHEMA_CHARS = 200_000            # Límite de caracteres del esquema
MODELO_OLLAMA = "qwen2.5:7b-instruct-q4_0"  # Modelo a utilizar
OLLAMA_URL = "http://localhost:11434/api/generate"  # URL de la API
```

## 🐛 Manejo de Errores

El programa incluye manejo robusto de errores:

- Archivo SQL no encontrado
- Errores de lectura de archivos
- Timeout en la respuesta del modelo
- Errores de conexión con Ollama
- Interrupciones del usuario (Ctrl+C)
- Respuestas malformadas

## 💡 Ejemplos de Salida

### Ejemplo 1: Consulta de últimos artículos

```
Introduce tu pregunta sobre el blog: ¿Cuáles son los últimos 5 artículos?

======================================================================
RESPUESTA DEL SISTEMA:
======================================================================

Para obtener los últimos 5 artículos del blog, puedes usar la siguiente consulta SQL:

```sql
SELECT titulo, fecha, contenido
FROM entradas
ORDER BY fecha DESC
LIMIT 5;
```

Esta consulta:
1. Selecciona los campos titulo, fecha y contenido de la tabla entradas
2. Ordena los resultados por fecha en orden descendente (más recientes primero)
3. Limita el resultado a 5 registros

======================================================================
```

## 📝 Notas Importantes

- El programa requiere que Ollama esté ejecutándose en `localhost:11434`
- El modelo debe estar previamente descargado (`ollama pull qwen2.5:7b-instruct-q4_0`)
- Las respuestas pueden tardar varios segundos dependiendo de la complejidad de la pregunta
- El programa trunca esquemas muy grandes para evitar exceder el contexto del modelo

## 👨‍💻 Autor

Estudiante de DAM-2  
Programación de Servicios y Procesos  
Fecha: 10 de noviembre de 2025

## 📚 Referencias

- Ejercicios 001-005 de la carpeta `101-Ejercicios`
- Documentación de Ollama API
- Material del curso de Programación de Servicios y Procesos
