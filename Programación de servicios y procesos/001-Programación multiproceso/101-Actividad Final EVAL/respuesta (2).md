En este proyecto desarrollo una **aplicación multinúcleo** que reparte el trabajo de **procesamiento de imágenes** entre varios hilos y/o procesos del sistema. La idea es paralelizar tareas **CPU‑bound** (aplicación de filtros con Pillow) para **acelerar el tiempo total de ejecución** y ofrecer **feedback en tiempo real** mediante WebSockets a un frontend web.

**¿Para qué sirve y en qué contexto se usa?**  
- **Caso de uso profesional:** técnicos de marketing, fotógrafos, diseñadores o equipos de soporte que necesitan **lotes de transformaciones** (blur, escala de grises, posterizar, marca de agua, etc.) sobre **carpetas enteras** de imágenes.  
- **Entorno:** backend Python con `multiprocessing`/`concurrent.futures`, **servidor WebSocket** para eventos de progreso y **frontend** en HTML/CSS/JS para monitorización y control.

**Evidencias en el proyecto:**  
- Backend: `backend/procesador.py`, `backend/filtros.py`, `backend/servidor_websocket.py`  
- Frontend: `frontend/index.html`, `frontend/app.js`, `frontend/styles.css`, `frontend/workers/monitor.js`  
- Generación de dataset de prueba: `generar_imagenes_prueba.py`  
- Datasets de entrada/salida: `input_images/` y `output_images/`

---

### Definiciones y terminología del temario
- **CPU‑bound vs I/O‑bound:** El filtrado de imágenes es **CPU‑bound** → se beneficia de **procesos** paralelos (aislamiento de GIL en CPython) más que de hilos. Para operaciones con mucha E/S, los **threads** pueden ser suficientes.  
- **Escalabilidad horizontal en cliente:** el frontend delega procesamiento a backend y muestra métricas en tiempo real vía **WebSockets**.  
- **Granularidad de tareas:** una **imagen = unidad de trabajo**, ideal para repartir en un **pool de procesos**.

### Funcionamiento (paso a paso)
1. **Selección del modo y filtros en el frontend** (`frontend/index.html` + `frontend/app.js`).  
2. **Comando vía WebSocket** al servidor (`backend/servidor_websocket.py` → `comando_procesar`).  
3. **Orquestación del batch** en `ProcesadorImagenes.procesar_batch(...)` (archivo `backend/procesador.py`):  
   - Divide el lote de imágenes.  
   - Por cada filtro elegido, lanza **`ProcessPoolExecutor`** (modo recomendado para CPU) o **`ThreadPoolExecutor`**.  
   - Cada tarea invoca `aplicar_filtro(...)` de `backend/filtros.py`.  
4. **Progreso en tiempo real:** el backend emite eventos (callback) y el **frontend** actualiza la barra y las estadísticas.  
5. **Resultados y métricas:** el backend devuelve estadísticas (tiempo total, éxitos/fallos, tiempo medio por imagen), y el frontend las presenta con estilo.

### Código del proyecto (fragmentos representativos)

**Procesamiento paralelo con procesos** (presente en `backend/procesador.py`, bloque `__main__`):  
```python
DIR_ENTRADA = "../input_images"
DIR_SALIDA = "../output_images"

procesador = ProcesadorImagenes(callback_progreso=callback_ejemplo)
imagenes = obtener_imagenes_directorio(DIR_ENTRADA)

stats = procesador.procesar_con_procesos(imagenes, 'blur', DIR_SALIDA)
```

**Aplicación de un filtro** (función existente en `backend/filtros.py`):  
```python
def aplicar_filtro(ruta_entrada, ruta_salida, nombre_filtro, parametros=None):
    imagen = Image.open(ruta_entrada)
    filtros = FiltrosImagen.obtener_filtros_disponibles()
    filtro = filtros[nombre_filtro]
    imagen_procesada = filtro(imagen.copy(), **parametros) if parametros else filtro(imagen.copy())
    imagen_procesada.save(ruta_salida)
    return True
```

**Listado de filtros disponibles** (extraído de `backend/filtros.py`):  
- `invertir`, `grises`, `blur`, `nitidez`, `brillo`, `contraste`, `sepia`, `bordes`, `relieve`, `posterizar`, `redimensionar`, `marca_agua`.

**Canal de tiempo real (WebSocket)** (`backend/servidor_websocket.py` → difunde progreso):  
```python
await self.broadcast({
    'tipo': 'progreso',
    'datos': info
})
```

### Ejemplos reales incluidos en el repo
- **Generación de imágenes de prueba:** `generar_imagenes_prueba.py` crea gradientes, geométricas y patrones en `input_images/`.  
- **UI de control:** en el **frontend** se seleccionan filtros y modo (threads/procesos), se inicia el lote y se visualiza el avance (porcentaje, img/s, núcleos).

---

**Cómo se aplica en la práctica (flujo real):**
1. **Preparar lote**: colocar imágenes en `input_images/` (puedo generarlas con `generar_imagenes_prueba.py`).  
2. **Levantar backend**: `python backend/servidor_websocket.py`.  
3. **Abrir interfaz**: `frontend/index.html`. Marcar filtros (p. ej., `grises`, `sepia`, `invertir`) y **modo “procesos”**.  
4. **Iniciar**: el servidor reparte imágenes a procesos, aplica filtros y envía **progreso en tiempo real** (velocidad, % y tiempo).  
5. **Consumo profesional**: resultados organizados por filtro en `output_images/<filtro>/...`, listos para campañas o catálogos.

**Ejemplo claro:**
```python
# backend/procesador.py (uso real)
resultados = procesador.procesar_batch(imagenes[:3], ['grises', 'sepia', 'invertir'], DIR_SALIDA)
```
> El frontend muestra para cada filtro: tiempo total, éxitos/fallos, tiempo/imagen y núcleos usados.

**Errores comunes y cómo evitarlos**
- **GIL y elección de estrategia:** para CPU‑bound usar **procesos** (`ProcessPoolExecutor`), no solo hilos. El proyecto ya lo implementa y compara.  
- **Cuellos de botella en disco:** evitar guardar en el mismo HDD saturado; si es posible, **SSD** o separar lectura/escritura.  
- **Tamaño de lote sobredimensionado:** no crear más procesos que núcleos de forma indiscriminada; el componente usa `multiprocessing.cpu_count()` como base.  
- **Faltan dependencias:** instalar Pillow y websockets; organizar virtualenv.  
- **Imágenes corruptas o formatos no soportados:** el código maneja excepciones en `aplicar_filtro(...)` y contabiliza fallos sin detener el lote.  
- **Bloqueo de bucle de eventos:** el servidor WebSocket crea **loops dedicados** al emitir desde threads (ver `callback_async`), evitando deadlocks.

---

**Resumen de puntos clave.**  
- He construido un **pipeline paralelo** de procesado de imágenes que aprovecha **múltiples núcleos**.  
- Elijo **procesos** para cargas **CPU‑bound** y **threads** para escenarios más I/O‑bound.  
- Integro **monitorización en tiempo real** vía WebSockets y una **UI** que permite operar sin consola.

**Conexión con contenidos de la unidad.**  
- Relaciono **multiproceso, pools y granularidad de tareas** con la mejora de rendimiento real.  
- Practico **comunicación asíncrona** (WebSockets) para desacoplar cómputo y visualización.  
- Aplico **medición y reporte de métricas** (tiempo total, img/s, núcleos, fallos) para justificar la ganancia obtenida.
