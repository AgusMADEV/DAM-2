He desarrollado **SysWatch**, un sistema profesional de monitorización de recursos del servidor en tiempo real. Este proyecto surge como una evolución personal del ejercicio sobre el panel de control del servidor Ollama trabajado en clase, pero extendiendo su funcionalidad para monitorizar **todos los recursos del sistema** (CPU por núcleo, memoria RAM, disco I/O y red), en lugar de limitarse a un único servicio.

SysWatch integra los conceptos fundamentales de las cuatro unidades del segundo trimestre: **programación multiproceso** (uso de `multiprocessing.Pool` y Web Workers), **programación multihilo** (hilos demonios, locks y eventos), **comunicaciones en red** (WebSockets bidireccionales) y **servicios en red** (servidor REST con Flask). El sistema recolecta métricas cada 2 segundos, las almacena en una base de datos SQLite con múltiples granularidades (datos raw y agregados horarios), y las muestra en un dashboard web interactivo que se actualiza en tiempo real mediante WebSockets.

Este tipo de herramientas son esenciales en entornos de producción para detectar cuellos de botella, prevenir caídas del sistema mediante alertas tempranas, y mantener un histórico de rendimiento que permita analizar tendencias y planificar escalado de recursos.

---

### Arquitectura del sistema

La arquitectura de SysWatch sigue un patrón cliente-servidor con tres componentes principales:

1. **Backend Python**: Hilo de monitorización + servidor HTTP/WebSocket + base de datos SQLite
2. **Frontend Web**: Dashboard HTML/CSS/JavaScript con Chart.js y Socket.IO
3. **Comunicación en tiempo real**: WebSockets para streaming de métricas y REST para consultas históricas

El punto de entrada es [main.py](301-Actividades%20final%20de%20unidad%20-%20Segundo%20trimestre/003-Monitorización%20de%20recursos/101-Ejercicios/main.py), que arranca tres componentes concurrentes:

```python
# 1. Hilo demonio de monitorización (Unidad 2 - Multihilo)
monitor = MonitorSistema(intervalo=args.intervalo)
monitor.suscribir(on_nueva_metrica)   # Conecta monitor → servidor
monitor.start()

# 2. Hilo de limpieza periódica de la BD
hilo_limpieza = threading.Thread(
    target=_tarea_limpieza_periodica,
    args=(24,),
    daemon=True,
    name="LimpiezaBD"
)
hilo_limpieza.start()

# 3. Iniciar servidor Flask-SocketIO (bloquea el hilo principal)
iniciar_servidor(host="0.0.0.0", puerto=args.puerto, debug=args.debug)
```

### Programación Multihilo (Unidad 2)

El núcleo del sistema es la clase `MonitorSistema` en [monitor.py](301-Actividades%20final%20de%20unidad%20-%20Segundo%20trimestre/003-Monitorización%20de%20recursos/101-Ejercicios/backend/monitor.py#L93-L311), que hereda de `threading.Thread` y se ejecuta como **hilo demonio** en segundo plano:

```python
class MonitorSistema(threading.Thread):
    """
    Hilo demonio que recoge métricas del sistema de forma periódica.
    """
    
    def __init__(self, intervalo: float = 2.0, umbrales: dict | None = None):
        super().__init__(daemon=True, name="MonitorSistema")
        self.intervalo  = intervalo
        self.umbrales   = {**self.UMBRALES_DEFAULT, **(umbrales or {})}
        
        # Lista de callbacks para distribuir métricas
        self._callbacks: list = []
        self._lock_callbacks = threading.Lock()
        
        # Señal de parada
        self._stop_event = threading.Event()
```

He implementado **tres mecanismos de sincronización** que evitan condiciones de carrera (race conditions):

1. **`threading.Lock`** para proteger las listas compartidas:
   - `_lock_callbacks`: sincroniza acceso a la lista de suscriptores desde múltiples hilos
   - `_lock_clientes` en [servidor.py](301-Actividades%20final%20de%20unidad%20-%20Segundo%20trimestre/003-Monitorización%20de%20recursos/101-Ejercicios/backend/servidor.py#L34): protege el contador de clientes conectados
   - `_lock_ultima` en [servidor.py](301-Actividades%20final%20de%20unidad%20-%20Segundo%20trimestre/003-Monitorización%20de%20recursos/101-Ejercicios/backend/servidor.py#L39): guarda la última métrica para nuevos clientes

2. **`threading.Event`** para coordinación de parada:
   ```python
   def detener(self) -> None:
       """Señaliza el hilo para que se detenga limpiamente."""
       self._stop_event.set()
   
   def run(self) -> None:
       while not self._stop_event.is_set():
           # ... recolección de métricas ...
           self._stop_event.wait(timeout=sleep_time)
   ```

3. **Patrón Observer con callbacks thread-safe**:
   ```python
   def suscribir(self, callback) -> None:
       """Añade una función callback que recibirá cada muestra nueva."""
       with self._lock_callbacks:
           if callback not in self._callbacks:
               self._callbacks.append(callback)
   
   # En el bucle principal:
   with self._lock_callbacks:
       callbacks_actuales = list(self._callbacks)
   
   for cb in callbacks_actuales:
       try:
           cb(metricas)
       except Exception as e:
           print(f"[MonitorSistema] Error en callback: {e}")
   ```

Este patrón es crucial porque el hilo `MonitorSistema` ejecuta los callbacks en su propio contexto, y estos modifican estructuras compartidas con el hilo del servidor Flask-SocketIO.

### Programación Multiproceso (Unidad 1)

He aplicado **procesamiento paralelo** en dos niveles:

#### Backend Python - `multiprocessing.Pool`

Cuando el usuario solicita estadísticas históricas, el cálculo se distribuye entre múltiples procesos para aprovechar **todos los núcleos de la CPU**:

```python
def calcular_estadisticas_paralelo(datos: dict[str, list[float]]) -> dict:
    """
    Calcula estadísticas de múltiples métricas en paralelo usando
    un pool de procesos (multiprocessing.Pool).
    """
    claves = list(datos.keys())
    listas  = [datos[k] for k in claves]
    
    # Pool crea N procesos (uno por métrica) para calcular en paralelo
    with Pool(processes=min(len(claves), 4)) as pool:
        resultados = pool.map(_calcular_estadisticas_chunk, listas)
    
    return dict(zip(claves, resultados))


def _calcular_estadisticas_chunk(valores: list[float]) -> dict:
    """Se ejecuta en un proceso hijo independiente."""
    if not valores:
        return {"min": 0, "max": 0, "avg": 0, "p95": 0}
    
    ordenados = sorted(valores)
    n = len(ordenados)
    idx_p95 = int(n * 0.95)
    
    return {
        "min": round(min(ordenados), 2),
        "max": round(max(ordenados), 2),
        "avg": round(sum(ordenados) / n, 2),
        "p95": round(ordenados[min(idx_p95, n - 1)], 2),
    }
```

Este enfoque es similar al ejercicio de clase sobre procesamiento paralelo de imágenes: cada proceso hijo calcula estadísticas de **una métrica independiente** (CPU, RAM, Disco, Red), evitando bloqueos del Global Interpreter Lock (GIL) de Python.

#### Frontend JavaScript - Web Worker

En el navegador, he implementado un **Web Worker** en [stats_worker.js](301-Actividades%20final%20de%20unidad%20-%20Segundo%20trimestre/003-Monitorización%20de%20recursos/101-Ejercicios/frontend/workers/stats_worker.js) que ejecuta cálculos pesados en un **proceso separado del hilo principal**:

```javascript
/**
 * Web Worker que ejecuta cálculos estadísticos en segundo plano
 * SIN bloquear el hilo principal de la interfaz.
 */

function calcularStats(arr) {
  if (!arr || arr.length === 0) {
    return { min: 0, max: 0, avg: 0, p95: 0, last: 0 };
  }
  const sorted = [...arr].sort((a, b) => a - b);
  const n = sorted.length;
  const sum = sorted.reduce((s, v) => s + v, 0);
  const p95idx = Math.floor(n * 0.95);
  return {
    min:  +sorted[0].toFixed(2),
    max:  +sorted[n - 1].toFixed(2),
    avg:  +(sum / n).toFixed(2),
    p95:  +sorted[Math.min(p95idx, n - 1)].toFixed(2),
    last: +sorted[n - 1].toFixed(2),
  };
}
```

En [app.js](301-Actividades%20final%20de%20unidad%20-%20Segundo%20trimestre/003-Monitorización%20de%20recursos/101-Ejercicios/frontend/app.js#L56-L92) inicializo y comunico con el Worker:

```javascript
let worker       = null;
let workerIdSeq  = 0;
const workerCbs  = {};    // id → { resolve, reject }

function iniciarWorker() {
  try {
    worker = new Worker("workers/stats_worker.js");
    worker.onmessage = (e) => {
      const { tipo, id, resultado, mensaje } = e.data;
      if (workerCbs[id]) {
        if (tipo === "error") workerCbs[id].reject(new Error(mensaje));
        else                  workerCbs[id].resolve({ tipo, resultado });
        delete workerCbs[id];
      }
    };
    worker.onerror = (e) => console.error("[Worker] Error:", e.message);
    console.log("[Worker] Web Worker iniciado.");
  } catch (e) {
    console.warn("[Worker] No disponible:", e.message);
  }
}

function workerLlamar(tipo, payload) {
  return new Promise((resolve, reject) => {
    if (!worker) { resolve({}); return; }
    const id = ++workerIdSeq;
    workerCbs[id] = { resolve, reject };
    worker.postMessage({ tipo, payload, id });
    // Timeout de seguridad: 10 s
    setTimeout(() => {
      if (workerCbs[id]) {
        delete workerCbs[id];
        reject(new Error("Timeout Worker"));
      }
    }, 10000);
  });
}
```

### Comunicaciones en Red

He implementado **comunicación bidireccional WebSocket** usando Flask-SocketIO en el servidor y Socket.IO en el cliente.

#### Servidor WebSocket ([servidor.py](301-Actividades%20final%20de%20unidad%20-%20Segundo%20trimestre/003-Monitorización%20de%20recursos/101-Ejercicios/backend/servidor.py))

```python
from flask_socketio import SocketIO, emit, disconnect

socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

@socketio.on("connect")
def ws_conectar():
    """Cliente se conecta por WebSocket."""
    global _clientes_conectados
    with _lock_clientes:
        _clientes_conectados += 1
        total = _clientes_conectados
    
    print(f"[WS] Cliente conectado. Total: {total}")
    
    # Enviar la última métrica disponible
    with _lock_ultima:
        ultima = _ultima_metrica
    
    if ultima:
        emit("metrica", {k: v for k, v in ultima.items() if k != "procesos"} |
             {"procesos": ultima["procesos"][:5]})
    
    emit("bienvenida", {
        "mensaje": "Conectado a SysWatch",
        "clientes": total,
        "version": "1.0.0",
    })

@socketio.on("disconnect")
def ws_desconectar():
    """Cliente se desconecta."""
    global _clientes_conectados
    with _lock_clientes:
        _clientes_conectados = max(0, _clientes_conectados - 1)
    print(f"[WS] Cliente desconectado. Total: {_clientes_conectados}")

@socketio.on("solicitar_historico")
def ws_solicitar_historico(data: dict):
    """El cliente solicita datos históricos."""
    ventana = data.get("ventana", "1h")
    filas   = _obtener_historico_por_ventana(ventana)
    emit("historico", {"ventana": ventana, "datos": filas})
```

El callback `on_nueva_metrica` es crucial porque **conecta el hilo de monitorización con el servidor WebSocket**:

```python
def on_nueva_metrica(metricas: dict) -> None:
    """
    Callback invocado por MonitorSistema en cada muestra.
    1. Persiste en la base de datos.
    2. Emite el evento 'metrica' a todos los clientes Socket.IO.
    """
    global _ultima_metrica
    
    # 1. Guardar en BD
    db.insertar_metrica(metricas)
    
    # 2. Guardar alertas
    if metricas.get("alertas"):
        db.insertar_alertas(metricas["alertas"], metricas["timestamp"])
    
    # 3. Actualizar caché de última métrica
    with _lock_ultima:
        _ultima_metrica = metricas
    
    # 4. Emitir a todos los clientes conectados por WebSocket
    with _lock_clientes:
        hay_clientes = _clientes_conectados > 0
    
    if hay_clientes:
        payload = {k: v for k, v in metricas.items() if k != "procesos"}
        payload["procesos"] = metricas["procesos"][:5]
        socketio.emit("metrica", payload)
```

#### Cliente WebSocket ([app.js](301-Actividades%20final%20de%20unidad%20-%20Segundo%20trimestre/003-Monitorización%20de%20recursos/101-Ejercicios/frontend/app.js))

```javascript
let socket = null;

function conectarWebSocket() {
  socket = io(CONFIG.socketUrl, { transports: ["websocket", "polling"] });
  
  socket.on("connect", () => {
    estado.conectado = true;
    console.log("[WS] Conectado al servidor");
    mostrarToast("Conectado a SysWatch", "exito");
  });
  
  socket.on("disconnect", () => {
    estado.conectado = false;
    console.warn("[WS] Desconectado del servidor");
    mostrarToast("Conexión perdida", "error");
  });
  
  socket.on("metrica", (data) => {
    estado.ultimaMetrica = data;
    actualizarTarjetas(data);
    actualizarGraficasRT(data);
    // Procesar alertas si las hay
    if (data.alertas && data.alertas.length > 0) {
      data.alertas.forEach(a => {
        mostrarToast(`⚠️ ${a.mensaje}`, a.severidad === "critica" ? "error" : "advertencia");
      });
    }
  });
  
  socket.on("historico", async (data) => {
    estado.historico = data.datos;
    estado.ventana   = data.ventana;
    await actualizarGraficasHistoricas(data.datos);
  });
}
```

Esta arquitectura permite **comunicación simultánea con múltiples clientes** (broadcasting), cumpliendo con el concepto de la Unidad 3 - Sección 009: "Utilización de hilos para la implementación de comunicaciones simultáneas con el servidor".

### Servicios en Red

Además de WebSockets, he implementado una **REST API completa** usando Flask:

```python
@app.route("/api/historico")
def api_historico():
    """GET /api/historico?ventana=6h"""
    ventana = request.args.get("ventana", "1h")
    filas   = _obtener_historico_por_ventana(ventana)
    return jsonify({"ventana": ventana, "total": len(filas), "datos": filas})

@app.route("/api/alertas")
def api_alertas():
    """GET /api/alertas?limite=20"""
    limite  = int(request.args.get("limite", 20))
    alertas = db.obtener_alertas_recientes(limite)
    resumen = db.contar_alertas_hoy()
    return jsonify({"resumen_hoy": resumen, "datos": alertas})

@app.route("/api/estado")
def api_estado():
    """GET /api/estado"""
    stats = db.estadisticas_generales()
    with _lock_clientes:
        clientes = _clientes_conectados
    with _lock_ultima:
        ultima = _ultima_metrica
    
    return jsonify({
        "clientes_ws": clientes,
        "base_datos":  stats,
        "ultima_muestra": ultima["timestamp"] if ultima else None,
        "version": "1.0.0",
    })

@app.route("/api/mantenimiento/limpiar")
def api_limpiar():
    """GET /api/mantenimiento/limpiar?dias=30"""
    dias      = int(request.args.get("dias", 30))
    eliminados = db.limpiar_datos_antiguos(dias)
    return jsonify({"eliminados": eliminados, "dias": dias})
```

El servidor también sirve los archivos estáticos del frontend:

```python
@app.route("/")
def index():
    """Sirve el dashboard principal."""
    return send_from_directory(_FRONTEND, "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    """Sirve cualquier fichero estático del frontend."""
    return send_from_directory(_FRONTEND, filename)
```

### 2.6. Base de Datos SQLite (Conceptos de Ollama)

He diseñado un esquema en [database.py](301-Actividades%20final%20de%20unidad%20-%20Segundo%20trimestre/003-Monitorización%20de%20recursos/101-Ejercicios/backend/database.py) con **tres tablas y múltiples granularidades**:

```python
_SQL_CREAR_TABLAS = """
-- Métricas en bruto (cada 2 s → ~43 mil filas/día)
CREATE TABLE IF NOT EXISTS metricas_raw (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp    TEXT    NOT NULL,
    cpu_global   REAL    NOT NULL,
    mem_pct      REAL    NOT NULL,
    mem_usado_mb REAL    NOT NULL,
    disco_pct    REAL    NOT NULL,
    disco_lect   REAL    NOT NULL,  -- MB/s
    disco_escr   REAL    NOT NULL,  -- MB/s
    red_env      REAL    NOT NULL,  -- KB/s
    red_recv     REAL    NOT NULL   -- KB/s
);

-- Estadísticas agregadas por hora
CREATE TABLE IF NOT EXISTS metricas_hora (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    hora         TEXT    NOT NULL UNIQUE,  -- "2024-02-20 14:00"
    cpu_avg      REAL, cpu_max  REAL,
    mem_avg      REAL, mem_max  REAL,
    disco_avg    REAL, disco_max REAL,
    red_avg      REAL, red_max  REAL,
    muestras     INTEGER
);

-- Registro de alertas
CREATE TABLE IF NOT EXISTS alertas (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp  TEXT  NOT NULL,
    metrica    TEXT  NOT NULL,
    valor      REAL  NOT NULL,
    umbral     REAL  NOT NULL,
    severidad  TEXT  NOT NULL,
    mensaje    TEXT  NOT NULL
);

-- Índices para consultas rápidas por tiempo
CREATE INDEX IF NOT EXISTS idx_raw_ts    ON metricas_raw  (timestamp);
CREATE INDEX IF NOT EXISTS idx_alerta_ts ON alertas        (timestamp);
"""
```

He aplicado **upserts con `ON CONFLICT`** (similar a los ejercicios de Ollama) para actualizar las estadísticas horarias de forma atómica:

```python
sql_hora = """
    INSERT INTO metricas_hora
        (hora, cpu_avg, cpu_max, mem_avg, mem_max,
         disco_avg, disco_max, red_avg, red_max, muestras)
    VALUES (?, ?,?,?,?,?,?,?,?, 1)
    ON CONFLICT(hora) DO UPDATE SET
        cpu_avg   = (cpu_avg   * muestras + ?) / (muestras + 1),
        cpu_max   = MAX(cpu_max,   ?),
        mem_avg   = (mem_avg   * muestras + ?) / (muestras + 1),
        mem_max   = MAX(mem_max,   ?),
        disco_avg = (disco_avg * muestras + ?) / (muestras + 1),
        disco_max = MAX(disco_max, ?),
        red_avg   = (red_avg   * muestras + ?) / (muestras + 1),
        red_max   = MAX(red_max,   ?),
        muestras  = muestras + 1
"""
```

La clase `BaseDatosSysWatch` es **thread-safe** mediante un `threading.Lock`:

```python
class BaseDatosSysWatch:
    """
    Clase que gestiona todas las operaciones sobre la base de datos SQLite.
    Utiliza un Lock para garantizar que los accesos desde múltiples
    hilos sean seguros (hilo del monitor + hilo del servidor Flask).
    """
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._lock   = threading.Lock()   # Lock para acceso multi-hilo seguro
        
        # Inicializar esquema
        self._ejecutar_ddl()
    
    def _conectar(self) -> sqlite3.Connection:
        """Abre una conexión fresca a SQLite (thread-safe con Lock externo)."""
        conn = sqlite3.connect(self.db_path, timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")   # Mejor concurrencia
        conn.execute("PRAGMA foreign_keys=ON;")
        return conn
```

---


### Ejemplo completo de flujo de datos

Cuando el sistema recolecta una métrica, ocurre la siguiente secuencia:

**1. Hilo de monitorización recolecta datos** ([monitor.py](301-Actividades%20final%20de%20unidad%20-%20Segundo%20trimestre/003-Monitorización%20de%20recursos/101-Ejercicios/backend/monitor.py#L268-L311)):

```python
# En MonitorSistema.run()
metricas = {
    "timestamp": datetime.now().isoformat(timespec='seconds'),
    "cpu":       self._leer_cpu(),
    "memoria":   self._leer_memoria(),
    "disco":     self._leer_disco(dt),
    "red":       self._leer_red(dt),
    "procesos":  self._leer_procesos_top(),
    "alertas":   [],
}
metricas["alertas"] = self._detectar_alertas(metricas)

# Notificar a todos los callbacks
with self._lock_callbacks:
    callbacks_actuales = list(self._callbacks)

for cb in callbacks_actuales:
    try:
        cb(metricas)  # Invoca on_nueva_metrica() en servidor.py
    except Exception as e:
        print(f"[MonitorSistema] Error en callback: {e}")
```

**2. Callback persiste y distribuye** ([servidor.py](301-Actividades%20final%20de%20unidad%20-%20Segundo%20trimestre/003-Monitorización%20de%20recursos/101-Ejercicios/backend/servidor.py#L46-L69)):

```python
def on_nueva_metrica(metricas: dict) -> None:
    # Guardar en BD (thread-safe internamente)
    db.insertar_metrica(metricas)
    
    # Guardar alertas
    if metricas.get("alertas"):
        db.insertar_alertas(metricas["alertas"], metricas["timestamp"])
    
    # Actualizar caché
    with _lock_ultima:
        _ultima_metrica = metricas
    
    # Broadcast a todos los clientes WebSocket
    if _clientes_conectados > 0:
        payload = {k: v for k, v in metricas.items() if k != "procesos"}
        payload["procesos"] = metricas["procesos"][:5]
        socketio.emit("metrica", payload)
```

**3. Cliente recibe y actualiza UI** ([app.js](301-Actividades%20final%20de%20unidad%20-%20Segundo%20trimestre/003-Monitorización%20de%20recursos/101-Ejercicios/frontend/app.js)):

```javascript
socket.on("metrica", (data) => {
  estado.ultimaMetrica = data;
  
  // Actualizar tarjetas de estado
  actualizarTarjetas(data);
  
  // Agregar punto a gráficas en tiempo real
  actualizarGraficasRT(data);
  
  // Mostrar alertas con toast
  if (data.alertas && data.alertas.length > 0) {
    data.alertas.forEach(a => {
      mostrarToast(`⚠️ ${a.mensaje}`, 
                   a.severidad === "critica" ? "error" : "advertencia");
    });
  }
});
```

### 3.2. Detección de alertas en tiempo real

He implementado un sistema de alertas con **umbrales configurables**. En [monitor.py](301-Actividades%20final%20de%20unidad%20-%20Segundo%20trimestre/003-Monitorización%20de%20recursos/101-Ejercicios/backend/monitor.py#L228-L269):

```python
UMBRALES_DEFAULT = {
    "cpu":     85.0,   # % de CPU
    "memoria": 90.0,   # % de RAM
    "disco":   95.0,   # % de uso del disco
    "red":    100.0,   # MB/s combinado
}

def _detectar_alertas(self, metricas: dict) -> list[dict]:
    """Compara métricas con umbrales y genera lista de alertas."""
    alertas = []
    
    cpu_val = metricas["cpu"]["global"]
    if cpu_val >= self.umbrales["cpu"]:
        alertas.append({
            "metrica":   "CPU",
            "valor":     cpu_val,
            "umbral":    self.umbrales["cpu"],
            "severidad": "critica" if cpu_val >= 95 else "advertencia",
            "mensaje":   f"CPU al {cpu_val}%",
        })
    
    mem_val = metricas["memoria"]["porcentaje"]
    if mem_val >= self.umbrales["memoria"]:
        alertas.append({
            "metrica":   "Memoria",
            "valor":     mem_val,
            "umbral":    self.umbrales["memoria"],
            "severidad": "critica" if mem_val >= 95 else "advertencia",
            "mensaje":   f"RAM al {mem_val}%",
        })
    
    disco_val = metricas["disco"]["porcentaje"]
    if disco_val >= self.umbrales["disco"]:
        alertas.append({
            "metrica":   "Disco",
            "valor":     disco_val,
            "umbral":    self.umbrales["disco"],
            "severidad": "critica" if disco_val >= 99 else "advertencia",
            "mensaje":   f"Disco lleno al {disco_val}%",
        })
    
    return alertas
```

### 3.3. Errores comunes evitados

**❌ ERROR 1: Acceso concurrente sin sincronización**
```python
# INCORRECTO: Multiple threads modificando lista sin Lock
def suscribir(self, callback):
    self._callbacks.append(callback)  # Race condition!
```

**✅ CORRECTO: Uso de Lock**
```python
def suscribir(self, callback) -> None:
    with self._lock_callbacks:
        if callback not in self._callbacks:
            self._callbacks.append(callback)
```

**❌ ERROR 2: Emitir WebSocket desde hilo no-principal sin async_mode**
```python
# Flask-SocketIO requiere async_mode="threading" para emitir desde otros hilos
socketio = SocketIO(app)  # INCORRECTO
```

**✅ CORRECTO:**
```python
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
```

**❌ ERROR 3: No copiar lista de callbacks antes de iterar**
```python
# INCORRECTO: Si otro hilo modifica _callbacks durante la iteración → RuntimeError
for cb in self._callbacks:
    cb(metricas)
```

**✅ CORRECTO: Copiar lista dentro del Lock**
```python
with self._lock_callbacks:
    callbacks_actuales = list(self._callbacks)

for cb in callbacks_actuales:
    try:
        cb(metricas)
    except Exception as e:
        print(f"Error en callback: {e}")
```

**❌ ERROR 4: No usar daemon=True en hilos de fondo**
```python
# Si el hilo no es daemon, el programa no termina al cerrar
monitor = threading.Thread(target=...)
```

**✅ CORRECTO:**
```python
monitor = MonitorSistema(intervalo=2.0)  # daemon=True en __init__
# O bien:
hilo = threading.Thread(target=..., daemon=True)
```

**❌ ERROR 5: Calcular I/O sin tiempo transcurrido**
```python
# INCORRECTO: Bytes leídos NO son tasa de lectura
disco_io = psutil.disk_io_counters()
lectura_mbs = disco_io.read_bytes / 1024**2
```

**✅ CORRECTO: Calcular delta entre muestras**
```python
def _leer_disco(self, dt: float) -> dict:
    io = psutil.disk_io_counters()
    read_mb  = 0.0
    if self._io_disco_prev and dt > 0:
        read_mb = (io.read_bytes - self._io_disco_prev.read_bytes) / 1024**2 / dt
    self._io_disco_prev = io
    return {"lectura_mbs": round(max(0.0, read_mb), 3)}
```

### Ventanas temporales y consultas optimizadas

He implementado **cinco ventanas temporales** que seleccionan automáticamente la granularidad óptima:

```python
def _obtener_historico_por_ventana(ventana: str) -> list[dict]:
    """
    - "1h"  → últimos  60 minutos (datos raw cada 2s)
    - "6h"  → últimas   6 horas   (datos raw)
    - "24h" → últimas  24 horas   (agregados por hora)
    - "7d"  → últimos   7 días    (agregados por hora)
    - "30d" → últimos  30 días    (agregados por hora)
    """
    if ventana == "1h":
        return db.obtener_ultimos_minutos(60)
    elif ventana == "6h":
        return db.obtener_ultimos_minutos(360)
    elif ventana == "24h":
        return db.obtener_por_horas(24)
    elif ventana == "7d":
        return db.obtener_por_horas(24 * 7)
    elif ventana == "30d":
        return db.obtener_por_horas(24 * 30)
    else:
        return db.obtener_ultimos_minutos(60)
```

Esto **evita transferir 43,000 filas al cliente** cuando solicita 30 días: en su lugar, envío solo 720 agregados horarios (30 días × 24 horas).

---

He desarrollado un sistema completo de monitorización de recursos que integra los cuatro pilares del segundo trimestre: programación multiproceso mediante `multiprocessing.Pool` y Web Workers, programación multihilo con hilos demonios y mecanismos de sincronización, comunicaciones en red bidireccionales con WebSockets, y servicios REST con Flask. Este proyecto me ha permitido comprender la importancia crítica de la sincronización en entornos concurrentes, especialmente el uso de `threading.Lock` para proteger datos compartidos y evitar condiciones de carrera.

El diseño separa claramente las responsabilidades entre el hilo de monitorización (que recolecta métricas del sistema), el servidor Flask-SocketIO (que distribuye los datos en tiempo real), y la base de datos SQLite (que almacena histórico con múltiples granularidades). La implementación del patrón Observer mediante callbacks permite desacoplar estos componentes, mientras que el procesamiento paralelo tanto en backend (Python) como en frontend (JavaScript) garantiza que los cálculos pesados no bloqueen la ejecución principal.

Este proyecto conecta directamente con la gestión de procesos (Unidad 1), sincronización entre hilos (Unidad 2), comunicaciones bidireccionales (Unidad 3) y servicios web RESTful (Unidad 4), y constituye una base sólida para implementar sistemas de monitorización distribuida en entornos de producción reales.
