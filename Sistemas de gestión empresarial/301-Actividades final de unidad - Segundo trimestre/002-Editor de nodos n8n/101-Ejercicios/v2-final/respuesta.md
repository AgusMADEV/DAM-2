El proyecto que he desarrollo consiste en un **editor visual de nodos tipo n8n** para la automatización de flujos de trabajo empresariales. Este sistema permite crear workflows mediante una interfaz gráfica de arrastrar y soltar, conectando diferentes nodos que procesan y transforman datos de forma secuencial o condicional.

En el contexto de los sistemas ERP-CRM que hemos estudiado a lo largo del curso, este proyecto se enmarca dentro de la **Unidad 5: Desarrollo de componentes**, específicamente en la creación de herramientas extensibles que permitan automatizar procesos empresariales sin necesidad de programar directamente cada operación. A diferencia de los sistemas tradicionales basados en formularios y ventanas, este enfoque visual facilita la comprensión del flujo de datos y permite a usuarios no técnicos configurar procesos complejos.

El sistema sirve para automatizar tareas repetitivas en entornos empresariales como:
- Procesamiento de datos desde archivos CSV (lectura, filtrado, transformación, escritura)
- Gestión de flujos condicionales (if/else, bucles while, routers)
- Manipulación de variables y estado entre nodos
- Operaciones de sistema de archivos (listar carpetas, copiar archivos)
- Extracción y mapeo de campos de datos estructurados

Este tipo de soluciones se utilizan en contextos donde se necesita integrar diferentes fuentes de datos, aplicar transformaciones complejas y ejecutar acciones basadas en condiciones específicas, todo ello de manera visual y mantenible.

---

### Arquitectura del Sistema

El proyecto implementa una **arquitectura cliente-servidor** con separación clara entre backend y frontend:

**Backend (Python/Flask):**
- Framework: Flask como servidor web RESTful
- Sistema de módulos dinámicos mediante carga reflexiva
- API RESTful para ejecución de workflows, gestión de archivos y persistencia
- Motor de ejecución basado en **dataflow** con propagación de datos tipo grafo dirigido

**Frontend (JavaScript Vanilla ESM):**
- Interfaz visual con HTML5 Canvas y SVG para conexiones
- Sistema de drag & drop para creación de nodos
- Gestión de estado mediante estructuras de datos en memoria
- Importación dinámica de módulos frontend para cada tipo de nodo

### Sistema de Módulos Extensible

Cada nodo del sistema sigue un **patrón de plugin** definido por un contrato específico:

**Backend (`modules/*.py`):**
```python
# Definición del tool (metadatos)
TOOL = {
    "type": "nombre_del_nodo",
    "label": "Etiqueta visible",
    "description": "Descripción funcional",
    "config": {
        "parametro1": {"type": "string", "label": "Etiqueta", "default": "valor"},
        # ... más parámetros
    }
}

# Función de ejecución
def execute(config, context):
    # config: parámetros configurados por el usuario
    # context: inputs (datos de entrada), state (estado persistente), BASE_DIR, safe_join
    return {"ok": True, "data": resultado}
```

**Frontend (`static/modules/*.js`):**
```javascript
export default {
  type: "nombre_del_nodo",
  
  // Construcción del UI del nodo
  buildBody(el, tool, nodeId) {
    // Renderiza inputs, selects, checkboxes...
  },
  
  // Lectura de configuración
  readConfig(el) {
    return { /* objeto con valores */ };
  },
  
  // Renderizado de resultados (opcional)
  renderResult(el, data) {
    // Muestra el resultado de la ejecución
  }
}
```

Este patrón permite **extender el sistema sin modificar el core**, siguiendo el principio Open/Closed de SOLID.

### Carga Dinámica de Módulos

El sistema implementa carga dinámica tanto en backend como en frontend:

**Backend (`modules/__init__.py`):**
```python
def load_backend_modules():
    registry = {}
    base_dir = os.path.dirname(__file__)
    
    for filename in os.listdir(base_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            # Carga reflexiva del módulo
            mod = _import_module_from_path(mod_name, path)
            
            # Valida el contrato
            tool = getattr(mod, "TOOL", None)
            execute = getattr(mod, "execute", None)
            
            if isinstance(tool, dict) and callable(execute):
                registry[tool["type"]] = {"TOOL": tool, "execute": execute}
    
    return registry
```

**Frontend:**
```javascript
// Importación dinámica ESM
await Promise.all(TOOLS.map(async (t) => {
    if (t.front_module) {
        const mod = await import(t.front_module);
        frontModules[t.type] = mod.default;
    }
}));
```

### Motor de Ejecución Dataflow

El motor de ejecución implementa un **algoritmo de propagación de datos tipo BFS (Breadth-First Search)** con soporte para ciclos y routing condicional:

**Proceso de ejecución paso a paso:**

1. **Construcción del grafo:**
   - Se crea un diccionario `node_by_id` con todos los nodos
   - Se construye una lista de adyacencia `adj[src] = [(to_id, from_port)]`
   - Se calcula el grado de entrada `indeg[node]` de cada nodo

2. **Inicialización de la cola:**
   - Se agregan a la cola todos los nodos fuente (`indeg == 0`)
   - Si no hay fuentes (grafo cíclico), se agregan todos para permitir ejecución

3. **Ejecución iterativa:**
   ```python
   while q and steps < MAX_STEPS:
       nid = q.popleft()
       
       # Ejecutar nodo
       res = execute_node(nid)
       results[nid] = res
       
       # Propagar resultados
       if res["ok"]:
           propagate(nid, res["data"])
   ```

4. **Propagación con routing:**
   ```python
   def propagate(src_id, out_payload):
       for (to_id, from_port) in adj.get(src_id, []):
           # Si el nodo devuelve routes, enrutar por puerto
           if "routes" in out_payload:
               val = out_payload["routes"].get(from_port)
           else:
               # Sin routes, solo propaga por 'default'
               val = out_payload if from_port == "default" else None
           
           if val is not None:
               inbox[to_id].append(val)
               q.append(to_id)
   ```

5. **Gestión de estado:**
   - Cada nodo puede mantener estado persistente entre ejecuciones via `_state`
   - Esto permite implementar bucles (while) y secuencias con memoria

### Nodos Implementados

He implementado **25 tipos de nodos diferentes**, organizados en categorías:

**Datos:**
- `leer_csv`: Lee archivos CSV y los convierte en listas de diccionarios
- `escribir_csv`: Escribe listas de diccionarios a archivos CSV
- `filtrar`: Filtra elementos según condiciones (==, !=, >, <, contains, etc.)
- `mapear`: Transforma datos (extraer campos, renombrar, agregar campos)
- `extraer_campo`: Extrae un campo específico de objetos

**Variables:**
- `var_set`: Establece variables globales
- `var_get`: Obtiene valores de variables
- `constante`: Emite un valor constante

**Lógica:**
- `ifnode`: Evalúa condición simple
- `ifrouter`: Routing condicional (true/false)
- `while_node`: Bucle while con límite de iteraciones
- `sequence`: Ejecuta nodos en secuencia

**Operadores:**
- `operador`: Operaciones aritméticas (+, -, *, /, %)
- `comparar`: Base para comparaciones
- `cmp_eq`, `cmp_neq`, `cmp_gt`, `cmp_lt`, `cmp_contains`: Operadores de comparación específicos

**Archivos:**
- `listarcarpetas`: Lista contenido de directorios
- `copiarencarpeta`: Copia archivos entre carpetas

**Otros:**
- `imprimir`: Muestra datos en consola con prefijo personalizable

### Sistema de Puertos Dinámicos

Los nodos pueden tener **múltiples puertos de salida** que se crean dinámicamente:

```javascript
// API expuesta al frontend para reconstruir puertos
window.NODE_API = {
  rebuildOutPorts(nodeEl, ports) {
    // ports: [{name, title, topPct}]
    nodeEl.querySelectorAll(".port.out").forEach(p => p.remove());
    
    ports.forEach(pdef => {
      const p = document.createElement("div");
      p.className = "port out";
      p.dataset.port = pdef.name;
      p.title = pdef.title;
      p.style.top = pdef.topPct + "%";
      nodeEl.appendChild(p);
      
      // Event listener para iniciar conexiones
      p.addEventListener("pointerdown", (e) => {
        iniciarConexionDesdeSalida(e, nodeEl, p);
      });
    });
  }
};
```

Esto permite que nodos como `if_router` tengan puertos "true" y "false", o que `while_node` tenga "loop" y "exit".

### Sistema de Persistencia

El sistema implementa **guardado y carga de workflows** en formato JSON:

**Estructura de un workflow:**
```json
{
  "nodes": [
    {"id": "n1", "x": 100, "y": 200, "type": "leer_csv", "config": {...}}
  ],
  "edges": [
    {"from": "n1", "to": "n2", "from_port": "default"}
  ],
  "viewport": {"scale": 1, "translateX": 0, "translateY": 0},
  "saved_at": "2026-02-18T18:47:35.974319",
  "name": "mi-workflow"
}
```

**API de workflows:**
- `GET /api/workflows` - Lista workflows guardados
- `GET /api/workflows/<name>` - Carga workflow específico
- `POST /api/workflows/<name>` - Guarda workflow
- `DELETE /api/workflows/<name>` - Elimina workflow

### Características de UX

**Interacción con el canvas:**
- **Pan:** Ctrl + arrastrar para mover el viewport
- **Zoom:** Ctrl + rueda del ratón
- **Selección:** Click en nodo para seleccionar
- **Borrar:** Tecla Supr para eliminar nodo seleccionado
- **Guardar rápido:** Ctrl + S

**Búsqueda de herramientas:**
```javascript
searchInput.addEventListener("input", (e) => {
  const term = e.target.value.toLowerCase().trim();
  categories.forEach(cat => {
    const matching = cat.tools.filter(t => 
      t.type.toLowerCase().includes(term) || 
      t.label.toLowerCase().includes(term) || 
      t.description.toLowerCase().includes(term)
    );
    cat.visible = matching.length > 0;
    cat.tools.forEach(t => t.visible = matching.includes(t));
  });
  renderCategories();
});
```

**Categorización de herramientas:**
Las herramientas se organizan en categorías colapsables (Datos, Variables, Lógica, Operadores, Archivos, Otros) con iconos SVG distintivos.

### Sistema de Undo/Redo

Implementé un **sistema de historial** para deshacer y rehacer acciones:

```javascript
const undoStack = [];
const redoStack = [];
const MAX_HISTORY = 50;

function saveState() {
  if (isRestoring) return;
  
  const state = serializeWorkflow();
  undoStack.push(state);
  
  if (undoStack.length > MAX_HISTORY) {
    undoStack.shift();
  }
  
  redoStack.length = 0; // Limpiar redo stack
}

// Atajos de teclado
document.addEventListener('keydown', (e) => {
  if (e.ctrlKey && e.key === 'z') {
    e.preventDefault();
    undo();
  }
  if (e.ctrlKey && e.key === 'y') {
    e.preventDefault();
    redo();
  }
});
```

### Seguridad y Límites

Para evitar bucles infinitos y consumo excesivo de recursos:

**Límite global de pasos:**
```python
MAX_STEPS = int(payload.get("max_steps") or 2000)

while q and steps < MAX_STEPS:
    # ... ejecución
    steps += 1

if steps >= MAX_STEPS:
    return jsonify({
        "results": results, 
        "error": f"Corte de seguridad: máximo de pasos alcanzado ({MAX_STEPS})."
    }), 400
```

**Límite por nodo while:**
```python
max_iter = config.get("max_iter", 10)
if iter_n >= max_iter:
    # Forzar salida
    return {"routes": {"loop": None, "exit": payload}}
```

**Control de rutas de archivos:**
```python
def safe_join(base: str, target: str, allow_abs: bool = False):
    if allow_abs and os.path.isabs(target):
        return os.path.abspath(target)
    
    p = os.path.abspath(os.path.join(base, target))
    if base != os.path.sep and not p.startswith(base):
        raise ValueError("Path escapes BASE_DIR")
    return p
```

---

### Caso de Uso Real: Procesamiento de Datos de Clientes

He desarrollado un **workflow de ejemplo** que demuestra un caso práctico empresarial:

**Escenario:** Procesamiento de una lista de clientes desde CSV, filtrado por edad, transformación de datos y escritura del resultado.

**Implementación paso a paso:**

1. **Nodo "Leer CSV"** (`datos_ejemplo.csv`):
```csv
nombre,edad,ciudad,compras
Juan,25,Madrid,150
María,32,Barcelona,280
Pedro,45,Valencia,520
Ana,28,Sevilla,190
```

2. **Nodo "Filtrar"** (edad >= 30):
```javascript
// Configuración del nodo
{
  "campo": "edad",
  "operador": ">=",
  "valor": "30"
}
```

3. **Nodo "Mapear"** (extraer campos relevantes):
```javascript
{
  "operacion": "extraer_campos",
  "campos": "nombre,ciudad,compras"
}
```

4. **Nodo "Escribir CSV"** (resultado.csv):
```csv
nombre,ciudad,compras
María,Barcelona,280
Pedro,Valencia,520
```

**Código del workflow completo:**
```json
{
  "nodes": [
    {
      "id": "n1",
      "type": "leer_csv",
      "config": {
        "archivo": "workflows/datos_ejemplo.csv",
        "delimiter": ",",
        "tiene_encabezado": true
      }
    },
    {
      "id": "n2",
      "type": "filtrar",
      "config": {
        "campo": "edad",
        "operador": ">=",
        "valor": "30"
      }
    },
    {
      "id": "n3",
      "type": "mapear",
      "config": {
        "operacion": "extraer_campos",
        "campos": "nombre,ciudad,compras"
      }
    },
    {
      "id": "n4",
      "type": "escribir_csv",
      "config": {
        "archivo": "workflows/resultado.csv",
        "delimiter": ","
      }
    }
  ],
  "edges": [
    {"from": "n1", "to": "n2"},
    {"from": "n2", "to": "n3"},
    {"from": "n3", "to": "n4"}
  ]
}
```

### Ejemplo de Flujo Condicional Complejo

**Escenario:** Clasificar clientes por nivel de compras (VIP si compras > 250, Regular si no).

**Workflow con IF Router:**

1. **Leer CSV** → lee datos
2. **Extraer Campo "compras"** → obtiene valor numérico
3. **Comparador** (compras > 250) → devuelve boolean
4. **IF Router** → enruta por "true" o "false"
5. **Rama TRUE:** Agregar campo `tipo: "VIP"`
6. **Rama FALSE:** Agregar campo `tipo: "Regular"`
7. **Merge y escritura**

```python
# Nodo comparador
def execute(config, context):
    inputs = context.get("inputs", [])
    valor = extraer_valor_numerico(inputs[0])
    umbral = float(config.get("valor", 0))
    
    return {"result": valor > umbral}

# Nodo if_router (propagación automática)
def execute(config, context):
    inputs = context.get("inputs", [])
    cond, payload = separar_condicion_y_datos(inputs)
    
    return {
        "routes": {
            "true": payload if cond else None,
            "false": payload if not cond else None
        }
    }
```

### Ejemplo de Bucle While

**Escenario:** Contador que suma números del 1 al 10.

```json
{
  "nodes": [
    {"id": "init", "type": "var_set", "config": {"name": "contador", "value": "1"}},
    {"id": "get", "type": "var_get", "config": {"name": "contador"}},
    {"id": "compare", "type": "cmp_lt", "config": {"valor": "10"}},
    {"id": "while", "type": "while_node", "config": {"max_iter": 15}},
    {"id": "increment", "type": "operador", "config": {"operacion": "+", "valor": "1"}},
    {"id": "print", "type": "imprimir", "config": {"prefix": "Valor actual"}}
  ],
  "edges": [
    {"from": "init", "to": "get"},
    {"from": "get", "to": "compare"},
    {"from": "compare", "to": "while"},
    {"from": "while", "to": "increment", "from_port": "loop"},
    {"from": "increment", "to": "print"},
    {"from": "print", "to": "get"},
    {"from": "while", "to": "final", "from_port": "exit"}
  ]
}
```

**Salida de consola:**
```
[18:45:32] Valor actual: 1
[18:45:32] Valor actual: 2
[18:45:32] Valor actual: 3
...
[18:45:32] Valor actual: 10
```

### Errores Comunes y Cómo Evitarlos

**Error 1: Bucle infinito sin límite**
```python
# ❌ INCORRECTO
while condicion:
    hacer_algo()

# ✅ CORRECTO
max_iter = 100
iter_count = 0
while condicion and iter_count < max_iter:
    hacer_algo()
    iter_count += 1
```

**Error 2: No validar tipos de datos**
```python
# ❌ INCORRECTO
def execute(config, context):
    data = context["inputs"][0]  # Puede fallar
    return {"data": data["campo"]}  # Asume que es dict

# ✅ CORRECTO
def execute(config, context):
    inputs = context.get("inputs", [])
    if not inputs:
        return {"ok": False, "error": "No hay datos"}
    
    first = inputs[0]
    if isinstance(first, dict) and "data" in first:
        data = first["data"]
    else:
        data = first
    
    if not isinstance(data, list):
        return {"ok": False, "error": "Se esperaba una lista"}
    
    return {"ok": True, "data": procesar(data)}
```

**Error 3: No limpiar estado entre ejecuciones**
```javascript
// ❌ INCORRECTO
let globalCounter = 0; // Se acumula entre ejecuciones

function execute() {
    globalCounter++;
    return {counter: globalCounter};
}

// ✅ CORRECTO
function execute(config, context) {
    const state = context.state || {};
    const counter = (state.counter || 0) + 1;
    
    return {
        result: counter,
        _state: {counter}  // Estado persistente por nodo
    };
}
```

**Error 4: Rutas de archivo inseguras**
```python
# ❌ INCORRECTO
ruta = config.get("archivo")
with open(ruta) as f:  # Puede acceder a cualquier archivo del sistema
    datos = f.read()

# ✅ CORRECTO
ruta = config.get("archivo")
safe_path = context["safe_join"](context["BASE_DIR"], ruta)
with open(safe_path) as f:
    datos = f.read()
```

### 3.5. Integración con el Temario de la Asignatura

Este proyecto integra conceptos vistos en múltiples unidades del curso:

**Unidad 1 (Identificación de ERP-CRM):**
- Sistemas modulares y extensibles
- Integración de componentes independientes

**Unidad 2 (Instalación y configuración):**
- Gestión de entornos (desarrollo, pruebas)
- Configuración de parámetros (BASE_DIR, ALLOW_ANY_PATH)

**Unidad 3 (Organización y consulta de información):**
- Procesamiento de datos estructurados (CSV, JSON)
- Filtrado y transformación de datasets

**Unidad 4 (Implantación):**
- Adaptación a necesidades específicas
- Módulos personalizables según procesos empresariales

**Unidad 5 (Desarrollo de componentes):**
- Arquitectura de plugins
- Definición de interfaces (TOOL + execute)
- Ciclo de vida de componentes
- APIs y llamadas a funciones
- Depuración y manejo de errores

---

He desarrollado un **sistema completo de automatización de workflows** que cumple con los requisitos de extensibilidad, modularidad y usabilidad propios de un sistema ERP-CRM moderno. Los puntos clave de este proyecto son:

1. **Arquitectura modular extensible:** Sistema de plugins que permite agregar nuevos nodos sin modificar el core, siguiendo principios SOLID.

2. **Motor de ejecución robusto:** Implementación de un algoritmo dataflow con soporte para ciclos, routing condicional y gestión de estado persistente.

3. **Interfaz visual intuitiva:** Sistema drag & drop con categorización de herramientas, búsqueda en tiempo real y atajos de teclado.

4. **Seguridad y control:** Límites de ejecución, validación de rutas de archivos y manejo exhaustivo de errores.

5. **Casos de uso prácticos:** Workflows reales para procesamiento de datos empresariales (filtrado, transformación, exportación).

Este proyecto se conecta directamente con otros contenidos de la unidad, especialmente:
- **Desarrollo de componentes:** Cada nodo es un componente reutilizable con interfaz estandarizada
- **APIs y librerías:** El sistema expone una API REST para integración con otros sistemas
- **Procesamiento de datos:** Implementa operaciones típicas de ETL (Extract, Transform, Load)
- **Depuración:** Sistema de logs y renderizado de resultados para troubleshooting

Las habilidades adquiridas en este proyecto son directamente aplicables al desarrollo de extensiones y personalizaciones en sistemas ERP-CRM comerciales como Odoo, SAP o Microsoft Dynamics, donde la capacidad de crear módulos personalizados y automatizar procesos es fundamental.

En futuros trabajos, podría extender este sistema con:
- Integración con bases de datos (PostgreSQL, MySQL)
- Nodos para APIs HTTP (webhooks, llamadas REST)
- Sistema de roles y permisos multiusuario
- Scheduler para ejecución programada de workflows
- Exportación a formatos de otros sistemas (n8n, Node-RED, Zapier)