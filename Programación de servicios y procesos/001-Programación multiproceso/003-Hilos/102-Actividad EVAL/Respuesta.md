Como aficionado a la **fotografía digital**, a veces necesito aplicar filtros rápidos (por ejemplo, **invertir colores**) a imágenes grandes. Este ejercicio muestra cómo **paralelizar** ese proceso en Python: divido la imagen en **bloques horizontales** y proceso cada bloque en **hilos** para acelerar el tiempo total, algo útil cuando trabajo con fotos pesadas o lotes.

---

El script aplica **inversión de colores** con Pillow (PIL) y reparte el trabajo entre varios hilos usando `ThreadPoolExecutor`.  
Puntos clave correctamente implementados en el código:

```python
from PIL import Image, ImageOps
from concurrent.futures import ThreadPoolExecutor, as_completed
import time, os

NUCLEOS = os.cpu_count()
ENTRADA = "agustin.png"
SALIDA  = "agustin2.png"

def procesa_bloque(img, y0, y1):
    box = (0, y0, img.width, y1)
    recorte = img.crop(box)
    return y0, ImageOps.invert(recorte.convert("RGB"))

def main():
    inicio = time.time()
    with Image.open(ENTRADA) as im:
        img = im.convert("RGB")
        img.load()

    alto, ancho = img.height, img.width
    numero_hilos = max(1, min(NUCLEOS, alto))
    bloque_altura = alto // numero_hilos

    rangos = []
    for i in range(numero_hilos):
        y0 = i * bloque_altura
        y1 = (i + 1) * bloque_altura if i < numero_hilos - 1 else alto
        if y1 > y0:
            rangos.append((y0, y1))

    resultados = []
    with ThreadPoolExecutor(max_workers=numero_hilos) as ex:
        futs = [ex.submit(procesa_bloque, img, y0, y1) for (y0, y1) in rangos]
        for f in as_completed(futs):
            resultados.append(f.result())

    salida = Image.new("RGB", (ancho, alto))
    for y0, bloque in sorted(resultados, key=lambda t: t[0]):
        salida.paste(bloque, (0, y0))

    salida.save(SALIDA, quality=95)
    tiempo_final = time.time() - inicio
    print(f"{tiempo_final:.3f} segundos")

if __name__ == "__main__":
    main()
```

- **Inversión de color:** `ImageOps.invert()` tras `convert("RGB")`.
- **Paralelismo por bloques:** cada hilo procesa un **recorte** independiente (sin conflicto entre hilos).
- **Orden garantizado:** se ordenan los resultados por `y0` antes de pegarlos.
- **Rendimiento realista:** Pillow usa código C, lo que permite que los hilos aporten **aceleración real**.

---

### 🔹 Código sin optimizar (versión secuencial)
Este es el código base, donde se recorre píxel a píxel sin paralelismo:
```python
from PIL import Image
import time

inicio = int(time.time())
img = Image.open("agustin.png")
tamanio = img.size
pixels = img.load()
for x in range(0,tamanio[0]):
  for y in range(0,tamanio[1]):
    pixel = img.getpixel((x, y))
    pixels[x, y] = (255-pixel[0], 255-pixel[1], 255-pixel[2])
    
img.save("agustin2.png")
final = int(time.time())
print((final-inicio),"segundos")
```
🔸 En este caso, todo el proceso se ejecuta **en un solo hilo**, lo que hace que el tiempo de ejecución aumente proporcionalmente al tamaño de la imagen.

---

### 🔹 Código optimizado (versión multihilo)
La versión optimizada divide la imagen en bloques horizontales y procesa cada bloque en paralelo usando **ThreadPoolExecutor**:
```python
# Versión multihilo
from PIL import Image, ImageOps
from concurrent.futures import ThreadPoolExecutor, as_completed
import time, os

NUCLEOS = os.cpu_count()
ENTRADA = "agustin.png"
SALIDA  = "agustin2.png"

def procesa_bloque(img, y0, y1):
    box = (0, y0, img.width, y1)
    recorte = img.crop(box)
    return y0, ImageOps.invert(recorte.convert("RGB"))

def main():
    inicio = time.time()
    with Image.open(ENTRADA) as im:
        img = im.convert("RGB")
        img.load()

    alto, ancho = img.height, img.width
    numero_hilos = max(1, min(NUCLEOS, alto))
    bloque_altura = alto // numero_hilos

    rangos = [(i * bloque_altura, alto if i == numero_hilos - 1 else (i + 1) * bloque_altura) for i in range(numero_hilos)]

    resultados = []
    with ThreadPoolExecutor(max_workers=numero_hilos) as ex:
        futs = [ex.submit(procesa_bloque, img, y0, y1) for (y0, y1) in rangos]
        for f in as_completed(futs):
            resultados.append(f.result())

    salida = Image.new("RGB", (ancho, alto))
    for y0, bloque in sorted(resultados, key=lambda t: t[0]):
        salida.paste(bloque, (0, y0))

    salida.save(SALIDA, quality=95)
    print(f"{time.time() - inicio:.3f} segundos")

if __name__ == "__main__":
    main()
```

---

El uso de **hilos y multihilo** reduce **tiempos de proceso** en tareas intensivas de imagen cuando la librería (Pillow) libera el GIL.  
Este patrón (particionar → procesar en paralelo → recomponer) es reutilizable para otros flujos de **fotografía digital**:  
- aplicar filtros de color o brillo por zonas,  
- crear versiones optimizadas de imágenes,  
- automatizar preprocesado de grandes galerías.  

Con esta práctica he comprendido cómo aprovechar **todos los núcleos del procesador** en tareas gráficas y cómo aplicar los conceptos de **concurrencia** de la unidad a mis proyectos personales de fotografía.
