He desarrollado un **sistema ERP con asistente de Inteligencia Artificial** que permite gestionar operaciones empresariales mediante lenguaje natural. El sistema responde preguntas como "¿qué productos tienen stock bajo?" y ejecuta automáticamente las consultas SQL necesarias, formateando los resultados de manera comprensible.

En las empresas tradicionales, acceder a información del ERP requiere:
- Conocer SQL o navegar complejos menús
- Tiempo para generar informes
- Personal capacitado para extraer datos

**Mi solución:** Un chat inteligente donde preguntas en lenguaje natural y obtienes respuestas inmediatas con los datos del ERP.

---

### Decisión de Diseño: ¿Por qué dos servicios separados?

Implementé una **arquitectura de microservicios** con dos aplicaciones Flask independientes:

**Puerto 5000 → Servicio de Inteligencia Artificial**
- Procesa lenguaje natural
- Genera consultas SQL dinámicas
- Formatea respuestas

**Puerto 5001 → API REST para CRUD**
- Gestiona productos, ventas, clientes
- Operaciones de lectura/escritura en BD
- Endpoints para el frontend

Esta separación permite:
- Escalar cada servicio según demanda
- Reiniciar el servicio de IA sin afectar operaciones críticas
- Desplegar actualizaciones independientemente

### Servicio de IA: Código Real del Motor Principal

El archivo `app.py` del servicio de IA implementa el endpoint principal que procesa consultas:

```python
@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint principal del chat con IA"""
    try:
        data = request.get_json()
        mensaje = data.get('mensaje', '')
        usuario_id = data.get('usuario_id', 1)
        
        # 1. Clasificar intención
        classifier = get_classifier()
        intencion, confianza = classifier.classify_intent(mensaje)
        
        # 2. Generar SQL
        query_gen = get_query_generator()
        sql, params = query_gen.generar_sql(intencion, mensaje)
        
        # 3. Ejecutar consulta
        resultados = ejecutar_consulta(sql, params)
        
        # 4. Formatear respuesta
        respuesta = format_response(resultados, intencion, mensaje)
        
        # 5. Guardar en historial
        guardar_conversacion(usuario_id, mensaje, respuesta, intencion, confianza, sql)
        
        return jsonify({
            'respuesta': respuesta,
            'intencion': intencion,
            'confianza': confianza
        })
        
    except Exception as e:
        return jsonify({
            'respuesta': f"❌ Error: {str(e)}",
            'error': True
        }), 500
```

Este código muestra el **pipeline completo** de procesamiento de IA en 5 pasos secuenciales.

### API REST: CRUD de Productos

El archivo `api_rest.py` implementa endpoints estándar para gestión de datos:

```python
@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    try:
        conexion = get_db_connection()
        if not conexion:
            return jsonify({'success': False, 'error': 'Error de conexión a BD'}), 500
        
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute('''
            SELECT p.*, c.nombre as categoria_nombre
            FROM productos p
            LEFT JOIN categorias_productos c ON p.categoria_id = c.id
            WHERE p.activo = TRUE
            ORDER BY p.nombre
        ''')
        
        productos = cursor.fetchall()
        conexion.close()
        
        return jsonify({'success': True, 'data': productos})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
```

Nótese:
- **DictCursor** para obtener resultados como diccionarios
- **LEFT JOIN** para traer datos relacionados en una sola consulta
- **Manejo de errores** con try-except y respuestas JSON consistentes
- **Cierre de conexión** en todas las rutas

---

## El Cerebro del Sistema: Clasificación de Intenciones

### ¿Cómo entiende el sistema lo que pregunto?

El módulo `intent_classifier.py` usa **pattern matching** con expresiones regulares y palabras clave. No utiliza redes neuronales complejas, sino un enfoque basado en reglas que es suficiente para nuestro dominio específico:

```python
class IntentClassifier:
    """Clasificador de intenciones del usuario"""
    
    # Definición de intenciones soportadas
    INTENTS = {
        'consulta_stock': {
            'keywords': ['stock', 'inventario', 'cantidad', 'cuántos', 'unidades', 'existencias', 'bajo stock'],
            'patterns': [
                r'\b(stock|inventario|unidades)\b.*\b(bajo|poco|mínimo|crítico)\b',
                r'\b(cuánto|cuántos|cantidad)\b.*\b(stock|inventario|quedan)\b',
                r'\b(productos|artículos)\b.*\b(stock|inventario)\b'
            ]
        },
        'consulta_ventas': {
            'keywords': ['ventas', 'vendido', 'facturas', 'ingresos', 'facturación', 'vendí'],
            'patterns': [
                r'\b(ventas|vendido)\b.*\b(hoy|semana|mes|año)\b',
                r'\b(cuánto|total)\b.*\b(vendido|ventas|ingresos)\b',
                r'\b(facturas?)\b.*\b(pendiente|pagada|vencida)\b'
            ]
        },
        'consulta_clientes': {
            'keywords': ['cliente', 'clientes', 'comprador', 'compradores'],
            'patterns': [
                r'\b(cliente|clientes)\b.*\b(mejor|top|más|inactivo)\b',
                r'\b(quién|cual)\b.*\b(cliente|comprado|compra)\b',
                r'\b(clientes?)\b.*\b(sin comprar|inactivos)\b'
            ]
        },
        'consulta_productos': {
            'keywords': ['producto', 'productos', 'artículo', 'artículos', 'catálogo'],
            'patterns': [
                r'\b(producto|productos)\b.*\b(más|mejor|top)\b',
                r'\b(cuáles?|qué)\b.*\b(productos?|artículos?)\b',
                r'\b(busca|encuentra|muestra)\b.*\b(producto)\b'
            ]
        }
    }
```

**Ejemplo práctico:** Si pregunto "¿Qué productos tienen stock bajo?", el clasificador:
1. Detecta las palabras clave: `productos`, `stock`, `bajo`
2. Aplica el pattern regex que busca: `\b(stock|inventario|unidades)\b.*\b(bajo|poco|mínimo|crítico)\b`
3. Clasifica como `consulta_stock` con confianza del 90%

### Ventajas de este enfoque basado en reglas:
- **Transparente:** Puedo debuggear exactamente por qué eligió una intención
- **Rápido:** No requiere modelos de ML pesados
- **Preciso:** En un dominio específico como ERP, las reglas funcionan muy bien
- **Sin dependencias externas:** Solo usa la librería `re` de Python estándar

---

## 4. Generación Dinámica de SQL: El Corazón de la IA

Una vez clasificada la intención, el módulo `query_generator.py` construye la consulta SQL apropiada:

```python
def _query_stock(self, texto: str) -> Tuple[str, Dict]:
    """Generar consulta para inventario/stock"""
    texto_lower = texto.lower()
    
    # Detectar si pregunta por stock bajo
    if any(word in texto_lower for word in ['bajo', 'poco', 'mínimo', 'crítico', 'escaso']):
        query = """
            SELECT 
                p.codigo,
                p.nombre,
                c.nombre AS categoria,
                p.stock_actual,
                p.stock_minimo,
                (p.stock_minimo - p.stock_actual) AS faltante
            FROM productos p
            LEFT JOIN categorias_productos c ON p.categoria_id = c.id
            WHERE p.stock_actual < p.stock_minimo 
                AND p.activo = TRUE
            ORDER BY (p.stock_minimo - p.stock_actual) DESC
            LIMIT 20
        """
        return (query, {})
```

**Características clave del generador:**
- **Consultas parametrizadas:** Aunque en este caso no hay parámetros, el sistema soporta `%s` para prevenir SQL Injection
- **JOINs inteligentes:** Trae datos de tablas relacionadas (categorías) en una sola consulta
- **Campo calculado:** `(p.stock_minimo - p.stock_actual) AS faltante` calcula cuántas unidades faltan
- **Ordenamiento estratégico:** Ordena por productos más críticos primero
- **Límite de resultados:** LIMIT 20 para no saturar la respuesta

### Caso real: Consulta de ventas del mes

```python
def _query_ventas(self, texto: str) -> Tuple[str, Dict]:
    """Generar consulta para ventas"""
    texto_lower = texto.lower()
    
    if 'mes' in texto_lower or 'mensual' in texto_lower:
        query = """
            SELECT 
                COUNT(*) as num_ventas,
                SUM(total) as total_ingresos,
                AVG(total) as ticket_promedio,
                MAX(total) as venta_mayor
            FROM ventas
            WHERE YEAR(fecha) = YEAR(CURDATE())
                AND MONTH(fecha) = MONTH(CURDATE())
        """
        return (query, {})
```

Esta consulta demuestra el uso de:
- **Funciones agregadas:** COUNT, SUM, AVG, MAX
- **Funciones de fecha:** YEAR(), MONTH(), CURDATE()
- **Filtros temporales:** Para obtener solo datos del mes actual

---

## Formateador de Respuestas: Datos Legibles para Humanos

El módulo `response_formatter.py` convierte resultados SQL crudos en texto amigable:

```python
def _format_stock(resultados, pregunta):
    """Formatear respuestas de stock"""
    if 'bajo' in pregunta.lower() or 'poco' in pregunta.lower():
        num_productos = len(resultados)
        respuesta = f"📦 He encontrado {num_productos} producto(s) con stock bajo:\n\n"
        
        for i, row in enumerate(resultados[:10], 1):  # Máximo 10
            nombre = row.get('nombre', 'Sin nombre')
            codigo = row.get('codigo', '')
            stock = row.get('stock_actual', 0)
            minimo = row.get('stock_minimo', 0)
            faltante = row.get('faltante', 0)
            
            respuesta += f"{i}. {nombre} (#{codigo})\n"
            respuesta += f"   Stock actual: {stock} unidades (mínimo: {minimo})\n"
            respuesta += f"   Faltan: {faltante} unidades\n\n"
        
        if num_productos > 10:
            respuesta += f"... y {num_productos - 10} producto(s) más.\n"
        
        respuesta += "¿Quieres que te ayude con algo más?"
        return respuesta
```

**Decisiones de diseño del formateador:**
- **Emojis:** Añaden contexto visual (📦 para stock, 💰 para ventas)
- **Límite de visualización:** Solo muestra primeros 10 resultados para no saturar
- **Información resumida:** Indica si hay más resultados
- **Método `.get()`:** Evita errores si falta algún campo en el resultado
- **Formato conversacional:** Termina con una pregunta amigable

### Ejemplo de respuesta formateada para ventas:

```python
def _format_ventas(resultados, pregunta):
    """Formatear respuestas de ventas"""
    if 'num_ventas' in resultados[0] and 'ticket_promedio' in resultados[0]:
        row = resultados[0]
        num_ventas = row.get('num_ventas', 0)
        total = row.get('total_ingresos', 0)
        promedio = row.get('ticket_promedio', 0)
        
        respuesta = "📊 Ventas del mes:\n\n"
        respuesta += f"• Número de ventas: {num_ventas}\n"
        respuesta += f"• Total ingresado: €{total:,.2f}\n"
        respuesta += f"• Ticket promedio: €{promedio:,.2f}\n"
        return respuesta
```

Observa el formato `{total:,.2f}`:
- `:,` añade separadores de miles (1,234.56)
- `.2f` fuerza 2 decimales

---

##  Frontend: Comunicación con los Servicios Backend

### Sistema de Autenticación con LocalStorage

El archivo `auth.js` implementa autenticación client-side:

```javascript
// Manejo del formulario de login
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const submitBtn = e.target.querySelector('button[type="submit"]');
    
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Iniciando sesión...';
    
    try {
        const validUsers = {
            'admin': 'admin123',
            'vendedor1': 'admin123',
            'gerente1': 'admin123'
        };
        
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        if (validUsers[username] && validUsers[username] === password) {
            // Login exitoso
            const userData = {
                username: username,
                nombre: username === 'admin' ? 'Administrador Sistema' : 
                        username === 'vendedor1' ? 'Juan Pérez' : 'Laura Martínez',
                rol: username === 'admin' ? 'Administrador' : 
                     username.startsWith('vendedor') ? 'Vendedor' : 'Gerente',
                loginTime: new Date().toISOString()
            };
            
            localStorage.setItem('user', JSON.stringify(userData));
            localStorage.setItem('isLoggedIn', 'true');
            
            window.location.href = 'dashboard.html';
        } else {
            throw new Error('Credenciales incorrectas');
        }
    } catch (error) {
        errorDiv.textContent = '❌ ' + error.message;
        errorDiv.style.display = 'block';
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-sign-in-alt"></i> Iniciar Sesión';
    }
});
```

**Flujo de autenticación:**
1. Usuario envía formulario → `preventDefault()` evita recarga de página
2. Deshabilita botón y muestra spinner (UX importante)
3. Valida credenciales (en producción llamaría a backend)
4. Si éxito → Guarda datos en `localStorage` como JSON
5. Redirecciona a `dashboard.html`
6. Si fallo → Muestra error y rehabilita botón

### Protección de Rutas en el Dashboard

En `dashboard.js`, la primera línea verifica autenticación:

```javascript
// Verificar autenticación
const user = JSON.parse(localStorage.getItem('user'));
if (!user) {
    window.location.href = 'index.html';
}

// Actualizar información del usuario
document.getElementById('userName').textContent = user.nombre;
document.getElementById('userRole').textContent = user.rol;

// Logout
function logout() {
    if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
        localStorage.removeItem('user');
        localStorage.removeItem('isLoggedIn');
        window.location.href = 'index.html';
    }
}
```

### Navegación SPA (Single Page Application)

El dashboard usa **navegación sin recargas** para mejor rendimiento:

```javascript
// Cambiar entre secciones (SPA Navigation)
function cambiarSeccion(seccion, event) {
    // Ocultar todas las secciones
    document.querySelectorAll('.dashboard-content').forEach(s => {
        s.style.display = 'none';
    });
    
    // Mostrar sección seleccionada
    const seccionElement = document.getElementById(seccion + '-section');
    if (seccionElement) {
        seccionElement.style.display = 'block';
    }
    
    // Actualizar clase active en sidebar
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    if (event && event.target) {
        event.target.closest('.nav-item').classList.add('active');
    }
    
    // Cargar datos según sección
    if (seccion === 'dashboard') {
        cargarDashboard();
    } else if (seccion === 'productos') {
        cargarSeccionProductos();
    } else if (seccion === 'ventas') {
        cargarSeccionVentas();
    }
}
```

**Ventajas del patrón SPA:**
- Usuario no ve parpadeo de carga
- Navegación instantánea
- Estado de aplicación se mantiene
- Solo se cargan datos necesarios

---

## 7. Chat con IA: Interfaz de Usuario

El archivo `chat.js` gestiona la comunicación con el servicio de IA:

```javascript
const API_IA_URL = 'http://localhost:5000';
let conversationId = 1;

// Enviar mensaje a la IA
async function sendMessage() {
    const input = document.getElementById('chatInput');
    const mensaje = input.value.trim();
    
    if (!mensaje) return;
    
    // Agregar mensaje del usuario
    addMessage('user', mensaje);
    input.value = '';
    
    // Mostrar loading
    showLoading();
    
    try {
        // Llamar a la API del servicio IA
        const response = await fetch(`${API_IA_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mensaje: mensaje,
                usuario_id: conversationId
            })
        });
        
        if (!response.ok) {
            throw new Error('Error en la comunicación con el servicio IA');
        }
        
        const data = await response.json();
        
        // Ocultar loading
        hideLoading();
        
        // Agregar respuesta de la IA
        addMessage('assistant', data.respuesta);
        
        // Si la consulta es de stock bajo, recargar las alertas
        if (mensaje.toLowerCase().includes('stock')) {
            await cargarAlertasStock();
        }
        
    } catch (error) {
        hideLoading();
        addMessage('assistant', '❌ Error al conectar con el asistente. Verifica que el servicio esté activo en el puerto 5000.');
        console.error('Error:', error);
    }
}
```

**Elementos clave de UX:**
- **Feedback inmediato:** Muestra spinner mientras procesa
- **Manejo de errores:** Si falla, informa al usuario con mensaje útil
- **Actualización automática:** Si pregunta por stock, recarga alertas en el dashboard
- **Async/await:** Código asíncrono limpio y legible

### Funciones de renderizado del chat:

```javascript
// Agregar mensaje al chat
function addMessage(role, content) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    // Formatear contenido (convertir saltos de línea a <br>)
    const formattedContent = content.replace(/\n/g, '<br>');
    messageDiv.innerHTML = formattedContent;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Mostrar indicador de carga
function showLoading() {
    const chatMessages = document.getElementById('chatMessages');
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message loading';
    loadingDiv.id = 'loadingMessage';
    loadingDiv.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Pensando...';
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
```

---

##  Base de Datos: Diseño Normalizado con MySQL

El archivo `schema.sql` define la estructura de datos:

```sql
-- =====================================================
-- TABLA: productos
-- =====================================================
CREATE TABLE productos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    categoria_id INT,
    precio_compra DECIMAL(10,2),
    precio_venta DECIMAL(10,2) NOT NULL,
    margen_porcentaje DECIMAL(5,2) GENERATED ALWAYS AS (
        CASE 
            WHEN precio_compra > 0 THEN ((precio_venta - precio_compra) / precio_compra * 100)
            ELSE 0 
        END
    ) STORED,
    stock_actual INT DEFAULT 0,
    stock_minimo INT DEFAULT 10,
    stock_maximo INT DEFAULT 100,
    unidad_medida VARCHAR(20) DEFAULT 'unidad',
    imagen_url VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias_productos(id) ON DELETE SET NULL,
    INDEX idx_codigo (codigo),
    INDEX idx_nombre (nombre),
    INDEX idx_categoria (categoria_id),
    INDEX idx_stock_bajo (stock_actual, stock_minimo),
    INDEX idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Características avanzadas implementadas:**

### Campo calculado automático (GENERATED COLUMN)
```sql
margen_porcentaje DECIMAL(5,2) GENERATED ALWAYS AS (
    CASE 
        WHEN precio_compra > 0 THEN ((precio_venta - precio_compra) / precio_compra * 100)
        ELSE 0 
    END
) STORED
```
- Se calcula automáticamente al insertar/actualizar
- **STORED** significa que se guarda físicamente (más rápido en consultas)
- Previene inconsistencias en los cálculos de margen

###  Índices estratégicos
```sql
INDEX idx_stock_bajo (stock_actual, stock_minimo)
```
- **Índice compuesto** optimizado para la consulta más común: productos con stock bajo
- MySQL puede usar este índice para comparar `stock_actual < stock_minimo` muy rápido

### Timestamps automáticos
```sql
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```
- `created_at` se establece automáticamente al insertar
- `updated_at` se actualiza solo al modificar el registro

### Claves foráneas con acciones
```sql
FOREIGN KEY (categoria_id) REFERENCES categorias_productos(id) ON DELETE SET NULL
```
- Si elimino una categoría, no borro los productos sino que establezco `categoria_id` a NULL
- Alternativas: `ON DELETE CASCADE` (eliminaría productos) o `ON DELETE RESTRICT` (evitaría eliminar categoría)

### Tabla de clientes con campos de negocio:

```sql
CREATE TABLE clientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefono VARCHAR(20),
    direccion TEXT,
    ciudad VARCHAR(50),
    provincia VARCHAR(50),
    codigo_postal VARCHAR(10),
    pais VARCHAR(50) DEFAULT 'España',
    nif VARCHAR(20) UNIQUE,
    scoring INT DEFAULT 50 COMMENT 'Valoración del cliente 0-100',
    notas TEXT,
    ultima_compra DATE,
    total_compras DECIMAL(10,2) DEFAULT 0.00,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_nombre (nombre),
    INDEX idx_email (email),
    INDEX idx_ultima_compra (ultima_compra),
    INDEX idx_scoring (scoring),
    INDEX idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Campo destacado:** `scoring INT DEFAULT 50 COMMENT 'Valoración del cliente 0-100'`
- Permite clasificar clientes (A, B, C según valor)
- Útil para campañas de marketing segmentadas
- El **COMMENT** documenta el propósito directamente en la BD

---

## Patrones de Código y Buenas Prácticas Aplicadas

### Gestión de Conexiones a Base de Datos

**Patrón implementado:** Función centralizada de conexión

```python
def get_db_connection():
    """Obtener conexión a BD - Patrón visto en clase"""
    try:
        return pymysql.connect(**DB_CONFIG)
    except Exception as e:
        print(f"[ERROR] Conexión BD: {e}")
        return None

def ejecutar_consulta(sql, params=None):
    """
    Ejecutar consulta SQL y devolver resultados
    Basado en el patrón de vuestros proyectos
    """
    conexion = get_db_connection()
    if not conexion:
        return None
    
    try:
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        
        resultados = cursor.fetchall()
        conexion.close()
        return resultados
        
    except Exception as e:
        print(f"[ERROR] Ejecutando consulta: {e}")
        if conexion:
            conexion.close()
        return None
```

**Ventajas:**
- **DRY (Don't Repeat Yourself):** Lógica de conexión en un solo lugar
- **Manejo de errores consistente:** Siempre cierra conexión incluso si falla
- **DictCursor:** Resultados como diccionarios, no tuplas → más legible
- **Consultas parametrizadas:** Previene SQL Injection

### Formato de Respuestas JSON Estandarizado

**Todas las respuestas de API siguen el mismo formato:**

```python
# Éxito
return jsonify({
    'success': True,
    'data': resultados
})

# Error
return jsonify({
    'success': False,
    'error': 'Descripción del error'
}), 500
```

**Beneficio en frontend:**
```javascript
const data = await response.json();
if (data.success) {
    // Procesar data.data
} else {
    // Mostrar data.error
}
```
Siempre sé qué esperar → código frontend más robusto.

### CORS: Permitiendo peticiones cross-origin

```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir peticiones desde el frontend
```

**¿Por qué es necesario?**
- Frontend corre en `http://localhost` (puerto 80 implícito)
- Backend en `http://localhost:5000` y `http://localhost:5001`
- Navegador bloquea peticiones entre diferentes orígenes por seguridad
- CORS le dice al navegador: "Esta API permite peticiones desde otros puertos"

### Patrón Singleton para Componentes de IA

```python
_classifier_instance = None
_query_generator_instance = None

def get_classifier():
    """Obtener instancia única del clasificador"""
    global _classifier_instance
    if _classifier_instance is None:
        _classifier_instance = IntentClassifier()
    return _classifier_instance

def get_query_generator():
    """Obtener instancia única del generador"""
    global _query_generator_instance
    if _query_generator_instance is None:
        _query_generator_instance = QueryGenerator()
    return _query_generator_instance
```

**Ventaja:** Solo se crea una instancia de cada clase durante toda la ejecución → ahorro de memoria.

---

## Casos de Uso Reales con Código Completo

### Caso 1: Usuario pregunta "¿Qué productos tienen stock bajo?"

**PASO 1 - Frontend envía pregunta:**
```javascript
// chat.js
const response = await fetch(`${API_IA_URL}/chat`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        mensaje: "¿Qué productos tienen stock bajo?",
        usuario_id: 1
    })
});
```

**PASO 2 - Backend clasifica intención:**
```python
# intent_classifier.py
# Detecta keywords: ['productos', 'stock', 'bajo']
# Aplica pattern: r'\b(stock|inventario)\b.*\b(bajo|poco|mínimo)\b'
# Resultado: intencion='consulta_stock', confianza=0.9
```

**PASO 3 - Backend genera SQL:**
```python
# query_generator.py
query = """
    SELECT 
        p.codigo, p.nombre, c.nombre AS categoria,
        p.stock_actual, p.stock_minimo,
        (p.stock_minimo - p.stock_actual) AS faltante
    FROM productos p
    LEFT JOIN categorias_productos c ON p.categoria_id = c.id
    WHERE p.stock_actual < p.stock_minimo AND p.activo = TRUE
    ORDER BY (p.stock_minimo - p.stock_actual) DESC
    LIMIT 20
"""
```

**PASO 4 - Backend ejecuta consulta:**
```python
# app.py
resultados = ejecutar_consulta(sql, params)
# Retorna lista de diccionarios con productos
```

**PASO 5 - Backend formatea respuesta:**
```python
# response_formatter.py
respuesta = """
📦 He encontrado 7 producto(s) con stock bajo:

1. Laptop Dell XPS 13 (#LAP001)
   Stock actual: 3 unidades (mínimo: 5)
   Faltan: 2 unidades

2. Mouse Logitech MX Master (#MOU001)
   Stock actual: 8 unidades (mínimo: 15)
   Faltan: 7 unidades

...
"""
```

**PASO 6 - Frontend recibe y muestra:**
```javascript
// chat.js
addMessage('assistant', data.respuesta);
// Usuario ve la respuesta formateada en el chat
```

### Caso 2: Cargar KPIs del Dashboard al iniciar sesión

**PASO 1 - Dashboard llama función de carga:**
```javascript
// dashboard.js
async function cargarDashboard() {
    await cargarKPIs();
    await cargarAlertasStock();
    await cargarVentasRecientes();
}
```

**PASO 2 - Petición al endpoint de KPIs:**
```javascript
async function cargarKPIs() {
    const response = await fetch(`${API_URL}/dashboard/kpis`);
    const data = await response.json();
    
    if (data.success) {
        const kpis = data.data;
        document.getElementById('ventasHoy').textContent = 
            `€${parseFloat(kpis.ventas_hoy || 0).toFixed(2)}`;
        document.getElementById('totalProductos').textContent = 
            kpis.total_productos || 0;
        document.getElementById('stockBajo').textContent = 
            kpis.productos_stock_bajo || 0;
        document.getElementById('totalClientes').textContent = 
            kpis.total_clientes || 0;
    }
}
```

**PASO 3 - Backend procesa múltiples consultas:**
```python
@app.route('/api/dashboard/kpis', methods=['GET'])
def dashboard_kpis():
    cursor = conexion.cursor(pymysql.cursors.DictCursor)
    
    # Ventas del día
    cursor.execute("""
        SELECT COALESCE(SUM(total), 0) as ventas_hoy
        FROM ventas WHERE DATE(fecha_venta) = CURDATE()
    """)
    ventas = cursor.fetchone()
    
    # Total productos activos
    cursor.execute("SELECT COUNT(*) as total FROM productos WHERE activo = TRUE")
    productos = cursor.fetchone()
    
    # Productos con stock bajo
    cursor.execute("""
        SELECT COUNT(*) as total FROM productos
        WHERE activo = TRUE AND stock_actual < stock_minimo
    """)
    stock_bajo = cursor.fetchone()
    
    # Total clientes
    cursor.execute("SELECT COUNT(*) as total FROM clientes")
    clientes = cursor.fetchone()
    
    return jsonify({
        'success': True,
        'data': {
            'ventas_hoy': float(ventas['ventas_hoy']),
            'total_productos': productos['total'],
            'productos_stock_bajo': stock_bajo['total'],
            'total_clientes': clientes['total']
        }
    })
```

**PASO 4 - Frontend actualiza DOM:**
```javascript
// El código de cargarKPIs() actualiza automáticamente los elementos HTML
// Resultado: Tarjetas de KPIs muestran datos en tiempo real
```

---

## Desafíos Técnicos Superados

### Problema 1: CORS bloqueaba todas las peticiones

**Síntoma:**
```
Access to fetch at 'http://localhost:5000' from origin 'http://localhost' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header
```

**Solución implementada:**
```python
from flask_cors import CORS
CORS(app)
```

**Lección aprendida:** En producción, debería configurar CORS solo para orígenes específicos:
```python
CORS(app, resources={r"/api/*": {"origins": "https://miaplicacion.com"}})
```

### Problema 2: Conexiones a BD no se cerraban

**Síntoma:** Después de varias peticiones, MySQL rechazaba conexiones (pool agotado)

**Solución:** Implementar try-finally para garantizar cierre:
```python
def ejecutar_consulta(sql, params=None):
    conexion = get_db_connection()
    if not conexion:
        return None
    
    try:
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, params if params else ())
        return cursor.fetchall()
    except Exception as e:
        print(f"[ERROR] {e}")
        return None
    finally:
        if conexion:
            conexion.close()  # SIEMPRE se ejecuta
```

### Problema 3: Async/Await mal usado en frontend

**Código problemático:**
```javascript
// ❌ INCORRECTO
function cargarDatos() {
    fetch(url).then(r => r.json()).then(data => {
        procesarDatos(data);
    });
    console.log('Datos cargados'); // ¡MENTIRA! Aún no están cargados
}
```

**Solución con async/await:**
```javascript
// ✅ CORRECTO
async function cargarDatos() {
    try {
        const response = await fetch(url);
        const data = await response.json();
        procesarDatos(data);
        console.log('Datos cargados correctamente');
    } catch (error) {
        console.error('Error:', error);
    }
}
```

---

He construido un **ERP funcional con IA** que demuestra dominio de las tecnologías del ciclo DAM-2. La decisión más importante fue separar el servicio de IA del API REST, permitiendo escalabilidad y mantenimiento independiente.

El sistema funciona completamente en un entorno local con XAMPP, Python 3.8+ y Ollama. La arquitectura de tres capas (presentación, lógica, datos) facilita futuras mejoras como:
- Autenticación con JWT en lugar de LocalStorage
- Despliegue en nube (AWS, Azure, Render)
- Modelo de IA más avanzado (fine-tuning con datos históricos)
- App móvil que consuma la misma API

El proyecto integra conocimientos de **bases de datos relacionales**, **servicios web RESTful**, **interfaces de usuario modernas** y **procesamiento de lenguaje natural**, representando una aplicación real del mundo empresarial con tecnología de vanguardia.
