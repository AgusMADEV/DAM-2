# Respuesta - Actividad EVAL

## 📝 Descripción de la Solución

He implementado un sistema completo de gestión de consultas SQL para blog que cumple con todos los requisitos especificados en el enunciado.

## ✅ Requisitos Cumplidos

### 1. Carga del Esquema ✓
- El programa carga automáticamente `blog.sql`
- Función `cargar_schema_sql()` maneja la lectura del archivo
- Incluye validación de existencia y manejo de errores
- Trunca contenido si excede 200,000 caracteres

### 2. Interacción con el Usuario ✓
- El programa solicita una pregunta mediante `input()`
- Valida que la pregunta no esté vacía
- Muestra feedback claro al usuario

### 3. Construcción del Prompt ✓
- Función `construir_prompt_completo()` integra:
  - Instrucciones claras para el modelo
  - Esquema completo de la base de datos
  - Pregunta del usuario
  - Formato de respuesta esperado

### 4. Ejecución del Modelo ✓
- Función `ejecutar_modelo_ollama()` realiza:
  - Llamada a Ollama usando `subprocess.run()`
  - Construcción del payload JSON
  - Procesamiento de respuesta JSONL línea por línea
  - Timeout de 120 segundos
  - Manejo completo de errores

### 5. Procesamiento y Presentación ✓
- Función `mostrar_respuesta()` presenta resultados formateados
- Banner de inicio profesional
- Feedback de progreso en los 5 pasos
- Formato estructurado y claro

## 🔒 Restricciones Respetadas

### ❌ Sin Librerías Externas
- **NO** se usa `requests`
- **NO** se usa `ollama-python`
- **NO** se usan librerías de terceros

### ✅ Solo Biblioteca Estándar
- `subprocess` - Para ejecutar comandos del sistema
- `json` - Para trabajar con JSON
- `os` - Para operaciones de archivos

### ✅ Conceptos de Clase
Todos los conceptos utilizados han sido vistos en los ejercicios 001-005:
- Ejecución de comandos con `subprocess`
- Construcción de payloads JSON
- Procesamiento de respuestas JSONL
- Lectura de archivos
- Manejo de excepciones
- Funciones y docstrings

## 🎯 Funcionalidades Implementadas

### Funciones Principales

#### 1. `cargar_schema_sql(path)`
```python
def cargar_schema_sql(path):
    """Carga el esquema SQL desde el archivo"""
```
- Verifica existencia del archivo
- Lee el contenido completo
- Maneja encodings problemáticos
- Trunca si es necesario

#### 2. `construir_prompt_completo(schema_sql, pregunta_usuario)`
```python
def construir_prompt_completo(schema_sql, pregunta_usuario):
    """Construye el prompt con esquema y pregunta"""
```
- Añade instrucciones al modelo
- Integra el esquema SQL
- Formatea la pregunta del usuario
- Especifica formato de respuesta

#### 3. `ejecutar_modelo_ollama(prompt)`
```python
def ejecutar_modelo_ollama(prompt):
    """Ejecuta llamada a Ollama y procesa respuesta"""
```
- Construye payload JSON
- Ejecuta curl con subprocess
- Parsea respuesta JSONL
- Concatena fragmentos de respuesta
- Maneja timeouts y errores

#### 4. `mostrar_respuesta(respuesta)`
```python
def mostrar_respuesta(respuesta):
    """Presenta la respuesta de forma estructurada"""
```
- Formato visual atractivo
- Separadores claros
- Fácil de leer

#### 5. `main()`
```python
def main():
    """Función principal - Orquesta los 5 pasos"""
```
- Paso 1: Carga esquema
- Paso 2: Solicita pregunta
- Paso 3: Construye prompt
- Paso 4: Ejecuta modelo
- Paso 5: Presenta respuesta

## 🧪 Ejemplos de Uso

### Ejemplo 1: Últimos artículos
```
Pregunta: ¿Cuáles son los últimos 5 artículos publicados?

Respuesta esperada:
- Consulta SQL con ORDER BY fecha DESC LIMIT 5
- Explicación de la consulta
```

### Ejemplo 2: Autor con más entradas
```
Pregunta: ¿Quién ha escrito más entradas?

Respuesta esperada:
- Consulta SQL con GROUP BY y COUNT
- JOIN entre entradas y usuarios
- ORDER BY count DESC LIMIT 1
```

### Ejemplo 3: Estructura de tablas
```
Pregunta: ¿Qué campos tiene la tabla usuarios?

Respuesta esperada:
- Lista de campos: Identificador, usuario, contrasena
- Tipos de datos de cada campo
- Restricciones (PRIMARY KEY, etc.)
```

## 🏗️ Arquitectura del Programa

```
consulta_blog.py
    |
    ├── main()
    |    |
    |    ├── [1] cargar_schema_sql()
    |    |    └── Lectura de blog.sql
    |    |
    |    ├── [2] input() - Pregunta del usuario
    |    |
    |    ├── [3] construir_prompt_completo()
    |    |    ├── Instrucciones al modelo
    |    |    ├── Esquema SQL
    |    |    └── Pregunta del usuario
    |    |
    |    ├── [4] ejecutar_modelo_ollama()
    |    |    ├── subprocess.run() + curl
    |    |    ├── Payload JSON
    |    |    └── Parseo JSONL
    |    |
    |    └── [5] mostrar_respuesta()
    |         └── Formato estructurado
    |
    └── Helpers
         ├── mostrar_banner()
         └── Manejo de errores
```

## 📊 Flujo de Datos

```
blog.sql → cargar_schema_sql()
                ↓
         [Esquema en memoria]
                ↓
    construir_prompt_completo() ← [Pregunta usuario]
                ↓
         [Prompt completo]
                ↓
    ejecutar_modelo_ollama()
                ↓
      [Llamada API Ollama]
                ↓
       [Respuesta JSONL]
                ↓
      [Procesamiento JSON]
                ↓
         mostrar_respuesta()
                ↓
       [Salida formateada]
```

## 💻 Detalles Técnicos

### API de Ollama
- **Endpoint**: `http://localhost:11434/api/generate`
- **Método**: POST
- **Formato**: JSON
- **Respuesta**: JSONL (JSON Lines)

### Payload Enviado
```json
{
  "model": "qwen2.5:7b-instruct-q4_0",
  "prompt": "[prompt construido]",
  "stream": true
}
```

### Procesamiento JSONL
```python
for line in lines:
    obj = json.loads(line)
    if "response" in obj and obj["response"] is not None:
        response += obj["response"]
```

## 🎨 Características Adicionales

1. **Banner de inicio** - Presentación profesional
2. **Feedback de progreso** - Usuario informado en cada paso
3. **Manejo robusto de errores** - Múltiples try/except
4. **Timeout configurable** - Evita esperas infinitas
5. **Documentación completa** - Docstrings en todas las funciones
6. **Código limpio** - PEP 8, nombres descriptivos
7. **Constantes configurables** - Fácil personalización

## 📈 Mejoras sobre el Ejercicio Base

El programa mejora respecto a `005-cargo blog.py`:

1. ✅ Mejor estructura con más funciones modulares
2. ✅ Banner y presentación profesional
3. ✅ Feedback de progreso paso a paso
4. ✅ Manejo de errores más robusto
5. ✅ Documentación exhaustiva
6. ✅ Funciones con docstrings
7. ✅ Formato de salida mejorado
8. ✅ Instrucciones más claras al modelo

## ⚠️ Consideraciones

### Prerequisitos
- Ollama debe estar instalado y ejecutándose
- Modelo `qwen2.5:7b-instruct-q4_0` debe estar descargado
- Python 3.x instalado
- Conexión a localhost:11434 disponible

### Limitaciones
- Requiere conexión local a Ollama
- Timeout fijo de 120 segundos
- Esquemas muy grandes son truncados
- No ejecuta las consultas SQL (solo las genera)

## 🎓 Conceptos Demostrados

1. **Programación Multiproceso**: Uso de `subprocess` para ejecutar procesos externos
2. **Integración con APIs**: Llamadas HTTP usando curl
3. **Procesamiento de JSON**: Construcción y parseo de datos JSON
4. **Manejo de Archivos**: Lectura y validación de archivos
5. **Manejo de Errores**: Try/except, timeouts, validaciones
6. **Estructuración de Código**: Funciones modulares, separación de responsabilidades
7. **Documentación**: Docstrings, comentarios, README completo

## ✨ Conclusión

Este programa cumple completamente con todos los requisitos del enunciado:
- ✅ Carga el esquema SQL
- ✅ Interactúa con el usuario
- ✅ Construye prompts dinámicos
- ✅ Ejecuta el modelo de lenguaje
- ✅ Presenta resultados estructurados
- ✅ Sin librerías externas
- ✅ Solo conceptos vistos en clase

El código es robusto, bien documentado y listo para usar en un entorno de producción educativa.
