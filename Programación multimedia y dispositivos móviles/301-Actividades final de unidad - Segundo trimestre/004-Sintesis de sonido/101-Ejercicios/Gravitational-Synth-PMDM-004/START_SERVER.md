# 🚀 Cómo ejecutar Gravitational Synth con Flask

Este proyecto ahora incluye un backend Flask para guardar y cargar composiciones del secuenciador.

## 📋 Requisitos

- Python 3.8 o superior
- Navegador web moderno (Chrome, Firefox, Edge)

## 🛠️ Instalación

### 1. Crear entorno virtual (recomendado)

```bash
# En Windows (PowerShell/CMD)
python -m venv .venv
.venv\Scripts\activate

# En Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## ▶️ Ejecución

### 1. Arrancar el servidor Flask

```bash
python app.py
```

Verás algo como:
```
🎵 Inicializando Gravitational Synth API...
✅ Base de datos lista
🚀 Servidor corriendo en http://127.0.0.1:5000
 * Running on http://127.0.0.1:5000
```

### 2. Abrir en el navegador

Abre tu navegador y ve a: **http://127.0.0.1:5000**

## 🎹 Funcionalidades nuevas

### Guardar composición
1. Crea tu patrón en el secuenciador 16-step
2. Ajusta el BPM y configuraciones
3. En el panel **"💾 Composiciones Guardadas"**:
   - Ingresa un título
   - Opcionalmente una descripción
   - Click en **"💾 Guardar Composición"**

### Cargar composición
1. En la lista de composiciones guardadas
2. Haz click en cualquier composición
3. Se cargará automáticamente:
   - Patrón del secuenciador
   - BPM
   - Tipo de oscilador
   - Todas las configuraciones

### Actualizar lista
- Click en **"🔄 Actualizar Lista"** para ver nuevas composiciones

## 📁 Estructura de archivos

```
Gravitational-Synth-PMDM-004/
├── app.py                          # Backend Flask + API REST
├── index.html                      # Frontend (SPA)
├── requirements.txt                # Dependencias Python
├── gravitational_synth.sqlite3     # Base de datos (se crea automáticamente)
├── README.md                       # Este archivo
└── START_SERVER.md                 # Instrucciones de arranque
```

## 🗄️ Base de datos

La base de datos SQLite se crea automáticamente en `gravitational_synth.sqlite3` con:

- **users**: Usuarios del sistema
- **compositions**: Composiciones guardadas
  - `sequencer_grid`: Matriz 7x16 del secuenciador
  - `settings_json`: Configuraciones de audio y física
  - `bpm`, `wave_type`, etc.

## 🔧 API REST Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/compositions` | Lista todas las composiciones |
| `GET` | `/api/compositions/:id` | Obtiene una composición por ID |
| `POST` | `/api/compositions` | Guarda una nueva composición |
| `DELETE` | `/api/compositions/:id` | Elimina una composición |
| `GET` | `/api/stats` | Estadísticas globales |
| `GET` | `/api/health` | Health check |

## 🐛 Solución de problemas

### "Error cargando composiciones"
- Asegúrate de que el servidor Flask esté corriendo en `http://127.0.0.1:5000`
- Verifica que no haya errores en la consola de Python

### "ModuleNotFoundError: No module named 'flask'"
- Activa el entorno virtual: `.venv\Scripts\activate` (Windows)
- Instala dependencias: `pip install -r requirements.txt`

### El servidor no arranca
- Verifica que el puerto 5000 no esté en uso
- Cambia el puerto en `app.py`: `app.run(port=5001)`
- Actualiza también en `index.html`: `const API_BASE = 'http://127.0.0.1:5001/api'`

## 📝 Notas

- La primera vez que arranques el servidor, se crea una composición demo
- Las composiciones se guardan con timestamp UTC
- El servidor corre en modo debug (auto-reload al cambiar código)

---

**¡Disfruta creando música generativa!** 🎵✨
