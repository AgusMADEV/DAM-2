# 🎵 Actividad: Generador de Waveform para MP3

## 📋 Descripción
Esta actividad consiste en crear un sistema completo para generar y visualizar la forma de onda (waveform) de un archivo MP3. El proyecto se divide en dos partes principales:

1. **Backend Python**: Generación de la imagen waveform
2. **Frontend HTML/JS**: Visualización interactiva

## 🎯 Objetivos de Aprendizaje
- Trabajar con archivos multimedia usando `pydub`
- Manipular arrays de datos con `numpy`
- Generar imágenes con `Pillow (PIL)`
- Crear interfaces web interactivas con HTML5 y JavaScript
- Integrar backend y frontend en un proyecto completo

## 📦 Requisitos

### Librerías Python
```bash
pip install pydub
pip install numpy
pip install Pillow
```

### Archivos necesarios
- `0802.mp3` - Archivo de audio de entrada (debe estar en la misma carpeta)
- `generar_waveform.py` - Script Python para generar la waveform
- `visualizar_waveform.html` - Interfaz web para visualizar

## 🚀 Instrucciones de Uso

### Paso 1: Preparar el archivo de audio
Asegúrate de tener un archivo MP3 llamado `0802.mp3` en la misma carpeta que los scripts. Si quieres usar otro archivo, modifica el nombre en:
- Línea 71 de `generar_waveform.py`
- Línea 144 de `visualizar_waveform.html`

### Paso 2: Generar la waveform
Ejecuta el script Python:
```bash
python generar_waveform.py
```

Esto creará un archivo `waveform.png` con la visualización de la forma de onda.

**Salida esperada:**
```
🎵 Generador de Waveform
----------------------------------------
📂 Cargando archivo: 0802.mp3
✓ Audio cargado: XXXXX muestras
  - Duración: X.XX segundos
  - Canales: X
  - Sample rate: XXXXX Hz

🎨 Generando waveform...
✓ Waveform guardada como: waveform.png

✅ Proceso completado con éxito!
```

### Paso 3: Visualizar en el navegador
Abre el archivo `visualizar_waveform.html` en tu navegador web favorito.

## 📝 Estructura del Código

### generar_waveform.py

#### Función `cargar_audio(ruta_archivo)`
- **Propósito**: Cargar un archivo MP3 y convertirlo en array de muestras
- **Entrada**: Ruta del archivo MP3
- **Salida**: Tupla (samples, audio)
- **Tecnologías**: pydub, numpy

#### Función `generar_waveform(samples, ancho, alto, color_onda)`
- **Propósito**: Crear una imagen que representa la forma de onda
- **Parámetros**:
  - `samples`: Array de muestras de audio
  - `ancho`: Ancho de la imagen (por defecto 1200px)
  - `alto`: Alto de la imagen (por defecto 400px)
  - `color_onda`: Color RGB (por defecto azul)
- **Salida**: Objeto Image de Pillow
- **Técnica**: Cápsulas redondeadas para cada segmento de audio

#### Función `main()`
- **Propósito**: Orquestar todo el proceso
- **Flujo**:
  1. Cargar el archivo MP3
  2. Generar la imagen waveform
  3. Guardar como PNG

### visualizar_waveform.html

#### Componentes HTML
- **Contenedor principal**: Diseño responsivo con gradiente
- **Sección de información**: Detalles del proyecto
- **Contenedor de waveform**: Área para mostrar la imagen
- **Controles de audio**: Botones de reproducción
- **Reproductor de audio**: Elemento `<audio>` de HTML5

#### Funciones JavaScript
- `reproducirAudio()`: Inicia la reproducción
- `pausarAudio()`: Pausa el audio
- `reiniciarAudio()`: Detiene y reinicia
- `descargarWaveform()`: Descarga la imagen PNG

## 🎨 Personalización

### Cambiar el color de la waveform
En `generar_waveform.py`, línea 79:
```python
imagen = generar_waveform(samples, ancho=1200, alto=400)
```

Puedes añadir el parámetro color:
```python
# Rojo
imagen = generar_waveform(samples, ancho=1200, alto=400, color_onda=(220, 53, 69))

# Verde
imagen = generar_waveform(samples, ancho=1200, alto=400, color_onda=(40, 167, 69))

# Morado
imagen = generar_waveform(samples, ancho=1200, alto=400, color_onda=(111, 66, 193))
```

### Cambiar las dimensiones
Modifica los parámetros `ancho` y `alto`:
```python
# Waveform más grande
imagen = generar_waveform(samples, ancho=1600, alto=600)

# Waveform más compacta
imagen = generar_waveform(samples, ancho=800, alto=300)
```

### Modificar el grosor de las barras
En `generar_waveform.py`, línea 57:
```python
ancho_barra = 2  # Cambiar a 3, 4, 5, etc.
```

## 🔍 Conceptos Técnicos

### Forma de Onda (Waveform)
Una representación visual de la amplitud del audio a lo largo del tiempo. Cada barra vertical representa la intensidad del sonido en un momento específico.

### Normalización
Proceso de ajustar los valores de las muestras para que se ajusten al rango de píxeles disponible:
```python
valor_normalizado = valor_max / valor_maximo
```

### Cápsulas Redondeadas
Rectángulos con esquinas redondeadas que dan un aspecto más suave y moderno a la visualización.

## ⚠️ Solución de Problemas

### Error: "No module named 'pydub'"
```bash
pip install pydub
```

### Error: "FileNotFoundError: 0802.mp3"
Asegúrate de que el archivo MP3 está en la misma carpeta que el script.

### La waveform no se muestra en el navegador
1. Verifica que `waveform.png` se generó correctamente
2. Abre la consola del navegador (F12) para ver errores
3. Asegúrate de que todos los archivos están en la misma carpeta

### El audio no se reproduce
Verifica que el archivo `0802.mp3` existe y es un archivo MP3 válido.

## 📚 Recursos Adicionales

- [Documentación de pydub](https://github.com/jiaaro/pydub)
- [Documentación de Pillow](https://pillow.readthedocs.io/)
- [HTML5 Audio API](https://developer.mozilla.org/es/docs/Web/HTML/Element/audio)

## ✅ Criterios de Evaluación

- ✓ El código carga correctamente el archivo MP3
- ✓ Se genera una imagen PNG con la waveform
- ✓ La visualización HTML es funcional e interactiva
- ✓ El código está bien estructurado y comentado
- ✓ Se utilizan nombres descriptivos para funciones y variables
- ✓ El proyecto es fácil de ejecutar siguiendo las instrucciones

## 🎓 Conclusión

Este proyecto integra múltiples conceptos de programación:
- Manejo de archivos multimedia
- Procesamiento de señales
- Visualización de datos
- Desarrollo web frontend
- Integración de tecnologías

¡Experimenta con diferentes archivos de audio y personaliza la visualización a tu gusto!
