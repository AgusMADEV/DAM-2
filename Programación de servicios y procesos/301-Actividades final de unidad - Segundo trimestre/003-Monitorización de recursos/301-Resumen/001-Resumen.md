# Resumen: Monitorización de Recursos

## ¿Qué es SysWatch?

**SysWatch** es un panel de control de recursos del servidor desarrollado como ejercicio personal basado en el ejemplo de clase (panel Ollama). Monitoriza CPU, RAM, Disco y Red, guarda los datos en SQLite y los visualiza en un dashboard web.

## Arquitectura

```
[psutil (OS)] → [MonitorSistema (Thread)] → [BaseDatosSysWatch (SQLite)]
                                          → [Flask-SocketIO (WebSocket)] → [Browser Dashboard]
                                                                          → [Chart.js + Web Worker]
```

## Tecnologías usadas

- **Backend**: Python, psutil, Flask, Flask-SocketIO, sqlite3
- **Frontend**: HTML5, CSS3, JavaScript ES6+, Chart.js, Socket.IO, Web Workers

## Conceptos del módulo aplicados

### Multiproceso (Unidad 1)
- `multiprocessing.Pool.map()` para calcular estadísticas de varias métricas en paralelo
- Web Workers en el navegador para no bloquear la UI

### Multihilo (Unidad 2)
- `MonitorSistema(threading.Thread)` corre en segundo plano recogiendo datos cada 2s
- `threading.Lock` protege acceso a callbacks, última métrica y contadores
- `threading.Event` controla la parada limpia del hilo
- Hilo de limpieza de BD independiente (cada 24h)

### Comunicaciones en red (Unidad 3)
- WebSocket bidireccional: el servidor emite `metrica` cada 2s a todos los clientes
- N clientes simultáneos gracias al broadcast de Flask-SocketIO

### Servicios en red (Unidad 4)
- API REST con Flask: `/api/historico`, `/api/alertas`, `/api/estado`
- El servidor sirve también los ficheros estáticos del frontend

### Base de datos (Ejercicios SQL/Ollama)
- 3 tablas: `metricas_raw` (bruto), `metricas_hora` (agregado), `alertas`
- `ON CONFLICT DO UPDATE` para acumular estadísticas horarias de forma eficiente
- `PRAGMA journal_mode=WAL` para concurrencia de lectura/escritura
