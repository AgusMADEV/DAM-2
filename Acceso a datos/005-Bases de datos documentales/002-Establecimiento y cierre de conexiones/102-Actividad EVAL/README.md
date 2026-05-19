# Actividad de Evaluación: Identificación de Imagen con API

## Descripción
En esta actividad, aprenderás a utilizar una API para identificar qué hay en una imagen de perro. Esta práctica te ayudará a entender cómo trabajar con imágenes y APIs en Python.

## Contexto
Imagina que eres un aficionado al deporte y disfrutas mucho jugando videojuegos. Además de eso, te gusta viajar y dibujar. Hoy, mientras estás en el parque jugando fútbol, ves una imagen de perro y te gustaría saber qué es.

## Objetivos
- Comprender cómo abrir y leer archivos de imagen en Python
- Aprender a codificar imágenes en formato base64
- Practicar el envío de solicitudes HTTP POST a una API
- Procesar y mostrar las respuestas de una API

## Pasos a seguir

### 1. Abrir la imagen
Debes abrir la imagen del perro que quieres identificar usando la función `open()` en modo lectura binaria.

### 2. Codificar la imagen en base64
Codifica la imagen en formato base64 para poder enviarla por una solicitud HTTP. Utiliza:
- `base64.b64encode()` para codificar
- `.decode()` para convertir a string

### 3. Enviar la solicitud
Utiliza la API de Ollama para enviar la imagen y recibir una respuesta que indique qué hay en la imagen:
- **URL**: `http://localhost:11434/api/generate`
- **Método**: POST
- **Datos JSON**:
  - `model`: "llava"
  - `prompt`: "what is in this image?"
  - `images`: [imagen codificada]
  - `stream`: False

### 4. Imprimir la respuesta
Finalmente, imprime la respuesta recibida accediendo a `r.json()["response"]`.

## Restricciones
- ❌ No puedes usar librerías externas o estructuras no vistas hasta ahora
- ✅ Solo puedes utilizar los conceptos y funciones permitidos en el material de clase
- ✅ Debes usar: `base64`, `requests`, `open()`, `read()`, `b64encode()`, `decode()`

## Archivos necesarios
- `actividad-identificar-imagen.py` - Archivo principal donde escribirás tu código
- `perro.jpg` - Imagen de perro a analizar (debe estar en el mismo directorio)

## Prerrequisitos
Asegúrate de tener instalado y ejecutando:
```bash
ollama pull llava
```

## Entrega
Completa el archivo `actividad-identificar-imagen.py` siguiendo las instrucciones y TODO's indicados.

## Evaluación
Se evaluará:
- Correcta apertura y lectura del archivo de imagen
- Correcta codificación en base64
- Correcta configuración de la solicitud POST
- Correcta extracción e impresión de la respuesta
- Uso únicamente de conceptos vistos en clase

¡Buena suerte! 🚀
