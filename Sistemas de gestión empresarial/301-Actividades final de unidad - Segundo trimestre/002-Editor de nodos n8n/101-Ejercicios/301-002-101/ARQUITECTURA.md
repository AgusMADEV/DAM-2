# Arquitectura del Sistema

## 📐 Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                    NAVEGADOR WEB (Frontend)                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Panel de    │  │   Lienzo     │  │   Consola    │      │
│  │ Herramientas │  │  de Trabajo  │  │  de Logs     │      │
│  │              │  │              │  │              │      │
│  │ [Cliente]    │  │  ┌────┐      │  │ [timestamp]  │      │
│  │ [Producto]   │  │  │Nodo│──┐   │  │ Ejecutando.. │      │
│  │ [Orden]      │  │  └────┘  │   │  │ Valores...   │      │
│  │ [Aprobar]    │  │     │    ▼   │  │              │      │
│  │ [Registro]   │  │  ┌────┐      │  │              │      │
│  └──────────────┘  │  │Nodo│      │  └──────────────┘      │
│                    │  └────┘      │                         │
│                    └──────────────┘                         │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │            app.js (Lógica Principal)                 │    │
│  │  • Gestión de nodos                                  │    │
│  │  • Sistema de conexiones                             │    │
│  │  • Drag & Drop                                        │    │
│  │  • Zoom & Pan                                         │    │
│  │  • Comunicación con API                              │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                               │
└────────────────────────┬──────────────────────────────────┬─┘
                         │  HTTP/JSON                        │
                         │  (fetch API)                      │
┌────────────────────────┴──────────────────────────────────┴─┐
│                    SERVIDOR FLASK (Backend)                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    app.py                             │   │
│  │  • Servidor HTTP (Flask)                             │   │
│  │  • Endpoints API:                                    │   │
│  │    - GET  /          → index.html                    │   │
│  │    - GET  /api/tools → Lista de herramientas         │   │
│  │    - POST /api/execute → Ejecutar grafo              │   │
│  └──────────────────────────────────────────────────────┘   │
│                            │                                  │
│  ┌────────────────────────┴──────────────────────────────┐  │
│  │              modules/__init__.py                       │  │
│  │  • Cargador dinámico de módulos                       │  │
│  │  • Registro de herramientas disponibles               │  │
│  └────────────────────────────────────────────────────────┘  │
│                            │                                  │
│         ┌──────────────────┼──────────────────┐              │
│         ▼                  ▼                  ▼              │
│  ┌───────────┐      ┌───────────┐      ┌───────────┐       │
│  │ cliente.py│      │producto.py│      │ orden.py  │       │
│  │           │      │           │      │           │       │
│  │ TOOL={}   │      │ TOOL={}   │      │ TOOL={}   │       │
│  │ execute() │      │ execute() │      │ execute() │  ...  │
│  └───────────┘      └───────────┘      └───────────┘       │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Flujo de Ejecución

### 1. Carga Inicial
```
Usuario → [GET /] → Flask → index.html → Navegador
                              ↓
                         app.js cargado
                              ↓
                    [GET /api/tools] → Flask
                              ↓
                      modules/__init__
                              ↓
                   Retorna lista de TOOLS
                              ↓
                     Renderiza botones
```

### 2. Creación de Nodos
```
Usuario click botón → crearNodoDesdeHerramienta()
                              ↓
                    Crea elemento DOM <article>
                              ↓
                    Renderiza campos según TOOL.config
                              ↓
                    Añade a array nodos[]
                              ↓
                    Habilita drag & drop
```

### 3. Conexión de Nodos
```
Usuario arrastra puerto salida → iniciarConexion()
                                        ↓
                              Crea línea SVG temporal
                                        ↓
Usuario suelta en puerto entrada → crearConexion()
                                        ↓
                              Añade a array conexiones[]
                                        ↓
                              Renderiza path SVG permanente
```

### 4. Ejecución del Flujo
```
Usuario click "Ejecutar" → [POST /api/execute]
                                    ↓
                        {nodes: [...], edges: [...]}
                                    ↓
                              Flask app.py
                                    ↓
                        Construye grafo de dependencias
                                    ↓
                          Encuentra nodos de inicio
                                    ↓
                    BFS: Ejecuta cada nodo en orden
                                    ↓
                    Para cada nodo: backend.execute()
                                    ↓
                        Recopila logs y resultados
                                    ↓
                    Retorna {success, logs, results}
                                    ↓
                        Frontend muestra en consola
```

## 📦 Estructura de Datos

### Nodo (Frontend)
```javascript
{
  id: "n1",              // Identificador único
  x: 250,                // Posición X en el lienzo
  y: 180,                // Posición Y en el lienzo
  el: <article>,         // Elemento DOM
  type: "cliente",       // Tipo de nodo
  config: {              // Configuración del usuario
    nombre: "Juan",
    email: "juan@mail.com",
    telefono: "123456"
  }
}
```

### Conexión (Frontend)
```javascript
{
  from: 0,               // Índice del nodo origen
  to: 1,                 // Índice del nodo destino
  fromPort: "default",   // Puerto de salida
  pathBg: <path>,        // Elemento SVG fondo
  path: <path>           // Elemento SVG principal
}
```

### TOOL (Backend)
```python
{
  "type": "cliente",                    # Identificador único
  "label": "👤 Cliente",               # Nombre mostrado
  "description": "Info del cliente",    # Tooltip
  "config": {                           # Campos configurables
    "nombre": {
      "type": "string",                 # Tipo: string|number|boolean
      "label": "Nombre",                # Etiqueta del campo
      "default": ""                     # Valor por defecto
    }
  }
}
```

### Context (Backend - execute)
```python
{
  "inputs": [                    # Valores de nodos anteriores
    {"nombre": "Juan", ...},
    {"precio": 100, ...}
  ],
  "node_id": "n3"                # ID del nodo actual
}
```

### Result (Backend - execute)
```python
{
  "message": "Cliente: Juan (juan@mail.com)",  # Log para consola
  "value": {                                    # Valor para siguiente nodo
    "nombre": "Juan",
    "email": "juan@mail.com",
    "telefono": "123456"
  }
}
```

## 🎨 Patrón de Diseño

### Frontend: MVC Simplificado

**Model** (Estado):
- `nodos[]` - Estado de nodos
- `conexiones[]` - Estado de conexiones
- `TOOLS[]` - Herramientas disponibles

**View** (DOM):
- `templates/index.html` - Estructura
- `static/styles.css` - Presentación
- Elementos dinámicos (nodos, conexiones)

**Controller** (Lógica):
- `static/app.js` - Gestión de eventos y estado
- Funciones: `crearNodo()`, `crearConexion()`, etc.

### Backend: Plugin Architecture

**Core**:
- `app.py` - Servidor y orquestador
- `modules/__init__.py` - Sistema de plugins

**Plugins**:
- `modules/cliente.py` - Plugin cliente
- `modules/producto.py` - Plugin producto
- etc.

Cada plugin es **independiente** y se **auto-registra** mediante:
1. Definir `TOOL` (metadatos)
2. Implementar `execute(config, context)` (lógica)

## 🔐 Seguridad y Validación

### Validaciones Actuales

✅ Verificación de existencia de nodos  
✅ Prevención de conexiones duplicadas  
✅ Detección de ciclos básica (nodos sin entradas)  
✅ Manejo de errores en ejecución  

### Mejoras Recomendadas

⚠️ Validación de tipos de datos  
⚠️ Sanitización de inputs del usuario  
⚠️ Límite de nodos/conexiones  
⚠️ Timeout en ejecución  
⚠️ Rate limiting en API  
⚠️ CORS configuration  

## ⚡ Performance

### Optimizaciones Actuales

- Uso de `transform` CSS para zoom/pan (GPU accelerated)
- Event delegation donde es posible
- Update de conexiones solo cuando es necesario

### Optimizaciones Futuras

- Virtualización para >100 nodos
- Debounce en actualizaciones visuales
- Worker threads para ejecución pesada
- Lazy loading de módulos grandes
- Canvas rendering para miles de conexiones

## 🧪 Testing

### Áreas a Testear

**Backend**:
- [ ] Carga de módulos
- [ ] Ejecución de nodos individuales
- [ ] Orden de ejecución del grafo
- [ ] Manejo de errores

**Frontend**:
- [ ] Creación de nodos
- [ ] Drag & drop
- [ ] Conexiones
- [ ] Zoom & Pan
- [ ] API calls

**Integración**:
- [ ] Flujo completo end-to-end
- [ ] Múltiples navegadores
- [ ] Rendimiento con muchos nodos

## 📚 Extensibilidad

### Añadir un Nuevo Tipo de Nodo

1. Crear archivo `modules/mi_nodo.py`:
```python
TOOL = {
    "type": "mi_nodo",
    "label": "Mi Nodo",
    "description": "...",
    "config": {...}
}

def execute(config, context):
    # Lógica
    return {"message": "...", "value": ...}
```

2. Reiniciar servidor → Auto-detectado ✅

### Añadir Módulo Frontend Específico

1. Crear archivo `static/modules/mi_nodo.js`:
```javascript
export default {
  type: "mi_nodo",
  
  // Personalizar puertos de salida
  getOutPorts(config) {
    return [
      {name: "success", title: "Éxito", topPct: 30},
      {name: "error", title: "Error", topPct: 70}
    ];
  }
};
```

2. El sistema lo cargará automáticamente ✅

## 🎯 Roadmap de Desarrollo

### Fase 1: Base (✅ Completada)
- [x] Estructura del proyecto
- [x] Sistema de nodos básico
- [x] Conexiones visuales
- [x] Ejecución de flujos
- [x] Nodos empresariales básicos

### Fase 2: Funcionalidad (🔄 Siguiente)
- [ ] Persistencia (localStorage)
- [ ] Más tipos de nodos
- [ ] Validaciones mejoradas
- [ ] Undo/Redo

### Fase 3: Datos (🔮 Futuro)
- [ ] Conexión con base de datos
- [ ] CRUD de datos reales
- [ ] Importar/Exportar

### Fase 4: UX (🔮 Futuro)
- [ ] Animaciones avanzadas
- [ ] Modo oscuro
- [ ] Atajos de teclado
- [ ] Minimap

### Fase 5: Enterprise (🔮 Futuro)
- [ ] Multi-usuario
- [ ] Versionado de flujos
- [ ] Roles y permisos
- [ ] Auditoría

---

✨ **Este sistema está diseñado para ser extendido progresivamente**  
Comienza con lo básico y ve añadiendo funcionalidades según necesites.
