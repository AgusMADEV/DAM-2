Para Programacion de Procesos y servicios, el proyecto que he desarrollado es una **aplicación multinúcleo** que reparte el trabajo de **procesamiento de imágenes** entre varios hilos y/o procesos del sistema. La idea es paralelizar tareas **CPU‑bound** (aplicación de filtros con Pillow) para **acelerar el tiempo total de ejecución** y ofrecer **feedback en tiempo real** mediante WebSockets a un frontend web.

#### ¿Para qué sirve y en qué contexto se usa?
- **Caso de uso profesional:** técnicos de marketing, fotógrafos, diseñadores o equipos de soporte que necesitan **lotes de transformaciones** (blur, escala de grises, posterizar, marca de agua, etc.) sobre **carpetas enteras** de imágenes.  
- **Entorno:** backend Python con `multiprocessing`/`concurrent.futures`, **servidor WebSocket** para eventos de progreso y **frontend** en HTML/CSS/JS para monitorización y control.

**Árbol de desarrollo del software:**
├── backend
│   ├── filtros.py
│   ├── procesador.py
│   └── servidor_websocket.py
├── frontend
│   ├── app.js
│   ├── index.html
│   ├── styles.css
│   └── workers
│       └── monitor.js
├── generar_imagenes_prueba.py (no necesario)
├── input_images
└──  output_images  

---

### Definiciones y terminología del temario
- **CPU‑bound vs I/O‑bound:** El filtrado de imágenes es **CPU‑bound** → se beneficia de **procesos** paralelos (aislamiento de GIL en CPython) más que de hilos. Para operaciones con mucha E/S, los **threads** pueden ser suficientes.  
- **Escalabilidad horizontal en cliente:** el frontend delega procesamiento a backend y muestra métricas en tiempo real vía **WebSockets**.  
- **Granularidad de tareas:** una **imagen = unidad de trabajo**, ideal para repartir en un **pool de procesos**.

### Funcionamiento
1. **Selección del modo y filtros en el frontend** (`frontend/index.html` + `frontend/app.js`).  
2. **Comando vía WebSocket** al servidor (`backend/servidor_websocket.py` → `comando_procesar`).  
3. **Orquestación del batch** en `ProcesadorImagenes.procesar_batch(...)` (archivo `backend/procesador.py`):  
   - Divide el lote de imágenes.  
   - Por cada filtro elegido, lanza **`ProcessPoolExecutor`** (modo recomendado para CPU) o **`ThreadPoolExecutor`**.  
   - Cada tarea invoca `aplicar_filtro(...)` de `backend/filtros.py`.  
4. **Progreso en tiempo real:** el backend emite eventos (callback) y el **frontend** actualiza la barra y las estadísticas.  
5. **Resultados y métricas:** el backend devuelve estadísticas (tiempo total, éxitos/fallos, tiempo medio por imagen), y el frontend las presenta con estilo.

### Código del proyecto (fragmentos representativos)

**Procesamiento paralelo con procesos** (en `backend/procesador.py`, bloque `__main__`):  
```python
DIR_ENTRADA = "../input_images"
DIR_SALIDA = "../output_images"

procesador = ProcesadorImagenes(callback_progreso=callback_ejemplo)
imagenes = obtener_imagenes_directorio(DIR_ENTRADA)

stats = procesador.procesar_con_procesos(imagenes, 'blur', DIR_SALIDA)
```

**Aplicación de un filtro** (función en `backend/filtros.py`):  
```py
def aplicar_filtro(ruta_entrada, ruta_salida, nombre_filtro, parametros=None):
    imagen = Image.open(ruta_entrada)
    filtros = FiltrosImagen.obtener_filtros_disponibles()
    filtro = filtros[nombre_filtro]
    imagen_procesada = filtro(imagen.copy(), **parametros) if parametros else filtro(imagen.copy())
    imagen_procesada.save(ruta_salida)
    return True
```

**Listado de filtros disponibles** (`backend/filtros.py`):  
- `invertir`, `grises`, `blur`, `nitidez`, `brillo`, `contraste`, `sepia`, `bordes`, `relieve`, `posterizar`, `redimensionar`, `marca_agua`.

**Canal de tiempo real (WebSocket)** (`backend/servidor_websocket.py` → difunde progreso):  
```py
await self.broadcast({
    'tipo': 'progreso',
    'datos': info
})
```

### Ejemplos reales incluidos en el repo
- **Generación de imágenes de prueba:** `generar_imagenes_prueba.py` crea gradientes, geométricas y patrones en `input_images/`.  
- **UI de control:** en el **frontend** se seleccionan filtros y modo (threads/procesos), se inicia el lote y se visualiza el avance (porcentaje, img/s, núcleos).

---

### **Cómo se aplica en la práctica:**

1. **Preparar lote**: colocar imágenes en `input_images/`.  
2. **Levantar backend**: `python backend/servidor_websocket.py`.  
3. **Abrir interfaz**: `frontend/index.html`. Marcar filtros (p. ej., `grises`, `sepia`, `invertir`) y **modo “procesos”**.  
4. **Iniciar**: el servidor reparte imágenes a procesos, aplica filtros y envía **progreso en tiempo real** (velocidad, % y tiempo).  
5. **Consumo profesional**: resultados organizados por filtro en `output_images/<filtro>/...`, listos para campañas o catálogos.

```python
# backend/procesador.py
resultados = procesador.procesar_batch(imagenes[:3], ['grises', 'sepia', 'invertir'], DIR_SALIDA)
```
> El frontend muestra para cada filtro: tiempo total, éxitos/fallos, tiempo/imagen y núcleos usados.

---


#### Filtro Aplicado en Paralelo

```py
@staticmethod
def blur(imagen, radio=5):
    return imagen.filter(ImageFilter.GaussianBlur(radius=radio))

def aplicar_filtro(ruta_entrada, ruta_salida, nombre_filtro, parametros=None):
    try:
        imagen = Image.open(ruta_entrada)
        filtros = FiltrosImagen.obtener_filtros_disponibles()
        filtro = filtros[nombre_filtro]
        
        # Aplicación del filtro (operación CPU-intensive)
        imagen_procesada = filtro(imagen.copy())
        imagen_procesada.save(ruta_salida)
        
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
```

#### Gestión de Concurrencia Real

**Problema resuelto:** Múltiples procesos escribiendo estadísticas simultáneamente

```py
class ProcesadorImagenes:
    def __init__(self):
        self.lock = threading.Lock()  # Protección de sección crítica
        self.imagenes_procesadas = 0  # Variable compartida
    
    def _reportar_progreso(self, imagen, estado, mensaje=""):
        with self.lock:  # Solo un hilo puede modificar estadísticas
            if estado == 'completado':
                self.imagenes_procesadas += 1
                self.estadisticas['exitosas'] += 1
```

#### Web Workers en el Frontend

```js
// monitor.js - Worker para monitorización sin bloquear UI
function actualizarEstadisticas(datos) {
    estadisticas.totalProcesadas = datos.procesadas;
    estadisticas.tiempoTotal = datos.tiempo_transcurrido;
    
    // Cálculos pesados en background
    if (datos.tiempo_transcurrido > 0) {
        estadisticas.velocidadPromedio = datos.procesadas / datos.tiempo_transcurrido;
    }
    
    // Notificar al hilo principal
    self.postMessage({
        tipo: 'progreso',
        datos: estadisticas
    });
}
```
## Backend:

`filtros.py`:
```py
from PIL import Image, ImageFilter, ImageEnhance
import os

class FiltrosImagen:
    @staticmethod
    def invertir_colores(imagen):
        pixels = imagen.load()
        width, height = imagen.size
        
        for x in range(width):
            for y in range(height):
                pixel = imagen.getpixel((x, y))
                if isinstance(pixel, tuple) and len(pixel) >= 3:
                    pixels[x, y] = (255 - pixel[0], 255 - pixel[1], 255 - pixel[2])
                    
        return imagen
    
    @staticmethod
    def escala_grises(imagen):
        return imagen.convert('L').convert('RGB')
    
    @staticmethod
    def blur(imagen, radio=5):
        return imagen.filter(ImageFilter.GaussianBlur(radius=radio))
    
    @staticmethod
    def nitidez(imagen, factor=2.0):
        enhancer = ImageEnhance.Sharpness(imagen)
        return enhancer.enhance(factor)
    
    @staticmethod
    def brillo(imagen, factor=1.5):
        enhancer = ImageEnhance.Brightness(imagen)
        return enhancer.enhance(factor)
    
    @staticmethod
    def contraste(imagen, factor=1.5):
        enhancer = ImageEnhance.Contrast(imagen)
        return enhancer.enhance(factor)
    
    @staticmethod
    def sepia(imagen):
        pixels = imagen.load()
        width, height = imagen.size
        
        for x in range(width):
            for y in range(height):
                pixel = imagen.getpixel((x, y))
                if isinstance(pixel, tuple) and len(pixel) >= 3:
                    r, g, b = pixel[0], pixel[1], pixel[2]
                    
                    # Fórmula sepia
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                    
                    # Asegurar que los valores estén en el rango 0-255
                    pixels[x, y] = (min(255, tr), min(255, tg), min(255, tb))
                    
        return imagen
    
    @staticmethod
    def detectar_bordes(imagen):
        return imagen.filter(ImageFilter.FIND_EDGES)
    
    @staticmethod
    def relieve(imagen):
        return imagen.filter(ImageFilter.EMBOSS)
    
    @staticmethod
    def posterizar(imagen, bits=4):
        from PIL import ImageOps
        return ImageOps.posterize(imagen, bits)
    
    @staticmethod
    def redimensionar(imagen, porcentaje=50):
        width, height = imagen.size
        nuevo_ancho = int(width * porcentaje / 100)
        nuevo_alto = int(height * porcentaje / 100)
        return imagen.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
    
    @staticmethod
    def marca_agua(imagen, texto="PROCESADO", opacidad=0.3):
        from PIL import ImageDraw, ImageFont
        
        # Crear una capa transparente
        marca = Image.new('RGBA', imagen.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(marca)
        
        # Intentar usar una fuente del sistema, si no, usar la predeterminada
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        # Calcular posición centrada
        bbox = draw.textbbox((0, 0), texto, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        width, height = imagen.size
        posicion = ((width - text_width) // 2, (height - text_height) // 2)
        
        # Dibujar texto con opacidad
        alpha = int(255 * opacidad)
        draw.text(posicion, texto, fill=(255, 255, 255, alpha), font=font)
        
        # Combinar con la imagen original
        imagen_rgba = imagen.convert('RGBA')
        resultado = Image.alpha_composite(imagen_rgba, marca)
        
        return resultado.convert('RGB')
    
    @staticmethod
    def obtener_filtros_disponibles():
        return {
            'invertir': FiltrosImagen.invertir_colores,
            'grises': FiltrosImagen.escala_grises,
            'blur': FiltrosImagen.blur,
            'nitidez': FiltrosImagen.nitidez,
            'brillo': FiltrosImagen.brillo,
            'contraste': FiltrosImagen.contraste,
            'sepia': FiltrosImagen.sepia,
            'bordes': FiltrosImagen.detectar_bordes,
            'relieve': FiltrosImagen.relieve,
            'posterizar': FiltrosImagen.posterizar,
            'redimensionar': FiltrosImagen.redimensionar,
            'marca_agua': FiltrosImagen.marca_agua
        }


def aplicar_filtro(ruta_entrada, ruta_salida, nombre_filtro, parametros=None):
    try:
        # Cargar imagen
        imagen = Image.open(ruta_entrada)
        
        # Obtener el filtro
        filtros = FiltrosImagen.obtener_filtros_disponibles()
        
        if nombre_filtro not in filtros:
            print(f"Filtro '{nombre_filtro}' no encontrado")
            return False
        
        filtro = filtros[nombre_filtro]
        
        # Aplicar filtro
        if parametros:
            imagen_procesada = filtro(imagen.copy(), **parametros)
        else:
            imagen_procesada = filtro(imagen.copy())
        
        # Guardar resultado
        imagen_procesada.save(ruta_salida)
        
        return True
        
    except Exception as e:
        print(f"Error al procesar {ruta_entrada}: {str(e)}")
        return False
```
`procesador.py`:
```py
import os
import time
import threading
import multiprocessing
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from filtros import aplicar_filtro, FiltrosImagen


class ProcesadorImagenes:
    def __init__(self, callback_progreso=None):
        self.num_nucleos = multiprocessing.cpu_count()
        self.callback_progreso = callback_progreso
        self.lock = threading.Lock()
        self.imagenes_procesadas = 0
        self.total_imagenes = 0
        self.tiempo_inicio = 0
        self.estadisticas = {
            'exitosas': 0,
            'fallidas': 0,
            'tiempo_total': 0,
            'nucleos_usados': self.num_nucleos
        }
        
    def _reportar_progreso(self, imagen, estado, mensaje=""):
        with self.lock:
            if estado == 'completado':
                self.imagenes_procesadas += 1
                self.estadisticas['exitosas'] += 1
            elif estado == 'error':
                self.imagenes_procesadas += 1
                self.estadisticas['fallidas'] += 1
            
            porcentaje = (self.imagenes_procesadas / self.total_imagenes * 100) if self.total_imagenes > 0 else 0
            tiempo_transcurrido = time.time() - self.tiempo_inicio
            
            info = {
                'imagen': imagen,
                'estado': estado,
                'mensaje': mensaje,
                'procesadas': self.imagenes_procesadas,
                'total': self.total_imagenes,
                'porcentaje': round(porcentaje, 2),
                'tiempo_transcurrido': round(tiempo_transcurrido, 2),
                'nucleos': self.num_nucleos
            }
            
            if self.callback_progreso:
                self.callback_progreso(info)
    
    def procesar_con_threads(self, imagenes, filtro, directorio_salida, max_workers=None):
        if max_workers is None:
            max_workers = self.num_nucleos * 2
        
        self.total_imagenes = len(imagenes)
        self.imagenes_procesadas = 0
        self.tiempo_inicio = time.time()
        
        print(f"\n🚀 Iniciando procesamiento con THREADS")
        print(f"📊 Núcleos disponibles: {self.num_nucleos}")
        print(f"🔧 Workers (threads): {max_workers}")
        print(f"📁 Imágenes a procesar: {self.total_imagenes}")
        print(f"🎨 Filtro: {filtro}\n")
        
        # Crear directorio de salida si no existe
        Path(directorio_salida).mkdir(parents=True, exist_ok=True)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futuros = []
            
            for ruta_imagen in imagenes:
                nombre_archivo = os.path.basename(ruta_imagen)
                nombre_sin_ext, ext = os.path.splitext(nombre_archivo)
                nombre_salida = f"{nombre_sin_ext}_{filtro}{ext}"
                ruta_salida = os.path.join(directorio_salida, nombre_salida)
                
                futuro = executor.submit(
                    self._procesar_imagen_individual,
                    ruta_imagen,
                    ruta_salida,
                    filtro,
                    'thread'
                )
                futuros.append(futuro)
            
            # Esperar a que todas las tareas terminen
            for futuro in as_completed(futuros):
                try:
                    futuro.result()
                except Exception as e:
                    print(f"❌ Error en thread: {str(e)}")
        
        self.estadisticas['tiempo_total'] = time.time() - self.tiempo_inicio
        return self.estadisticas
    
    def procesar_con_procesos(self, imagenes, filtro, directorio_salida, max_workers=None):
        if max_workers is None:
            max_workers = self.num_nucleos
        
        self.total_imagenes = len(imagenes)
        self.imagenes_procesadas = 0
        self.tiempo_inicio = time.time()
        
        print(f"\n🚀 Iniciando procesamiento con PROCESOS PARALELOS")
        print(f"📊 Núcleos disponibles: {self.num_nucleos}")
        print(f"🔧 Workers (procesos): {max_workers}")
        print(f"📁 Imágenes a procesar: {self.total_imagenes}")
        print(f"🎨 Filtro: {filtro}\n")
        
        # Crear directorio de salida si no existe
        Path(directorio_salida).mkdir(parents=True, exist_ok=True)
        
        # Preparar tareas
        tareas = []
        for ruta_imagen in imagenes:
            nombre_archivo = os.path.basename(ruta_imagen)
            nombre_sin_ext, ext = os.path.splitext(nombre_archivo)
            nombre_salida = f"{nombre_sin_ext}_{filtro}{ext}"
            ruta_salida = os.path.join(directorio_salida, nombre_salida)
            
            tareas.append((ruta_imagen, ruta_salida, filtro))
        
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futuros = []
            
            for tarea in tareas:
                futuro = executor.submit(aplicar_filtro, *tarea)
                futuros.append((futuro, tarea[0]))
            
            # Esperar y reportar progreso
            for futuro, ruta_imagen in futuros:
                nombre_archivo = os.path.basename(ruta_imagen)
                try:
                    resultado = futuro.result()
                    if resultado:
                        self._reportar_progreso(nombre_archivo, 'completado', 'Procesado exitosamente')
                    else:
                        self._reportar_progreso(nombre_archivo, 'error', 'Error al procesar')
                except Exception as e:
                    self._reportar_progreso(nombre_archivo, 'error', str(e))
        
        self.estadisticas['tiempo_total'] = time.time() - self.tiempo_inicio
        return self.estadisticas
    
    def _procesar_imagen_individual(self, ruta_entrada, ruta_salida, filtro, modo):
        nombre_archivo = os.path.basename(ruta_entrada)
        
        try:
            self._reportar_progreso(nombre_archivo, 'procesando', f'Procesando con {modo}...')
            
            resultado = aplicar_filtro(ruta_entrada, ruta_salida, filtro)
            
            if resultado:
                self._reportar_progreso(nombre_archivo, 'completado', 'Procesado exitosamente')
            else:
                self._reportar_progreso(nombre_archivo, 'error', 'Error al aplicar filtro')
                
        except Exception as e:
            self._reportar_progreso(nombre_archivo, 'error', str(e))
    
    def procesar_batch(self, imagenes, filtros, directorio_salida, modo='procesos'):
        resultados = []
        
        for filtro in filtros:
            print(f"\n{'='*60}")
            print(f"Aplicando filtro: {filtro.upper()}")
            print(f"{'='*60}")
            
            directorio_filtro = os.path.join(directorio_salida, filtro)
            
            if modo == 'threads':
                stats = self.procesar_con_threads(imagenes, filtro, directorio_filtro)
            else:
                stats = self.procesar_con_procesos(imagenes, filtro, directorio_filtro)
            
            stats['filtro'] = filtro
            resultados.append(stats)
            
            # Reiniciar estadísticas para el siguiente filtro
            self.estadisticas = {
                'exitosas': 0,
                'fallidas': 0,
                'tiempo_total': 0,
                'nucleos_usados': self.num_nucleos
            }
        
        return resultados
    
    def comparar_rendimiento(self, imagenes, filtro, directorio_salida):
        print("\n" + "="*60)
        print("COMPARACIÓN DE RENDIMIENTO: THREADS vs PROCESOS")
        print("="*60)
        
        # Test con threads
        dir_threads = os.path.join(directorio_salida, "test_threads")
        stats_threads = self.procesar_con_threads(imagenes, filtro, dir_threads)
        
        # Reiniciar estadísticas
        self.estadisticas = {
            'exitosas': 0,
            'fallidas': 0,
            'tiempo_total': 0,
            'nucleos_usados': self.num_nucleos
        }
        
        # Test con procesos
        dir_procesos = os.path.join(directorio_salida, "test_procesos")
        stats_procesos = self.procesar_con_procesos(imagenes, filtro, dir_procesos)
        
        # Calcular mejora
        mejora = ((stats_threads['tiempo_total'] - stats_procesos['tiempo_total']) 
                  / stats_threads['tiempo_total'] * 100)
        
        comparacion = {
            'threads': stats_threads,
            'procesos': stats_procesos,
            'mejora_porcentual': round(mejora, 2),
            'ganador': 'procesos' if stats_procesos['tiempo_total'] < stats_threads['tiempo_total'] else 'threads'
        }
        
        print("\n" + "="*60)
        print("RESULTADOS DE LA COMPARACIÓN")
        print("="*60)
        print(f"⏱️  Tiempo con THREADS: {stats_threads['tiempo_total']:.2f} segundos")
        print(f"⏱️  Tiempo con PROCESOS: {stats_procesos['tiempo_total']:.2f} segundos")
        print(f"📈 Mejora: {mejora:.2f}% {'más rápido' if mejora > 0 else 'más lento'}")
        print(f"🏆 Ganador: {comparacion['ganador'].upper()}")
        print("="*60)
        
        return comparacion


def obtener_imagenes_directorio(directorio, extensiones=None):
    if extensiones is None:
        extensiones = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    
    imagenes = []
    
    if not os.path.exists(directorio):
        print(f"⚠️  El directorio {directorio} no existe")
        return imagenes
    
    for archivo in os.listdir(directorio):
        ext = os.path.splitext(archivo)[1].lower()
        if ext in extensiones:
            ruta_completa = os.path.join(directorio, archivo)
            imagenes.append(ruta_completa)
    
    return imagenes


# Función de callback de ejemplo
def callback_ejemplo(info):
    print(f"[{info['porcentaje']:.1f}%] {info['imagen']} - {info['estado']} - {info['mensaje']}")


if __name__ == "__main__":
    # Configuración
    DIR_ENTRADA = "../input_images"
    DIR_SALIDA = "../output_images"
    
    # Crear procesador
    procesador = ProcesadorImagenes(callback_progreso=callback_ejemplo)
    
    # Obtener imágenes
    imagenes = obtener_imagenes_directorio(DIR_ENTRADA)
    
    if not imagenes:
        print("⚠️  No se encontraron imágenes en el directorio de entrada")
        print(f"📁 Coloca imágenes en: {os.path.abspath(DIR_ENTRADA)}")
    else:
        print(f"\n✅ Se encontraron {len(imagenes)} imágenes")
        
        # Ejemplo 1: Procesar con un filtro usando procesos
        print("\n" + "="*60)
        print("EJEMPLO 1: Procesamiento con procesos paralelos")
        print("="*60)
        stats = procesador.procesar_con_procesos(imagenes, 'blur', DIR_SALIDA)
        
        print("\n📊 ESTADÍSTICAS FINALES:")
        print(f"✅ Exitosas: {stats['exitosas']}")
        print(f"❌ Fallidas: {stats['fallidas']}")
        print(f"⏱️  Tiempo total: {stats['tiempo_total']:.2f} segundos")
        print(f"⚡ Imágenes/segundo: {stats['exitosas']/stats['tiempo_total']:.2f}")
        
        # Ejemplo 2: Procesar múltiples filtros
        if len(imagenes) >= 3:
            print("\n" + "="*60)
            print("EJEMPLO 2: Batch con múltiples filtros")
            print("="*60)
            
            # Reiniciar estadísticas
            procesador.estadisticas = {
                'exitosas': 0,
                'fallidas': 0,
                'tiempo_total': 0,
                'nucleos_usados': procesador.num_nucleos
            }
            
            filtros = ['grises', 'sepia', 'invertir']
            resultados = procesador.procesar_batch(imagenes[:3], filtros, DIR_SALIDA)
            
            print("\n📊 RESUMEN FINAL:")
            for resultado in resultados:
                print(f"\n🎨 Filtro: {resultado['filtro']}")
                print(f"   ⏱️  Tiempo: {resultado['tiempo_total']:.2f}s")
                print(f"   ✅ Exitosas: {resultado['exitosas']}")
```

`Servidor_websockets.py`:
```py
import asyncio
import websockets
import json
import os
import threading
from pathlib import Path
from procesador import ProcesadorImagenes, obtener_imagenes_directorio


class ServidorWebSocket:
    def __init__(self, host='localhost', puerto=8765):
        self.host = host
        self.puerto = puerto
        self.clientes = set()
        self.procesador = None
        self.procesando = False
        
    async def registrar_cliente(self, websocket):
        self.clientes.add(websocket)
        print(f"✅ Cliente conectado. Total clientes: {len(self.clientes)}")
        
        # Enviar mensaje de bienvenida
        await self.enviar_mensaje(websocket, {
            'tipo': 'conexion',
            'mensaje': 'Conectado al servidor de procesamiento',
            'estado': 'conectado'
        })
    
    async def desregistrar_cliente(self, websocket):
        self.clientes.discard(websocket)
        print(f"❌ Cliente desconectado. Total clientes: {len(self.clientes)}")
    
    async def enviar_mensaje(self, websocket, datos):
        try:
            mensaje = json.dumps(datos, ensure_ascii=False)
            await websocket.send(mensaje)
        except websockets.exceptions.ConnectionClosed:
            pass
    
    async def broadcast(self, datos):
        if self.clientes:
            mensaje = json.dumps(datos, ensure_ascii=False)
            await asyncio.gather(
                *[cliente.send(mensaje) for cliente in self.clientes],
                return_exceptions=True
            )
    
    def callback_progreso(self, info):
        # Crear tarea asíncrona para enviar el mensaje
        asyncio.run(self.broadcast({
            'tipo': 'progreso',
            'datos': info
        }))
    
    async def procesar_comando(self, websocket, comando):
        tipo = comando.get('tipo', '')
        
        if tipo == 'listar_filtros':
            await self.comando_listar_filtros(websocket)
            
        elif tipo == 'listar_imagenes':
            await self.comando_listar_imagenes(websocket)
            
        elif tipo == 'procesar':
            await self.comando_procesar(websocket, comando)
            
        elif tipo == 'estado':
            await self.comando_estado(websocket)
            
        elif tipo == 'cancelar':
            await self.comando_cancelar(websocket)
            
        else:
            await self.enviar_mensaje(websocket, {
                'tipo': 'error',
                'mensaje': f'Comando desconocido: {tipo}'
            })
    
    async def comando_listar_filtros(self, websocket):
        from filtros import FiltrosImagen
        filtros = list(FiltrosImagen.obtener_filtros_disponibles().keys())
        
        await self.enviar_mensaje(websocket, {
            'tipo': 'filtros',
            'datos': filtros
        })
    
    async def comando_listar_imagenes(self, websocket):
        dir_entrada = "../input_images"
        imagenes = obtener_imagenes_directorio(dir_entrada)
        
        nombres = [os.path.basename(img) for img in imagenes]
        
        await self.enviar_mensaje(websocket, {
            'tipo': 'imagenes',
            'datos': {
                'cantidad': len(nombres),
                'imagenes': nombres
            }
        })
    
    async def comando_procesar(self, websocket, comando):
        if self.procesando:
            await self.enviar_mensaje(websocket, {
                'tipo': 'error',
                'mensaje': 'Ya hay un procesamiento en curso'
            })
            return
        
        self.procesando = True
        
        # Obtener parámetros
        filtros = comando.get('filtros', ['grises'])
        modo = comando.get('modo', 'procesos')
        
        # Obtener imágenes
        dir_entrada = "../input_images"
        dir_salida = "../output_images"
        imagenes = obtener_imagenes_directorio(dir_entrada)
        
        if not imagenes:
            await self.enviar_mensaje(websocket, {
                'tipo': 'error',
                'mensaje': 'No se encontraron imágenes para procesar'
            })
            self.procesando = False
            return
        
        # Notificar inicio
        await self.broadcast({
            'tipo': 'inicio_procesamiento',
            'datos': {
                'imagenes': len(imagenes),
                'filtros': filtros,
                'modo': modo
            }
        })
        
        # Ejecutar procesamiento en thread separado
        def ejecutar_procesamiento():
            # Crear procesador con callback adaptado
            def callback_async(info):
                try:
                    # Crear nuevo event loop para este thread
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(self.broadcast({
                        'tipo': 'progreso',
                        'datos': info
                    }))
                    loop.close()
                except Exception as e:
                    print(f"Error en callback: {e}")
            
            procesador = ProcesadorImagenes(callback_progreso=callback_async)
            
            try:
                resultados = procesador.procesar_batch(imagenes, filtros, dir_salida, modo)
                
                # Enviar resultados finales
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.broadcast({
                    'tipo': 'finalizado',
                    'datos': {
                        'resultados': resultados,
                        'mensaje': 'Procesamiento completado exitosamente'
                    }
                }))
                loop.close()
                
            except Exception as e:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.broadcast({
                    'tipo': 'error',
                    'mensaje': f'Error en el procesamiento: {str(e)}'
                }))
                loop.close()
            
            finally:
                self.procesando = False
        
        # Ejecutar en thread separado
        thread = threading.Thread(target=ejecutar_procesamiento, daemon=True)
        thread.start()
        
        await self.enviar_mensaje(websocket, {
            'tipo': 'aceptado',
            'mensaje': 'Procesamiento iniciado'
        })
    
    async def comando_estado(self, websocket):
        await self.enviar_mensaje(websocket, {
            'tipo': 'estado',
            'datos': {
                'procesando': self.procesando,
                'clientes_conectados': len(self.clientes)
            }
        })
    
    async def comando_cancelar(self, websocket):
        await self.enviar_mensaje(websocket, {
            'tipo': 'info',
            'mensaje': 'Funcionalidad de cancelación no implementada'
        })
    
    async def handler(self, websocket):
        await self.registrar_cliente(websocket)
        
        try:
            async for mensaje in websocket:
                try:
                    comando = json.loads(mensaje)
                    await self.procesar_comando(websocket, comando)
                except json.JSONDecodeError:
                    await self.enviar_mensaje(websocket, {
                        'tipo': 'error',
                        'mensaje': 'Formato de mensaje inválido'
                    })
                except Exception as e:
                    await self.enviar_mensaje(websocket, {
                        'tipo': 'error',
                        'mensaje': f'Error al procesar comando: {str(e)}'
                    })
        finally:
            await self.desregistrar_cliente(websocket)
    
    async def iniciar(self):
        print("="*60)
        print("🚀 SERVIDOR WEBSOCKET DE PROCESAMIENTO DE IMÁGENES")
        print("="*60)
        print(f"🌐 Host: {self.host}")
        print(f"🔌 Puerto: {self.puerto}")
        print(f"📡 Esperando conexiones...")
        print("="*60)
        
        async with websockets.serve(self.handler, self.host, self.puerto):
            await asyncio.Future()  # Ejecutar indefinidamente
    
    def ejecutar(self):
        try:
            asyncio.run(self.iniciar())
        except KeyboardInterrupt:
            print("\n\n👋 Servidor detenido por el usuario")


def main():
    # Crear directorios si no existen
    Path("../input_images").mkdir(parents=True, exist_ok=True)
    Path("../output_images").mkdir(parents=True, exist_ok=True)
    
    # Crear y ejecutar servidor
    servidor = ServidorWebSocket(host='localhost', puerto=8765)
    servidor.ejecutar()


if __name__ == "__main__":
    main()
```

## Frontend:

`index.html`:
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Procesador de Imágenes Multinúcleo</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header>
            <h1>🎨 Procesador de Imágenes Multinúcleo</h1>
            <p class="subtitle">Sistema de procesamiento paralelo en tiempo real</p>
            <div class="status-bar">
                <span id="conexion-estado" class="estado desconectado">● Desconectado</span>
                <span id="nucleos-info">🖥️ Núcleos: --</span>
                <span id="clientes-info">👥 Clientes: --</span>
            </div>
        </header>

        <!-- Panel de control -->
        <div class="panel-control">
            <div class="seccion">
                <h2>📁 Imágenes Disponibles</h2>
                <div class="imagenes-container">
                    <button id="btn-actualizar-imagenes" class="btn btn-secondary">🔄 Actualizar Lista</button>
                    <div id="lista-imagenes" class="lista-imagenes">
                        <p class="mensaje-placeholder">Conectando al servidor...</p>
                    </div>
                </div>
            </div>

            <div class="seccion">
                <h2>🎨 Filtros Disponibles</h2>
                <div id="filtros-container" class="filtros-grid">
                    <!-- Los filtros se cargarán dinámicamente -->
                </div>
                <button id="btn-seleccionar-todos" class="btn btn-secondary">✅ Seleccionar Todos</button>
                <button id="btn-deseleccionar-todos" class="btn btn-secondary">❌ Deseleccionar Todos</button>
            </div>

            <div class="seccion">
                <h2>⚙️ Configuración</h2>
                <div class="config-opciones">
                    <div class="opcion-grupo">
                        <label for="modo-procesamiento">Modo de Procesamiento:</label>
                        <select id="modo-procesamiento" class="select-modo">
                            <option value="procesos">🚀 Procesos Paralelos (Recomendado)</option>
                            <option value="threads">🧵 Threads</option>
                        </select>
                    </div>
                </div>
            </div>

            <div class="seccion-acciones">
                <button id="btn-procesar" class="btn btn-primary" disabled>
                    🚀 Iniciar Procesamiento
                </button>
                <button id="btn-cancelar" class="btn btn-danger" disabled>
                    ⛔ Cancelar
                </button>
            </div>
        </div>

        <!-- Panel de progreso -->
        <div class="panel-progreso">
            <h2>📊 Progreso del Procesamiento</h2>
            
            <div id="progreso-general" class="progreso-general oculto">
                <div class="progreso-info">
                    <span id="progreso-texto">Preparando procesamiento...</span>
                    <span id="progreso-porcentaje">0%</span>
                </div>
                <div class="barra-progreso">
                    <div id="barra-progreso-fill" class="barra-progreso-fill" style="width: 0%"></div>
                </div>
                <div class="progreso-stats">
                    <span>⏱️ Tiempo: <strong id="tiempo-transcurrido">0s</strong></span>
                    <span>📁 Procesadas: <strong id="imagenes-procesadas">0</strong> / <strong id="imagenes-total">0</strong></span>
                    <span>⚡ Velocidad: <strong id="velocidad">--</strong> img/s</span>
                </div>
            </div>

            <div id="log-container" class="log-container">
                <div class="log-header">
                    <h3>📋 Log de Actividad</h3>
                    <button id="btn-limpiar-log" class="btn btn-small">🗑️ Limpiar</button>
                </div>
                <div id="log-content" class="log-content">
                    <p class="log-item info">Sistema iniciado. Esperando conexión...</p>
                </div>
            </div>
        </div>

        <!-- Panel de resultados -->
        <div id="panel-resultados" class="panel-resultados oculto">
            <h2>✅ Resultados del Procesamiento</h2>
            <div id="resultados-content" class="resultados-content">
                <!-- Los resultados se mostrarán aquí -->
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer>
        <p>Desarrollado para la asignatura de Programación de Servicios y Procesos</p>
        <p>Actividad Final - Unidad 1: Programación Multiproceso</p>
    </footer>

    <!-- Scripts -->
    <script src="app.js"></script>
</body>
</html>
```

`app.js`
```js
class AplicacionProcesadorImagenes {
    constructor() {
        this.ws = null;
        this.conectado = false;
        this.filtrosDisponibles = [];
        this.filtrosSeleccionados = new Set();
        this.procesando = false;
        
        // Worker para tareas en segundo plano
        this.worker = null;
        
        // Estadísticas
        this.estadisticas = {
            inicio: null,
            imagenesProcesadas: 0,
            imagenesTotal: 0
        };
        
        this.inicializar();
    }
    
    inicializar() {
        console.log('🚀 Inicializando aplicación...');
        this.conectarWebSocket();
        this.inicializarEventos();
        this.inicializarWorker();
    }
    
    // ==================== WEBSOCKET ====================
    
    conectarWebSocket() {
        this.log('Conectando al servidor WebSocket...', 'info');
        
        try {
            this.ws = new WebSocket('ws://localhost:8765');
            
            this.ws.onopen = () => this.alConectar();
            this.ws.onmessage = (event) => this.alRecibirMensaje(event);
            this.ws.onerror = (error) => this.alError(error);
            this.ws.onclose = () => this.alDesconectar();
            
        } catch (error) {
            this.log(`Error al conectar: ${error.message}`, 'error');
            this.actualizarEstadoConexion(false);
        }
    }
    
    alConectar() {
        this.conectado = true;
        this.actualizarEstadoConexion(true);
        this.log('✅ Conectado al servidor exitosamente', 'success');
        
        // Solicitar información inicial
        this.solicitarFiltros();
        this.solicitarImagenes();
    }
    
    alRecibirMensaje(event) {
        try {
            const mensaje = JSON.parse(event.data);
            this.procesarMensaje(mensaje);
        } catch (error) {
            this.log(`Error al procesar mensaje: ${error.message}`, 'error');
        }
    }
    
    alError(error) {
        this.log(`Error de WebSocket: ${error.message}`, 'error');
        this.actualizarEstadoConexion(false);
    }
    
    alDesconectar() {
        this.conectado = false;
        this.actualizarEstadoConexion(false);
        this.log('❌ Desconectado del servidor', 'error');
        
        // Intentar reconectar después de 3 segundos
        setTimeout(() => {
            if (!this.conectado) {
                this.log('Intentando reconectar...', 'info');
                this.conectarWebSocket();
            }
        }, 3000);
    }
    
    enviarComando(comando) {
        if (!this.conectado || !this.ws) {
            this.log('No hay conexión con el servidor', 'error');
            return;
        }
        
        try {
            this.ws.send(JSON.stringify(comando));
        } catch (error) {
            this.log(`Error al enviar comando: ${error.message}`, 'error');
        }
    }
    
    // ==================== PROCESAMIENTO DE MENSAJES ====================
    
    procesarMensaje(mensaje) {
        const tipo = mensaje.tipo;
        
        switch (tipo) {
            case 'conexion':
                this.log(mensaje.mensaje, 'success');
                break;
                
            case 'filtros':
                this.actualizarFiltros(mensaje.datos);
                break;
                
            case 'imagenes':
                this.actualizarImagenes(mensaje.datos);
                break;
                
            case 'inicio_procesamiento':
                this.iniciarProcesamientoUI(mensaje.datos);
                break;
                
            case 'progreso':
                this.actualizarProgreso(mensaje.datos);
                break;
                
            case 'finalizado':
                this.finalizarProcesamiento(mensaje.datos);
                break;
                
            case 'error':
                this.log(`❌ Error: ${mensaje.mensaje}`, 'error');
                this.procesando = false;
                this.actualizarBotones();
                break;
                
            case 'aceptado':
                this.log(mensaje.mensaje, 'success');
                break;
                
            default:
                console.log('Mensaje desconocido:', mensaje);
        }
    }
    
    // ==================== UI - FILTROS ====================
    
    solicitarFiltros() {
        this.enviarComando({ tipo: 'listar_filtros' });
    }
    
    actualizarFiltros(filtros) {
        this.filtrosDisponibles = filtros;
        const container = document.getElementById('filtros-container');
        container.innerHTML = '';
        
        const descripciones = {
            'invertir': '🔄 Invertir Colores',
            'grises': '⬜ Escala de Grises',
            'blur': '🌫️ Desenfocar (Blur)',
            'nitidez': '✨ Aumentar Nitidez',
            'brillo': '💡 Ajustar Brillo',
            'contraste': '🎚️ Ajustar Contraste',
            'sepia': '📜 Efecto Sepia',
            'bordes': '🔲 Detectar Bordes',
            'relieve': '🗻 Efecto Relieve',
            'posterizar': '🎨 Posterizar',
            'redimensionar': '📏 Redimensionar',
            'marca_agua': '©️ Marca de Agua'
        };
        
        filtros.forEach(filtro => {
            const div = document.createElement('div');
            div.className = 'filtro-item';
            div.dataset.filtro = filtro;
            
            div.innerHTML = `
                <input type="checkbox" class="filtro-checkbox" id="filtro-${filtro}">
                <label for="filtro-${filtro}">${descripciones[filtro] || filtro}</label>
            `;
            
            div.addEventListener('click', (e) => {
                if (e.target.tagName !== 'INPUT') {
                    const checkbox = div.querySelector('input');
                    checkbox.checked = !checkbox.checked;
                }
                this.toggleFiltro(filtro, div.querySelector('input').checked);
                div.classList.toggle('seleccionado');
            });
            
            container.appendChild(div);
        });
        
        this.log(`📋 Cargados ${filtros.length} filtros disponibles`, 'info');
    }
    
    toggleFiltro(filtro, seleccionado) {
        if (seleccionado) {
            this.filtrosSeleccionados.add(filtro);
        } else {
            this.filtrosSeleccionados.delete(filtro);
        }
        this.actualizarBotones();
    }
    
    // ==================== UI - IMÁGENES ====================
    
    solicitarImagenes() {
        this.enviarComando({ tipo: 'listar_imagenes' });
    }
    
    actualizarImagenes(datos) {
        const container = document.getElementById('lista-imagenes');
        
        if (datos.cantidad === 0) {
            container.innerHTML = '<p class="mensaje-placeholder">⚠️ No hay imágenes en el directorio input_images</p>';
            this.log('No se encontraron imágenes para procesar', 'warning');
            return;
        }
        
        container.innerHTML = '';
        datos.imagenes.forEach(imagen => {
            const div = document.createElement('div');
            div.className = 'imagen-item';
            div.innerHTML = `
                <span>📷</span>
                <span>${imagen}</span>
            `;
            container.appendChild(div);
        });
        
        this.log(`✅ Encontradas ${datos.cantidad} imágenes`, 'success');
        this.actualizarBotones();
    }
    
    // ==================== UI - PROCESAMIENTO ====================
    
    iniciarProcesamiento() {
        if (this.filtrosSeleccionados.size === 0) {
            this.log('⚠️ Selecciona al menos un filtro', 'warning');
            return;
        }
        
        const modo = document.getElementById('modo-procesamiento').value;
        const filtros = Array.from(this.filtrosSeleccionados);
        
        this.enviarComando({
            tipo: 'procesar',
            filtros: filtros,
            modo: modo
        });
        
        this.procesando = true;
        this.actualizarBotones();
    }
    
    iniciarProcesamientoUI(datos) {
        this.estadisticas.inicio = Date.now();
        this.estadisticas.imagenesProcesadas = 0;
        this.estadisticas.imagenesTotal = datos.imagenes;
        
        const panel = document.getElementById('progreso-general');
        panel.classList.remove('oculto');
        
        document.getElementById('imagenes-total').textContent = datos.imagenes;
        document.getElementById('imagenes-procesadas').textContent = '0';
        document.getElementById('progreso-porcentaje').textContent = '0%';
        document.getElementById('barra-progreso-fill').style.width = '0%';
        
        this.log(`🚀 Iniciando procesamiento: ${datos.imagenes} imágenes, ${datos.filtros.length} filtros, modo: ${datos.modo}`, 'info');
        
        // Ocultar resultados anteriores
        document.getElementById('panel-resultados').classList.add('oculto');
    }
    
    actualizarProgreso(info) {
        // Actualizar estadísticas
        document.getElementById('imagenes-procesadas').textContent = info.procesadas;
        document.getElementById('progreso-porcentaje').textContent = `${info.porcentaje}%`;
        document.getElementById('barra-progreso-fill').style.width = `${info.porcentaje}%`;
        document.getElementById('tiempo-transcurrido').textContent = `${info.tiempo_transcurrido}s`;
        
        // Calcular velocidad
        if (info.tiempo_transcurrido > 0) {
            const velocidad = (info.procesadas / info.tiempo_transcurrido).toFixed(2);
            document.getElementById('velocidad').textContent = velocidad;
        }
        
        // Actualizar texto de progreso
        const estados = {
            'procesando': '⏳',
            'completado': '✅',
            'error': '❌'
        };
        
        const emoji = estados[info.estado] || '📁';
        document.getElementById('progreso-texto').textContent = `${emoji} ${info.imagen}`;
        
        // Log del progreso
        const clase = info.estado === 'completado' ? 'success' : (info.estado === 'error' ? 'error' : 'info');
        this.log(`[${info.porcentaje.toFixed(1)}%] ${info.imagen} - ${info.mensaje}`, clase);
        
        // Enviar datos al worker para análisis
        if (this.worker) {
            this.worker.postMessage({
                tipo: 'actualizar_stats',
                datos: info
            });
        }
    }
    
    finalizarProcesamiento(datos) {
        this.procesando = false;
        this.actualizarBotones();
        
        this.log('🎉 Procesamiento completado exitosamente', 'success');
        
        // Mostrar resultados
        this.mostrarResultados(datos.resultados);
        
        // Actualizar barra a 100%
        document.getElementById('progreso-porcentaje').textContent = '100%';
        document.getElementById('barra-progreso-fill').style.width = '100%';
        document.getElementById('progreso-texto').textContent = '✅ Procesamiento completado';
    }
    
    mostrarResultados(resultados) {
        const panel = document.getElementById('panel-resultados');
        const content = document.getElementById('resultados-content');
        
        panel.classList.remove('oculto');
        content.innerHTML = '';
        
        resultados.forEach(resultado => {
            const div = document.createElement('div');
            div.className = 'resultado-item fade-in';
            
            const tiempoPorImagen = (resultado.tiempo_total / resultado.exitosas).toFixed(2);
            
            div.innerHTML = `
                <h3>🎨 ${resultado.filtro.toUpperCase()}</h3>
                <div class="resultado-stats">
                    <div class="stat-row">
                        <span>⏱️ Tiempo Total:</span>
                        <strong>${resultado.tiempo_total.toFixed(2)}s</strong>
                    </div>
                    <div class="stat-row">
                        <span>✅ Exitosas:</span>
                        <strong>${resultado.exitosas}</strong>
                    </div>
                    <div class="stat-row">
                        <span>❌ Fallidas:</span>
                        <strong>${resultado.fallidas}</strong>
                    </div>
                    <div class="stat-row">
                        <span>⚡ Tiempo/Imagen:</span>
                        <strong>${tiempoPorImagen}s</strong>
                    </div>
                    <div class="stat-row">
                        <span>🖥️ Núcleos Usados:</span>
                        <strong>${resultado.nucleos_usados}</strong>
                    </div>
                </div>
            `;
            
            content.appendChild(div);
        });
        
        // Scroll suave al panel de resultados
        panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    
    // ==================== UI - CONTROLES ====================
    
    actualizarEstadoConexion(conectado) {
        const elemento = document.getElementById('conexion-estado');
        elemento.textContent = conectado ? '● Conectado' : '● Desconectado';
        elemento.className = `estado ${conectado ? 'conectado' : 'desconectado'}`;
        
        this.actualizarBotones();
    }
    
    actualizarBotones() {
        const btnProcesar = document.getElementById('btn-procesar');
        const btnCancelar = document.getElementById('btn-cancelar');
        
        const hayImagenes = document.querySelectorAll('.imagen-item').length > 0;
        const hayFiltros = this.filtrosSeleccionados.size > 0;
        
        btnProcesar.disabled = !this.conectado || this.procesando || !hayImagenes || !hayFiltros;
        btnCancelar.disabled = !this.procesando;
    }
    
    // ==================== EVENTOS ====================
    
    inicializarEventos() {
        // Botón procesar
        document.getElementById('btn-procesar').addEventListener('click', () => {
            this.iniciarProcesamiento();
        });
        
        // Botón cancelar
        document.getElementById('btn-cancelar').addEventListener('click', () => {
            this.enviarComando({ tipo: 'cancelar' });
        });
        
        // Actualizar imágenes
        document.getElementById('btn-actualizar-imagenes').addEventListener('click', () => {
            this.solicitarImagenes();
        });
        
        // Seleccionar/deseleccionar todos los filtros
        document.getElementById('btn-seleccionar-todos').addEventListener('click', () => {
            document.querySelectorAll('.filtro-item input').forEach(checkbox => {
                checkbox.checked = true;
                const filtro = checkbox.closest('.filtro-item').dataset.filtro;
                this.filtrosSeleccionados.add(filtro);
                checkbox.closest('.filtro-item').classList.add('seleccionado');
            });
            this.actualizarBotones();
        });
        
        document.getElementById('btn-deseleccionar-todos').addEventListener('click', () => {
            document.querySelectorAll('.filtro-item input').forEach(checkbox => {
                checkbox.checked = false;
                checkbox.closest('.filtro-item').classList.remove('seleccionado');
            });
            this.filtrosSeleccionados.clear();
            this.actualizarBotones();
        });
        
        // Limpiar log
        document.getElementById('btn-limpiar-log').addEventListener('click', () => {
            document.getElementById('log-content').innerHTML = '';
        });
    }
    
    // ==================== WEB WORKER ====================
    
    inicializarWorker() {
        try {
            this.worker = new Worker('workers/monitor.js');
            
            this.worker.onmessage = (e) => {
                if (e.data.tipo === 'stats') {
                    // Actualizar información de núcleos si está disponible
                    if (e.data.nucleos) {
                        document.getElementById('nucleos-info').textContent = `🖥️ Núcleos: ${e.data.nucleos}`;
                    }
                }
            };
            
            this.log('✅ Worker inicializado para monitorización', 'info');
        } catch (error) {
            this.log('⚠️ No se pudo inicializar el worker', 'warning');
        }
    }
    
    // ==================== UTILIDADES ====================
    
    log(mensaje, tipo = 'info') {
        const logContent = document.getElementById('log-content');
        const logItem = document.createElement('p');
        logItem.className = `log-item ${tipo}`;
        
        const timestamp = new Date().toLocaleTimeString();
        logItem.textContent = `[${timestamp}] ${mensaje}`;
        
        logContent.appendChild(logItem);
        logContent.scrollTop = logContent.scrollHeight;
        
        // Limitar número de logs
        if (logContent.children.length > 100) {
            logContent.removeChild(logContent.firstChild);
        }
    }
}

// Inicializar aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.app = new AplicacionProcesadorImagenes();
});
```

`workers/monitor.js`:
```js
let estadisticas = {
    totalProcesadas: 0,
    tiempoTotal: 0,
    velocidadPromedio: 0,
    nucleos: navigator.hardwareConcurrency || 'Desconocido'
};

// Historial de procesamiento
let historial = [];

// Escuchar mensajes del hilo principal
self.onmessage = function(e) {
    const { tipo, datos } = e.data;
    
    switch (tipo) {
        case 'iniciar':
            inicializarMonitoreo();
            break;
            
        case 'actualizar_stats':
            actualizarEstadisticas(datos);
            break;
            
        case 'calcular_metricas':
            calcularMetricas();
            break;
            
        case 'obtener_nucleos':
            obtenerInfoSistema();
            break;
            
        default:
            console.log('Worker: Comando desconocido', tipo);
    }
};
function inicializarMonitoreo() {
    console.log('Worker: Iniciando monitoreo');
    
    // Obtener información del sistema
    obtenerInfoSistema();
    
    // Enviar confirmación
    self.postMessage({
        tipo: 'inicializado',
        mensaje: 'Worker de monitorización activo',
        nucleos: estadisticas.nucleos
    });
    
    // Enviar actualizaciones periódicas de stats
    setInterval(() => {
        self.postMessage({
            tipo: 'stats',
            nucleos: estadisticas.nucleos
        });
    }, 5000);
}
function obtenerInfoSistema() {
    const info = {
        nucleos: navigator.hardwareConcurrency || 'Desconocido',
        memoria: navigator.deviceMemory || 'Desconocido',
        plataforma: navigator.platform || 'Desconocido',
        userAgent: navigator.userAgent
    };
    
    estadisticas.nucleos = info.nucleos;
    
    self.postMessage({
        tipo: 'info_sistema',
        datos: info
    });
}
function actualizarEstadisticas(datos) {
    estadisticas.totalProcesadas = datos.procesadas;
    estadisticas.tiempoTotal = datos.tiempo_transcurrido;
    
    if (datos.tiempo_transcurrido > 0) {
        estadisticas.velocidadPromedio = datos.procesadas / datos.tiempo_transcurrido;
    }
    
    // Agregar al historial
    historial.push({
        timestamp: Date.now(),
        procesadas: datos.procesadas,
        tiempo: datos.tiempo_transcurrido,
        porcentaje: datos.porcentaje,
        estado: datos.estado
    });
    
    // Limitar tamaño del historial
    if (historial.length > 1000) {
        historial.shift();
    }
    
    // Calcular tendencias si hay suficientes datos
    if (historial.length > 5) {
        calcularTendencias();
    }
}
function calcularTendencias() {
    const ultimos10 = historial.slice(-10);
    
    // Calcular velocidad promedio de los últimos 10 registros
    let velocidadAcumulada = 0;
    let contador = 0;
    
    for (let i = 1; i < ultimos10.length; i++) {
        const anterior = ultimos10[i - 1];
        const actual = ultimos10[i];
        
        const deltaImagenes = actual.procesadas - anterior.procesadas;
        const deltaTiempo = actual.tiempo - anterior.tiempo;
        
        if (deltaTiempo > 0) {
            velocidadAcumulada += deltaImagenes / deltaTiempo;
            contador++;
        }
    }
    
    if (contador > 0) {
        const velocidadReciente = velocidadAcumulada / contador;
        
        self.postMessage({
            tipo: 'tendencia',
            datos: {
                velocidad_reciente: velocidadReciente.toFixed(2),
                velocidad_promedio: estadisticas.velocidadPromedio.toFixed(2)
            }
        });
    }
}
function calcularMetricas() {
    if (historial.length < 2) {
        return;
    }
    
    // Calcular tiempo estimado de finalización
    const ultimoRegistro = historial[historial.length - 1];
    const porcentajeRestante = 100 - ultimoRegistro.porcentaje;
    
    let tiempoEstimado = 0;
    if (estadisticas.velocidadPromedio > 0 && porcentajeRestante > 0) {
        const imagenesRestantes = (ultimoRegistro.procesadas / ultimoRegistro.porcentaje) * porcentajeRestante;
        tiempoEstimado = imagenesRestantes / estadisticas.velocidadPromedio;
    }
    
    // Calcular eficiencia (imágenes por segundo por núcleo)
    const eficiencia = estadisticas.velocidadPromedio / estadisticas.nucleos;
    
    self.postMessage({
        tipo: 'metricas',
        datos: {
            tiempo_estimado: Math.round(tiempoEstimado),
            eficiencia_por_nucleo: eficiencia.toFixed(3),
            imagenes_por_segundo: estadisticas.velocidadPromedio.toFixed(2),
            registros_historial: historial.length
        }
    });
}

function realizarBenchmark() {
    const inicio = performance.now();
    
    // Operación intensiva de prueba
    let resultado = 0;
    for (let i = 0; i < 1000000; i++) {
        resultado += Math.sqrt(i);
    }
    
    const fin = performance.now();
    const tiempo = fin - inicio;
    
    self.postMessage({
        tipo: 'benchmark',
        datos: {
            tiempo_ms: tiempo.toFixed(2),
            operaciones_por_segundo: (1000000 / (tiempo / 1000)).toFixed(0)
        }
    });
}

function limpiarHistorial() {
    historial = [];
    estadisticas = {
        totalProcesadas: 0,
        tiempoTotal: 0,
        velocidadPromedio: 0,
        nucleos: navigator.hardwareConcurrency || 'Desconocido'
    };
    
    self.postMessage({
        tipo: 'historial_limpiado',
        mensaje: 'Historial reiniciado'
    });
}
// Inicialización automática
console.log('Worker de monitorización cargado');
inicializarMonitoreo();
```

#### Errores comunes y cómo evitarlos
- **GIL y elección de estrategia:** para CPU‑bound usar **procesos** (`ProcessPoolExecutor`), no solo hilos. El proyecto ya lo implementa y compara.  
- **Cuellos de botella en disco:** evitar guardar en el mismo HDD saturado; si es posible, **SSD** o separar lectura/escritura.  
- **Tamaño de lote sobredimensionado:** no crear más procesos que núcleos de forma indiscriminada; el componente usa `multiprocessing.cpu_count()` como base.  
- **Faltan dependencias:** instalar Pillow y websockets; organizar virtualenv.  
- **Imágenes corruptas o formatos no soportados:** el código maneja excepciones en `aplicar_filtro(...)` y contabiliza fallos sin detener el lote.  
- **Bloqueo de bucle de eventos:** el servidor WebSocket crea **loops dedicados** al emitir desde threads (ver `callback_async`), evitando deadlocks.

---

He construido un **pipeline paralelo** de procesos de imágenes que aprovecha **múltiples núcleos**, en el que he elegido **procesos** para cargas `CPU-bound` y **threads** para escenarios mas I/O-bound.
También he integrado **monitorización en tiempo real** gracias a WebSockets y una **UI** que permite operar sin la necesidad de la consola.
Este ejercicio me a ayudado a ser más `consciente` a la hora de mejorar el rendimiento con multiples procesos, y la mejora que proporciona el trabajar con **aplicación multinúcleo** que reparten el trabajo de **procesamientos** entre varios hilos y/o procesos del sistema.