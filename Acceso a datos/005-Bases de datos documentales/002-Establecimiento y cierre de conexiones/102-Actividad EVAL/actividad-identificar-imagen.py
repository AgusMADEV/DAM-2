"""
ACTIVIDAD DE EVALUACIÓN: Identificación de Imagen con API

Descripción:
En este ejercicio, vamos a utilizar una API para identificar qué hay en una imagen de perro.
Esta práctica nos ayudará a entender cómo trabajar con imágenes y APIs en Python.

Contexto:
Imagina que eres un aficionado al deporte y disfrutas mucho jugando videojuegos.
Además de eso, te gusta viajar y dibujar. Hoy, mientras estás en el parque jugando fútbol,
ves una imagen de perro y te gustaría saber qué es.
"""

# Importamos las librerías necesarias
import base64, requests

# Abrimos el archivo perro.jpg en modo lectura binaria y lo codificamos en base64
with open("perro.jpg","rb") as f:
    img = base64.b64encode(f.read()).decode()

# Enviamos una solicitud POST a la API de Ollama
r = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model":"llava",
        "prompt":"what is in this image?",
        "images":[img],
        "stream": False
    }
)

# Imprimimos la respuesta recibida de la API
print(r.json()["response"])

