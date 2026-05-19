# Actividad de Monitoreo de Servidor - Práctica EVAL

## ✅ Configuración Completada

### 1. Archivos Copiados
- ✅ `server_monitor.py` - Script de monitoreo del servidor
- ✅ `api.php` - API para acceder a los datos
- ✅ `grafica3.php` - Componente de visualización de gráficos
- ✅ `index.php` - Página principal con el dashboard

### 2. Dependencias Instaladas
- ✅ `psutil` - Para monitoreo de recursos del sistema
- ✅ `pytz` - Para manejo de zonas horarias

### 3. Script de Monitoreo Ejecutado
El script `server_monitor.py` ha sido adaptado para Windows y ejecutado correctamente. Los datos se están guardando en la carpeta `monitor_data/`.

---

## 🔧 Cómo Personalizar la Configuración

### Ajustar Endpoints en index.php

Abre el archivo `index.php` y encontrarás el array `$endpoints` (línea 107):

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

#### Opciones de Personalización:

1. **Cambiar el tipo de gráfico:**
   - `'type' => 'line'` - Gráfico de líneas
   - `'type' => 'bar'` - Gráfico de barras
   - `'type' => 'pie'` - Gráfico circular

2. **Ajustar discos a monitorear:**
   ```php
   ['endpoint' => 'disk_io', 'type' => 'line', 'label' => 'DISK I/O', 'disk' => 'PhysicalDrive0']
   ```
   Para ver los discos disponibles en Windows, ejecuta en PowerShell:
   ```powershell
   Get-PhysicalDisk | Select-Object DeviceId, FriendlyName
   ```

3. **Ajustar interfaces de red:**
   ```php
   ['endpoint' => 'bandwidth', 'type' => 'bar', 'label' => 'BANDWIDTH', 'iface' => 'Ethernet']
   ```
   Para ver las interfaces disponibles, ejecuta:
   ```powershell
   Get-NetAdapter | Select-Object Name, InterfaceDescription
   ```

4. **Cambiar credenciales de autenticación (líneas 119-120):**
   ```php
   $username = 'tu_usuario';
   $password = 'tu_contraseña';
   ```

---

## 🚀 Cómo Ejecutar la Aplicación

### Paso 1: Ejecutar el Monitor (ya ejecutado)
El script de monitoreo ya está configurado y ejecutado. Para volver a ejecutarlo:

```powershell
cd "d:\xampp\htdocs\DAM-2\Desarrollo de interfaces\005-Creación de informes\002-Herramientas gráficas integradas en el IDE y externas al mismo\102-Actividad EVAL"
& "D:/xampp/htdocs/DAM-2/Desarrollo de interfaces/005-Creación de informes/002-Herramientas gráficas integradas en el IDE y externas al mismo/.venv/Scripts/python.exe" server_monitor.py
```

### Paso 2: Iniciar Apache
Asegúrate de que XAMPP Apache esté ejecutándose:
1. Abre el Panel de Control de XAMPP
2. Inicia el servicio Apache

### Paso 3: Acceder a la Aplicación
Abre tu navegador y accede a:
```
http://localhost/DAM-2/Desarrollo%20de%20interfaces/005-Creación%20de%20informes/002-Herramientas%20gráficas%20integradas%20en%20el%20IDE%20y%20externas%20al%20mismo/102-Actividad%20EVAL/
```

---

## 📊 Características de la Visualización

- **Actualización automática:** Las gráficas se actualizan cada 10 segundos
- **Diseño responsive:** Se adapta a diferentes tamaños de pantalla
- **Estilo cyberpunk:** Diseño moderno con efectos visuales
- **Grid dinámico:** Las tarjetas ocupan espacios aleatorios en la cuadrícula

---

## 🔄 Ejecutar el Monitor Periódicamente

Para que el monitor recopile datos continuamente, puedes:

1. **Crear un script de PowerShell para ejecutar cada minuto:**
   ```powershell
   # Guardar como run_monitor.ps1
   while ($true) {
       & "D:/xampp/htdocs/DAM-2/Desarrollo de interfaces/005-Creación de informes/002-Herramientas gráficas integradas en el IDE y externas al mismo/.venv/Scripts/python.exe" server_monitor.py
       Start-Sleep -Seconds 60
   }
   ```

2. **Ejecutar el script en segundo plano:**
   ```powershell
   .\run_monitor.ps1
   ```

---

## 📝 Ejercicios Sugeridos

1. **Cambiar tipos de gráficos:** Experimenta cambiando `'line'` por `'bar'` o `'pie'`
2. **Añadir nuevos endpoints:** Agrega más tarjetas de monitoreo
3. **Personalizar estilos CSS:** Modifica los colores y efectos visuales
4. **Cambiar la frecuencia de actualización:** Busca el intervalo de actualización en `grafica3.php`

---

## ⚠️ Notas Importantes

- Los datos se guardan en la carpeta `monitor_data/` en formato CSV
- El log de Apache debe estar en `D:/xampp/apache/logs/access.log`
- En Windows, algunos atributos de `psutil` pueden no estar disponibles (como `busy_time`)
- Las credenciales de autenticación están configuradas en `index.php` y deben coincidir con las de `api.php`

---

¡Buena suerte con tu práctica! 🚀
