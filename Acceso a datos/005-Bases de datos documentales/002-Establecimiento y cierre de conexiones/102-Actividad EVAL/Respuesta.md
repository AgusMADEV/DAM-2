Como estudiante aficionado al deporte, disfruto mucho jugando videojuegos, viajando y dibujando. Hoy, mientras estaba en el parque jugando fútbol con mis amigos, vi una imagen interesante de un perro que alguien había compartido. Me dio curiosidad saber qué tipo de perro era o qué características tenía, así que decidí utilizar mis conocimientos de programación en Python para identificar qué había en esa imagen.

Este ejercicio me permite aplicar lo aprendido en clase sobre el manejo de imágenes y APIs, llevando la teoría a un caso práctico y real de mi día a día.

---

Para resolver este problema, he desarrollado un código estructurado que sigue los pasos necesarios para enviar una imagen a una API de análisis de imágenes:

### Paso 1: Importación de librerías
```python
import base64, requests
```
He importado las librerías `base64` para codificar la imagen y `requests` para realizar solicitudes HTTP, tal como vimos en clase.

### Paso 2: Apertura y codificación de la imagen
```python
with open("perro.jpg","rb") as f:
    img = base64.b64encode(f.read()).decode()
```
Utilizo el gestor de contexto `with` para abrir el archivo `perro.jpg` en modo lectura binaria (`"rb"`). Luego:
- `f.read()` lee los bytes de la imagen
- `base64.b64encode()` codifica esos bytes en formato base64
- `.decode()` convierte el resultado a una cadena de texto que puedo enviar por HTTP

### Paso 3: Envío de solicitud POST a la API
```python
r = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model":"llava",
        "prompt":"what is in this image?",
        "images":[img],
        "stream": False
    }
)
```
Realizo una solicitud POST a la API de Ollama en `localhost:11434/api/generate`, enviando:
- El modelo a utilizar: `"llava"` (especializado en análisis de imágenes)
- El prompt: `"what is in this image?"` para preguntar qué hay en la imagen
- La imagen codificada en base64 dentro de un array `[img]`
- `stream: False` para recibir la respuesta completa de una vez

### Paso 4: Impresión de la respuesta
```python
print(r.json()["response"])
```
Extraigo la respuesta del JSON devuelto por la API accediendo a la clave `"response"` y la imprimo en pantalla.

---

### Ejecución del código
Para ejecutar este programa, debo seguir estos pasos:

1. **Asegurarme de tener Ollama instalado y ejecutándose** con el modelo llava:
   ```bash
   ollama pull llava
   ```

2. **Colocar la imagen** `perro.jpg` en el mismo directorio que el script Python.

3. **Ejecutar el script**:
   ```bash
   python actividad-identificar-imagen.py
   ```

### Resultado esperado
Al ejecutar el código, la API analiza la imagen y devuelve una descripción detallada. Por ejemplo:

```
This is an image of a dog. The dog appears to be a golden retriever, sitting on grass in what looks like a park setting. The dog has a friendly expression and golden-brown fur.
```

La respuesta varía dependiendo del contenido exacto de la imagen, pero siempre proporciona una descripción precisa de lo que la IA visual detecta en la fotografía.

## 4. Cierre y Conclusión - Enlace con la Unidad

Esta actividad me ha permitido consolidar y aplicar varios conceptos fundamentales vistos en clase sobre el **establecimiento y cierre de conexiones** con bases de datos documentales y APIs:

### Conceptos aplicados:
- **Manejo de archivos binarios**: He aprendido a trabajar con imágenes como datos binarios, abriendo archivos en modo `"rb"` y procesándolos correctamente.

- **Codificación Base64**: Comprendo ahora cómo transformar datos binarios a un formato de texto que puede ser transmitido fácilmente a través de protocolos HTTP, esencial para trabajar con APIs REST.

- **Conexiones HTTP**: He establecido conexiones con una API externa mediante solicitudes POST, enviando datos estructurados en formato JSON y recibiendo respuestas procesables.

- **Gestión de recursos**: El uso de `with` para manejar archivos garantiza que los recursos se cierren automáticamente, evitando fugas de memoria o archivos bloqueados.

### Utilidad práctica:
Este tipo de interacción con APIs es fundamental en el desarrollo moderno de aplicaciones. Me permite:
- Integrar servicios de inteligencia artificial en mis aplicaciones
- Procesar y analizar contenido multimedia sin necesidad de desarrollar algoritmos complejos
- Entender cómo funcionan aplicaciones reales que utilizo diariamente (redes sociales, apps de fotos, etc.)

---

La capacidad de conectarme a APIs y enviar datos estructurados es una habilidad esencial en el acceso a datos moderno. Este ejercicio me ha mostrado cómo los conceptos teóricos de la unidad (establecimiento de conexiones, envío de datos, procesamiento de respuestas) se aplican en situaciones reales y cotidianas, convirtiendo una simple curiosidad sobre una imagen de perro en una oportunidad de aprendizaje significativa.