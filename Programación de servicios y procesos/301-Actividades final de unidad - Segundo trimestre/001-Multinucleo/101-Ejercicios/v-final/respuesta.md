El **procesamiento multinúcleo** es una técnica de programación que consiste en distribuir la carga de trabajo de un programa entre varios núcleos físicos del procesador, ejecutando múltiples procesos de forma simultánea. A diferencia de la programación secuencial, donde las tareas se encolan y se ejecutan de una en una en un solo núcleo, el procesamiento multinúcleo aprovecha el paralelismo real del hardware moderno para reducir los tiempos de cómputo de forma significativa.

Este concepto se enmarca dentro de la **programación multiproceso**, unidad que hemos estudiado en el módulo de *Programación de Servicios y Procesos*. Cuando un proceso necesita realizar operaciones costosas —como el análisis de grandes conjuntos de archivos, el procesamiento de imágenes o los cálculos matemáticos intensivos— la estrategia multiproceso permite partir ese trabajo en fragmentos independientes y repartirlos entre todos los núcleos disponibles del sistema.

En Python, el módulo de la biblioteca estándar encargado de esto es `multiprocessing`, que sortea la limitación del **GIL** (*Global Interpreter Lock*) creando procesos independientes en lugar de hilos dentro del mismo proceso. Esto lo hace especialmente adecuado para tareas **CPU-bound** (vinculadas al procesador), en contraposición a las tareas **I/O-bound** donde el módulo `threading` o `asyncio` suelen ser más apropiados.

---

### Conceptos clave

| Término | Definición |
|---|---|
| **Proceso** | Instancia de un programa en ejecución, con su propio espacio de memoria, PID y recursos del S.O. |
| **Multiproceso** | Técnica que lanza varios procesos independientes para ejecutarlos en paralelo. |
| **Pool de procesos** | Conjunto de *workers* (trabajadores) que se crean una sola vez y reutilizan para procesar tareas, evitando el coste de creación/destrucción repetida. |
| **Speedup** | Cociente entre el tiempo secuencial y el tiempo paralelo. Mide la ganancia de rendimiento obtenida. $S = T_{sec} / T_{par}$ |
| **Eficiencia** | Indica qué fracción del potencial máximo se aprovecha. $E = S / N_{núcleos}$ |
| **CPU-bound** | Tarea cuyo cuello de botella es el procesador (muchos cálculos). Ideal para multiprocessing. |
| **I/O-bound** | Tarea cuyo cuello de botella es la entrada/salida (red, disco). Mejor con asyncio o threading. |
| **GIL** | Mecanismo interno de CPython que impide que dos hilos ejecuten bytecode Python a la vez. No afecta a `multiprocessing` porque cada proceso tiene su propio intérprete. |

### El módulo `multiprocessing` en Python

La clase principal que he utilizado es `multiprocessing.Pool`, que implementa el patrón **master-worker**:

1. El proceso principal (**master**) crea un `Pool` con tantos *workers* como núcleos tenga la máquina (`cpu_count()`).  
2. El master distribuye la lista de tareas mediante `pool.map()` o `pool.starmap()`.  
3. Cada *worker* ejecuta su tarea de forma independiente en un núcleo distinto.  
4. Al terminar, los resultados se recogen automáticamente en el proceso principal, manteniendo el orden original de entrada.

```
Proceso Principal (master)
        │
        ├──► Worker 1 (núcleo 0) → tarea A
        ├──► Worker 2 (núcleo 1) → tarea B
        ├──► Worker 3 (núcleo 2) → tarea C
        └──► Worker 4 (núcleo 3) → tarea D
        │
   (pool.map espera)
        │
   [resultado A, B, C, D]
```

### Funcionamiento paso a paso de `Pool.map()`

1. **Creación del pool:** `with multiprocessing.Pool(processes=N) as pool:` — se levantan N subprocesos en segundo plano.  
2. **Serialización (*pickling*):** los argumentos enviados a cada worker se serializan con `pickle` para poder cruzar la barrera de memoria entre procesos.  
3. **Distribución:** el pool reparte automáticamente los elementos de la lista de entrada entre los workers disponibles.  
4. **Ejecución paralela:** cada worker ejecuta la función objetivo de forma simultánea en su núcleo asignado por el sistema operativo.  
5. **Recolección:** los valores de retorno se deserializan y se devuelven en el mismo orden en que se enviaron.  
6. **Cierre:** al salir del bloque `with`, el pool llama a `terminate()` y libera los recursos.

### Integración con `asyncio` y `concurrent.futures`

En la Versión 4 del proyecto introduje el `ProcessPoolExecutor` de `concurrent.futures`, que permite integrar el paralelismo de procesos con el bucle de eventos de `asyncio`:

```python
loop = asyncio.get_event_loop()
with ProcessPoolExecutor(max_workers=num_workers) as executor:
    futures = [loop.run_in_executor(executor, procesar_imagen_wrapper, args)
               for args in lista_tareas]
    resultados = await asyncio.gather(*futures)
```

Esto es importante porque el servidor WebSocket es asíncrono (necesita atender múltiples clientes simultáneamente con `asyncio`), pero el procesamiento de imágenes es intensivo en CPU, por lo que no puede bloquearse en el hilo del bucle de eventos. La solución es delegar el trabajo pesado a procesos reales mediante `run_in_executor`, obteniendo lo mejor de ambos mundos: concurrencia asíncrona para las conexiones y paralelismo real para el cómputo.

---

### Cómo lo he aplicado en el proyecto

He estructurado el proyecto en cuatro versiones progresivas, cada una añadiendo una capa de complejidad:

**Versión 1 — Cálculo numérico:**  
La tarea más sencilla para medir el speedup puro. Calculamos números primos y divisores para rangos grandes, distribuyendo los rangos entre los workers.

**Versión 2 — Análisis de archivos de texto:**  
Cada worker recibe un archivo `.txt` de `datos_ejemplo/` y devuelve sus estadísticas (palabras, líneas, caracteres, palabras más frecuentes). Aquí el paralelismo también ayuda con I/O porque la lectura y el análisis regex se hacen simultáneamente.

```python
# paralelo.py — fragmento real del proyecto
def procesar_archivos_paralelo(lista_archivos, num_procesos=None):
    if num_procesos is None:
        num_procesos = multiprocessing.cpu_count()

    with multiprocessing.Pool(processes=num_procesos) as pool:
        resultados = pool.map(analizar_archivo, lista_archivos)

    return resultados
```

**Versión 3 — Procesamiento de imágenes con Pillow:**  
Cada imagen en `imagenes_entrada/` se procesa de forma independiente aplicando filtros encadenados (`GaussianBlur`, `SHARPEN`, `FIND_EDGES`, escala de grises) y redimensionamiento. En mis pruebas con 12 núcleos obtuve un **speedup de ~4.4x** y una reducción del tiempo del **77.5%**.

```python
# version3_paralelo.py — envío de tareas al pool
args_lista = [
    (ruta_entrada, ruta_salida, operaciones)
    for ruta_entrada, ruta_salida in pares_imagenes
]
with multiprocessing.Pool(processes=num_procesos) as pool:
    resultados = pool.map(procesar_imagen_wrapper, args_lista)
```

> **¿Por qué un wrapper?** `pool.map()` solo acepta una función con un único argumento. El wrapper desempaqueta la tupla `(ruta_entrada, ruta_salida, operaciones)` y llama a la función real. Es el patrón habitual cuando la función tiene múltiples parámetros.

**Versión 4 — Dashboard web en tiempo real:**  
Un servidor WebSocket (`servidor.py`) expone el procesamiento a un frontend HTML/JS (`frontend/`). Combina `asyncio` para gestionar varias conexiones simultáneas y `ProcessPoolExecutor` para el cómputo paralelo. El cliente recibe actualizaciones en tiempo real: porcentaje de progreso, uso de cada núcleo (via `psutil`), RAM consumida y log de eventos.

### Resultados medidos

| Versión | Tareas | Tiempo sec. | Tiempo par. | Speedup | Eficiencia |
|---|---|---|---|---|---|
| V1 (números) | Rangos grandes | ~8.2 s | ~1.9 s | ~4.4x | ~37% |
| V2 (archivos) | 5 archivos .txt | ~0.6 s | ~0.3 s | ~2.0x | ~17% |
| V3 (imágenes) | 10 imágenes | ~12.4 s | ~2.8 s | ~4.4x | ~37% |

La eficiencia no llega al 100% porque existe un **overhead** inherente al paralelismo: serialización con `pickle`, creación inicial del pool, comunicación entre procesos y coste de sincronización al unir resultados. Este overhead domina en tareas pequeñas (como V2 con pocos archivos) y se amortiza en tareas grandes (V1 y V3).

### Errores comunes y cómo evitarlos

| Error | Causa | Solución |
|---|---|---|
| `RuntimeError: freeze_support()` en Windows | Falta del bloque `if __name__ == '__main__':` en el script principal | Envolver siempre el código que lanza el pool en dicho bloque. |
| `AttributeError: Can't pickle local object` | Intentar pasar a un worker una función definida dentro de otra función o una lambda | Definir la función en el nivel del módulo (nunca como función anidada o lambda). |
| Speedup peor que secuencial | Usar multiprocessing para tareas demasiado pequeñas | Asegurarse de que el coste de cada tarea supera ampliamente el overhead de pickle y creación de procesos. |
| Errores silenciosos en workers | Las excepciones en workers no siempre se propagan al master | Capturar excepciones dentro de la función del worker y devolverlas como parte del resultado (campo `'exito': False`). |
| Consumo excesivo de RAM | `Pool` con demasiados workers para el hardware disponible | Limitar el número de workers o usar `chunksize` en `pool.map()`. |

---

A lo largo de este proyecto he comprobado de primera mano que el procesamiento multinúcleo, implementado con el módulo `multiprocessing` de Python, es una herramienta poderosa para acelerar tareas intensivas en CPU. El patrón `Pool + map()` resulta elegante, seguro y fácil de razonar: separas la lógica de cada tarea (función del worker) de la estrategia de distribución (el pool), lo que hace el código limpio y mantenible.

Los conceptos aplicados en este proyecto conectan directamente con varios contenidos de la unidad:

- **Programación multiproceso (UD1):** procesos independientes, PID, estados (*running*, *waiting*, *terminated*) y la diferencia entre paralelismo real y concurrencia.
- **Programación multihilo (UD2):** entendí mejor la diferencia entre hilos y procesos al constatar que `threading` no supera el GIL para tareas CPU-bound, mientras que `multiprocessing` sí lo hace.
- **Comunicaciones en red / Servicios web (UD3 y UD4):** la Versión 4 integra un servidor WebSocket asíncrono que sirve datos en tiempo real al cliente web, aplicando directamente los conceptos de cliente-servidor, sockets y protocolos de comunicación.
- **Programación segura (UD5):** al gestionar múltiples procesos y conexiones simultáneas es necesario ser cuidadoso con las condiciones de carrera y el acceso a recursos compartidos, protegiendo el estado del servidor con `asyncio.Lock`.

En definitiva, el procesamiento multinúcleo no es un concepto aislado, sino la intersección práctica de la gestión de procesos, la concurrencia, las comunicaciones y la optimización del rendimiento: pilares fundamentales del módulo.