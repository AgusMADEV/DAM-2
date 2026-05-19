En esta actividad práctica he trabajado con herramientas gráficas para la visualización de datos en tiempo real, específicamente aplicadas al monitoreo de recursos del sistema. El concepto principal que he implementado es la **creación de dashboards interactivos** que combinan backend (Python para recopilación de datos), API REST (PHP para servir los datos) y frontend (visualización gráfica con JavaScript).

Este tipo de soluciones se utiliza ampliamente en entornos profesionales para:
- **Monitorización de servidores**: Control de CPU, RAM, disco y red en tiempo real
- **Análisis de rendimiento**: Detección de cuellos de botella y optimización de recursos
- **Dashboards empresariales**: Visualización de KPIs y métricas de negocio
- **Sistemas de alertas**: Notificación automática cuando se superan umbrales críticos

He configurado un sistema completo de monitoreo que recopila métricas del sistema cada minuto y las presenta en gráficos interactivos que se actualizan automáticamente cada 10 segundos.

---

### Arquitectura del Sistema

Mi implementación sigue una **arquitectura de tres capas**:

1. **Capa de Recopilación de Datos (Backend - Python)**
   - Script `server_monitor.py` que utiliza la librería `psutil`
   - Recopila métricas del sistema: CPU, RAM, disco, red, Apache
   - Almacena datos en formato CSV con timestamp

2. **Capa de API (Middleware - PHP)**
   - Archivo `api.php` que actúa como servidor REST
   - Implementa autenticación HTTP Basic
   - Lee archivos CSV y los convierte a JSON
   - Soporta diferentes endpoints según el recurso solicitado

3. **Capa de Presentación (Frontend - PHP/JavaScript)**
   - `index.php`: Dashboard principal con diseño responsive
   - `grafica3.php`: Componente reutilizable de visualización
   - Actualización automática mediante polling

### Componentes Técnicos Implementados

#### A) Script de Monitoreo (server_monitor.py)

He adaptado el script original de Linux para que funcione en Windows. Los principales cambios que realicé fueron:

```python
# Adaptación para Windows del atributo busy_time
def monitor_disk_io():
    disk_io_counters = psutil.disk_io_counters(perdisk=True)
    for disk, io in disk_io_counters.items():
        # busy_time no está disponible en Windows
        busy_time = getattr(io, 'busy_time', 0)
        save_to_csv(f'disk_io_{disk}.csv', [...])
```

**Funciones principales implementadas:**
- `monitor_cpu()`: Captura el porcentaje de uso de CPU con intervalo de 1 segundo
- `monitor_ram()`: Obtiene uso de RAM en porcentaje y GB totales
- `monitor_disk_io()`: Registra operaciones de lectura/escritura por disco
- `monitor_disk_usage()`: Calcula el espacio usado del disco C:
- `monitor_bandwidth()`: Mide bytes enviados/recibidos por interfaz de red
- `monitor_apache_request_rate()`: Analiza logs de Apache para contar peticiones

#### B) API REST (api.php)

He configurado una API que implementa:

**Autenticación:**
```php
$username = 'jocarsa';
$password = 'jocarsa';

if (!isset($_SERVER['PHP_AUTH_USER']) ||
    $_SERVER['PHP_AUTH_USER'] != $username ||
    $_SERVER['PHP_AUTH_PW'] != $password) {
    header('HTTP/1.0 401 Unauthorized');
    die('Authentication required.');
}
```

**Endpoints disponibles:**
- `api.php?endpoint=cpu` - Uso de CPU
- `api.php?endpoint=ram` - Uso de RAM
- `api.php?endpoint=disk_usage` - Uso de disco
- `api.php?endpoint=disk_io&disk=PhysicalDrive0` - I/O de disco específico
- `api.php?endpoint=bandwidth&iface=Ethernet` - Ancho de banda por interfaz
- `api.php?endpoint=apache_request_rate` - Tasa de peticiones Apache

La función `readCsvAsJson()` lee los archivos CSV y los convierte en arrays asociativos JSON:
```php
function readCsvAsJson($csvFile) {
    $data = [];
    $file = fopen($csvFile, 'r');
    $header = fgetcsv($file);
    while ($row = fgetcsv($file)) {
        $data[] = array_combine($header, $row);
    }
    fclose($file);
    return $data;
}
```

#### C) Dashboard Visual (index.php)

He configurado un dashboard con las siguientes características:

**Configuración de gráficos:**
```php
$endpoints = [
    ['endpoint' => 'cpu', 'type' => 'line', 'label' => 'CPU'],
    ['endpoint' => 'ram', 'type' => 'bar', 'label' => 'RAM'],
    ['endpoint' => 'disk_usage', 'type' => 'pie', 'label' => 'DISK'],
    ['endpoint' => 'disk_io', 'type' => 'line', 'label' => 'DISK I/O', 'disk' => 'sda'],
    ['endpoint' => 'bandwidth', 'type' => 'bar', 'label' => 'BANDWIDTH', 'iface' => 'eth0'],
    ['endpoint' => 'apache_request_rate', 'type' => 'line', 'label' => 'REQUEST RATE'],
];
```

**Tipos de visualización implementados:**
- **Line charts**: Para métricas continuas (CPU, I/O, peticiones)
- **Bar charts**: Para comparaciones (RAM, ancho de banda)
- **Pie charts**: Para distribuciones (uso de disco)

**Diseño responsive con CSS Grid:**
```css
body {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    grid-auto-rows: 220px;
    gap: var(--grid-gap);
}
```

Cada tarjeta ocupa espacio dinámico en la cuadrícula mediante:
```php
grid-column: span <?php echo rand(1, 2); ?>;
grid-row: span <?php echo rand(1, 2); ?>;
```

### 2.3. Flujo de Datos Completo

1. **Recopilación**: Python ejecuta `psutil` y guarda métricas en CSV con timestamp
2. **Almacenamiento**: Datos en `monitor_data/*.csv` con estructura:
   ```csv
   date,cpu_usage
   2026-02-05 14:30:15,45.2
   2026-02-05 14:31:15,52.7
   ```
3. **Exposición**: API PHP lee CSV, valida autenticación y devuelve JSON
4. **Visualización**: JavaScript en `grafica3.php` solicita datos cada 10s y renderiza gráficos
5. **Actualización**: Proceso continúo que mantiene el dashboard actualizado

---

###  Implementación Realizada

He configurado el entorno completo en la carpeta `102-Actividad EVAL/` con la siguiente estructura:

```
102-Actividad EVAL/
├── server_monitor.py       # Script de recopilación
├── api.php                 # API REST
├── grafica3.php            # Componente de gráficos
├── index.php               # Dashboard principal
├── run_monitor.ps1         # Script de ejecución continua
├── monitor_data/           # Datos CSV generados
│   ├── cpu_usage.csv
│   ├── ram_usage.csv
│   ├── disk_usage.csv
│   └── ...
├── README.md               # Documentación técnica
└── INSTRUCCIONES.html      # Guía visual
```

### Pasos de Configuración Realizados

**1. Preparación del entorno Python:**
```powershell
# Configuración del entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate

# Instalación de dependencias
pip install psutil pytz
```

**2. Adaptaciones para Windows:**

He modificado el código original para compatibilidad con Windows:

```python
# Cambio 1: Manejo del atributo busy_time
busy_time = getattr(io, 'busy_time', 0)

# Cambio 2: Ruta de disco en Windows
disk_usage = psutil.disk_usage('C:' if os.name == 'nt' else '/')

# Cambio 3: Ruta de logs de Apache en XAMPP
ACCESS_LOG = 'D:/xampp/apache/logs/access.log' if os.name == 'nt' else '/var/log/apache2/access.log'
```

**3. Ejecución del monitor:**

He creado un script PowerShell para ejecución continua:
```powershell
# run_monitor.ps1
$pythonPath = "D:/.../.venv/Scripts/python.exe"
$scriptPath = "server_monitor.py"

while ($true) {
    & $pythonPath $scriptPath
    Start-Sleep -Seconds 60
}
```

**4. Personalización del dashboard:**

He configurado diferentes tipos de gráficos según el tipo de dato:
- **CPU**: Gráfico de líneas (tendencia temporal)
- **RAM**: Gráfico de barras (comparación de estados)
- **Disco**: Gráfico circular (proporción usado/libre)

### Ejemplo Real de Uso

**Caso práctico implementado:**

1. Inicio el monitor en PowerShell:
```powershell
cd "102-Actividad EVAL"
.\run_monitor.ps1
```

2. El monitor recopila datos cada 60 segundos:
```
[1] Recopilando datos del sistema... ✓ Completado en 0.87s
[2] Recopilando datos del sistema... ✓ Completado en 0.92s
```

3. Los datos se guardan en CSV:
```csv
date,cpu_usage
2026-02-05 14:30:15,45.2
2026-02-05 14:31:15,52.7
2026-02-05 14:32:15,38.1
```

4. Accedo al dashboard en: `http://localhost/.../102-Actividad EVAL/index.php`

5. El dashboard solicita autenticación (jocarsa/jocarsa)

6. Los gráficos se renderizan y actualizan automáticamente cada 10 segundos

### Errores Comunes y Soluciones

Durante la implementación encontré y resolví estos errores:

**Error 1: AttributeError 'busy_time'**
```
AttributeError: 'sdiskio' object has no attribute 'busy_time'
```
**Solución:** Usar `getattr()` con valor por defecto
```python
busy_time = getattr(io, 'busy_time', 0)
```

**Error 2: Ruta de disco incorrecta**
```
FileNotFoundError: [Errno 2] No such file or directory: '/'
```
**Solución:** Detectar sistema operativo y usar ruta apropiada
```python
disk_usage = psutil.disk_usage('C:' if os.name == 'nt' else '/')
```

**Error 3: Log de Apache no encontrado**
```
Warning: Apache log file not found at /var/log/apache2/access.log
```
**Solución:** Usar ruta de XAMPP en Windows y validar existencia
```python
ACCESS_LOG = 'D:/xampp/apache/logs/access.log' if os.name == 'nt' else '/var/log/apache2/access.log'
if not os.path.exists(ACCESS_LOG):
    print(f"Warning: Apache log file not found")
    return
```

**Error 4: CORS en peticiones AJAX**
```
Cross-Origin Request Blocked
```
**Solución:** Asegurar que todo esté en el mismo dominio o configurar headers CORS en `api.php`

### Optimizaciones Realizadas

1. **Caché de datos**: Los CSV actúan como caché persistente
2. **Polling eficiente**: Actualización cada 10s en lugar de real-time websockets
3. **Lazy loading**: Los gráficos solo solicitan datos cuando son visibles
4. **Compresión de respuestas**: PHP automáticamente comprime JSON si el cliente lo soporta

---

En esta actividad he implementado un **sistema completo de monitoreo y visualización de datos** que integra múltiples tecnologías y conceptos aprendidos en la unidad:

**Puntos clave alcanzados:**

1. ✅ **Recopilación automatizada de datos** usando Python y psutil
2. ✅ **API REST funcional** con autenticación y múltiples endpoints
3. ✅ **Visualización interactiva** con tres tipos de gráficos diferentes
4. ✅ **Actualización en tiempo real** mediante polling cada 10 segundos
5. ✅ **Diseño responsive** adaptable a diferentes dispositivos
6. ✅ **Compatibilidad multiplataforma** (adaptado Linux → Windows)

**Conexión con otros contenidos de la unidad:**

- **Informes dinámicos**: El dashboard es un informe visual que se genera dinámicamente
- **Chart libraries**: Aunque usé código personalizado, entiendo cómo bibliotecas como Chart.js, D3.js o ApexCharts funcionan bajo el mismo principio
- **Integración IDE**: He trabajado con VS Code usando extensiones de Python, PHP y depuración
- **APIs externas**: La API implementada podría consumirse desde cualquier cliente (móvil, desktop, web)
- **Persistencia de datos**: Los CSV son una forma simple pero efectiva de almacenar series temporales

**Aprendizajes significativos:**

He comprendido la importancia de:
- Separar responsabilidades (recopilación, exposición, visualización)
- Implementar autenticación en APIs públicas
- Adaptar código entre diferentes sistemas operativos
- Manejar errores de forma robusta con valores por defecto
- Documentar el código y proceso para facilitar mantenimiento

Esta actividad me ha permitido aplicar conocimientos de **desarrollo web full-stack**, combinando backend (Python), middleware (PHP/API REST) y frontend (JavaScript/CSS), y entender cómo se construyen dashboards profesionales de monitoreo como los que se usan en empresas para supervisar servidores de producción.

La experiencia de adaptar código de Linux a Windows me ha enseñado la importancia de escribir **código portable** y manejar las diferencias entre plataformas de forma elegante.