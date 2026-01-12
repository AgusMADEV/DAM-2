Para la asignatura de Proyecto intermodular he pensado que la mejor opción sería un **Sistema ERP (Enterprise Resource Planning) Inteligente** que integra un asistente virtual basado en **Inteligencia Artificial** para facilitar la gestión empresarial mediante lenguaje natural.

Un ERP es un sistema de gestión empresarial que integra diferentes áreas de negocio (ventas, inventario, clientes, productos) en una única plataforma centralizada. En nuestro caso, hemos añadido una capa de inteligencia artificial que permite a los usuarios interactuar con el sistema mediante preguntas en lenguaje natural, sin necesidad de conocer SQL o navegar por múltiples menús.

Este tipo de sistemas se utiliza en:
- **Pequeñas y medianas empresas** que necesitan gestionar productos, ventas y clientes
- **Entornos donde la rapidez de acceso a la información** es crucial para la toma de decisiones
- **Empresas que buscan digitalizar** sus procesos de gestión con tecnología moderna
- **Organizaciones que requieren análisis de datos** mediante estadísticas y gráficos en tiempo real

---

### Arquitectura del Sistema

El proyecto sigue una **arquitectura de tres capas** (Presentación, Lógica de Negocio, Datos):

#### Capa de Presentación (Frontend)

**Tecnologías:** HTML5, CSS3, JavaScript vanilla

La interfaz de usuario implementa el patrón **SPA (Single Page Application)**, donde toda la navegación ocurre sin recargar la página:

```javascript
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
}
```

Esta función permite cambiar entre secciones dinámicamente, mejorando la experiencia de usuario al evitar recargas de página completas.

#### Capa de Lógica de Negocio (Backend)

**Tecnologías:** Python, Flask, Ollama

El backend está dividido en **dos servicios independientes**:

**Servicio 1: API REST (Puerto 5001)**
- Gestiona operaciones CRUD sobre la base de datos
- Proporciona endpoints para productos, ventas, clientes, inventario y estadísticas
- Implementa CORS para permitir peticiones desde el frontend

Ejemplo de endpoint:

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
        
        return jsonify({
            'success': True,
            'data': productos
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
```

**Servicio 2: Servicio de IA (Puerto 5000)**
- Procesa consultas en lenguaje natural
- Clasifica la intención del usuario
- Genera consultas SQL dinámicas
- Formatea respuestas comprensibles

#### Capa de Datos

**Tecnología:** MySQL

La base de datos `erp_inteligente` está diseñada siguiendo principios de normalización:

- **Tablas principales:** productos, clientes, ventas, inventario, categorías
- **Relaciones:** Claves foráneas que mantienen integridad referencial
- **Triggers automáticos:** Actualizan el inventario al registrar ventas
- **Vistas:** Facilitan consultas complejas

### Funcionamiento del Asistente IA

El proceso de consulta con IA sigue estos pasos:

**Paso 1: Clasificación de Intención**

El módulo `intent_classifier.py` analiza la pregunta del usuario y determina qué tipo de consulta es:

```python
def classify_intent(self, mensaje):
    """Clasifica la intención del usuario"""
    mensaje_lower = mensaje.lower()
    
    # Patrones para cada intención
    if any(word in mensaje_lower for word in ['stock', 'inventario', 'disponible']):
        if any(word in mensaje_lower for word in ['bajo', 'crítico', 'poco']):
            return 'consulta_stock_bajo', 0.9
        return 'consulta_stock', 0.85
    
    if any(word in mensaje_lower for word in ['venta', 'vendido', 'factur']):
        return 'consulta_ventas', 0.9
```

**Paso 2: Generación de Consulta SQL**

El módulo `query_generator.py` convierte la intención en una consulta SQL válida:

```python
def generar_sql(self, intencion, mensaje, contexto=None):
    """Genera SQL basado en la intención"""
    
    if intencion == 'consulta_stock_bajo':
        sql = """
            SELECT 
                p.codigo,
                p.nombre,
                p.stock_actual,
                p.stock_minimo,
                (p.stock_actual / p.stock_minimo * 100) as porcentaje
            FROM productos p
            WHERE p.stock_actual < p.stock_minimo
            ORDER BY porcentaje ASC
            LIMIT 10
        """
        return sql, None
```

**Paso 3: Ejecución y Formateo**

Se ejecuta la consulta SQL y el módulo `response_formatter.py` convierte los datos en una respuesta legible:

```python
def format_response(datos, intencion, mensaje):
    """Formatea la respuesta según la intención"""
    
    if intencion == 'consulta_stock_bajo':
        if not datos:
            return "✅ ¡Excelente! No hay productos con stock bajo."
        
        respuesta = f"🚨 Encontré {len(datos)} productos con stock bajo:\n\n"
        for p in datos:
            respuesta += f"• {p['nombre']} (código: {p['codigo']})\n"
            respuesta += f"  Stock: {p['stock_actual']} (mínimo: {p['stock_minimo']})\n\n"
        
        return respuesta
```

### Terminología Técnica Utilizada

- **REST API:** Interfaz de programación que sigue los principios arquitectónicos REST
- **CORS (Cross-Origin Resource Sharing):** Mecanismo que permite peticiones HTTP entre diferentes orígenes
- **SPA (Single Page Application):** Aplicación web que carga una sola página HTML y actualiza dinámicamente el contenido
- **Promesas (Promises):** Objetos JavaScript para manejar operaciones asíncronas
- **Async/Await:** Sintaxis para trabajar con promesas de forma más legible
- **JSON (JavaScript Object Notation):** Formato de intercambio de datos ligero
- **ORM conceptual:** Aunque no usamos un ORM real, aplicamos patrones similares en nuestras funciones de acceso a datos
- **Triggers de BD:** Procedimientos almacenados que se ejecutan automáticamente ante eventos

---

### Caso de Uso Real: Consulta de Stock Bajo

**Escenario:** Un gerente necesita saber rápidamente qué productos están en niveles críticos de inventario.

**Solución Tradicional (sin IA):**
1. Navegar al módulo de inventario
2. Aplicar filtros manualmente
3. Ordenar por stock
4. Analizar la tabla resultante

**Solución con IA (nuestro sistema):**
1. Abrir el chat del asistente
2. Escribir: "¿Qué productos tienen stock bajo?"
3. Obtener respuesta inmediata formateada

**Código del flujo completo:**

**Frontend (chat.js):**
```javascript
async function sendMessage() {
    const input = document.getElementById('chatInput');
    const mensaje = input.value.trim();
    
    if (!mensaje) return;
    
    addMessage('user', mensaje);
    input.value = '';
    showLoading();
    
    try {
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
        
        const data = await response.json();
        removeLoading();
        addMessage('assistant', data.respuesta);
        
    } catch (error) {
        removeLoading();
        addMessage('assistant', '❌ Error al conectar con el asistente');
        console.error('Error:', error);
    }
}
```

**Backend (app.py):**
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

#### Error 1: CORS bloqueando peticiones
**Problema:** El navegador bloquea peticiones entre diferentes puertos
```
Access to fetch at 'http://localhost:5000' from origin 'http://localhost' 
has been blocked by CORS policy
```

**Solución:** Configurar CORS en Flask
```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas
```

#### Error 2: Conexión a base de datos no cerrada
**Problema:** Múltiples conexiones abiertas agotan el pool de MySQL

**Solución:** Siempre cerrar conexiones en bloques try-finally
```python
def get_db_connection():
    try:
        return pymysql.connect(**DB_CONFIG)
    except Exception as e:
        print(f"[ERROR] Conexión BD: {e}")
        return None

# Uso correcto
conexion = get_db_connection()
try:
    cursor = conexion.cursor()
    # ... operaciones ...
finally:
    if conexion:
        conexion.close()
```

#### Error 3: Formato de respuesta JSON inconsistente
**Problema:** El frontend espera siempre el mismo formato pero recibe estructuras diferentes

**Solución:** Estandarizar todas las respuestas
```python
# ✅ CORRECTO - Formato consistente
return jsonify({
    'success': True,
    'data': resultados
})

# ❌ INCORRECTO - Formato variable
return jsonify(resultados)  # A veces es lista, a veces diccionario
```

#### Error 4: Asincronía mal manejada en JavaScript
**Problema:** Intentar usar datos antes de que la promesa se resuelva

**Solución:** Usar async/await correctamente
```javascript
// ❌ INCORRECTO
function cargarProductos() {
    fetch(`${API_URL}/productos`)
        .then(response => response.json())
        .then(data => mostrarProductos(data));
    
    console.log('Productos cargados'); 
}

// ✅ CORRECTO
async function cargarProductos() {
    try {
        const response = await fetch(`${API_URL}/productos`);
        const data = await response.json();
        mostrarProductos(data);
        
        // Ahora sí tenemos los datos
        console.log('Productos cargados correctamente');
    } catch (error) {
        console.error('Error cargando productos:', error);
    }
}
```

### Sistema de Autenticación y Carga Dinámica del Dashboard

Un caso práctico fundamental es el sistema de autenticación con LocalStorage y la carga dinámica de datos al acceder al dashboard.

**Flujo completo:** Usuario hace login → Se guardan datos en LocalStorage → Al entrar al dashboard se valida sesión → Se cargan KPIs y alertas en tiempo real.

**Frontend - Autenticación (auth.js):**
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
        // Validación de usuarios
        const validUsers = {
            'admin': 'admin123',
            'vendedor1': 'admin123',
            'gerente1': 'admin123'
        };
        
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        if (validUsers[username] && validUsers[username] === password) {
            // Login exitoso - Guardar en LocalStorage
            const userData = {
                username: username,
                nombre: username === 'admin' ? 'Administrador' : username,
                rol: username === 'admin' ? 'Administrador' : 'Usuario',
                id: 1
            };
            
            localStorage.setItem('user', JSON.stringify(userData));
            localStorage.setItem('isLoggedIn', 'true');
            
            // Redireccionar al dashboard
            window.location.href = 'dashboard.html';
        } else {
            throw new Error('Credenciales incorrectas');
        }
    } catch (error) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Iniciar Sesión';
        document.getElementById('loginError').style.display = 'block';
    }
});
```

**Frontend - Validación de Sesión (dashboard.js):**
```javascript
// Verificar autenticación al cargar el dashboard
const user = JSON.parse(localStorage.getItem('user'));
if (!user) {
    window.location.href = 'index.html';
}

// Actualizar información del usuario en la interfaz
document.getElementById('userName').textContent = user.nombre;
document.getElementById('userRole').textContent = user.rol;

// Función de logout
function logout() {
    if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
        localStorage.removeItem('user');
        localStorage.removeItem('isLoggedIn');
        window.location.href = 'index.html';
    }
}
```

**Frontend - Carga de Datos del Dashboard (dashboard.js):**
```javascript
// Cargar datos del dashboard al iniciar
async function cargarDashboard() {
    try {
        await cargarKPIs();
        await cargarAlertasStock();
        await cargarVentasRecientes();
        await cargarTopClientes();
    } catch (error) {
        console.error('Error cargando dashboard:', error);
    }
}

// Cargar KPIs desde la API
async function cargarKPIs() {
    try {
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
    } catch (error) {
        console.error('Error cargando KPIs:', error);
    }
}
```

**Backend - Endpoint de KPIs (api_rest.py):**
```python
@app.route('/api/dashboard/kpis', methods=['GET'])
def dashboard_kpis():
    """Obtener indicadores principales del dashboard"""
    try:
        conexion = get_db_connection()
        if not conexion:
            return jsonify({'success': False, 'error': 'Error de conexión'}), 500
        
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        
        # Ventas del día actual
        cursor.execute("""
            SELECT COALESCE(SUM(total), 0) as ventas_hoy
            FROM ventas
            WHERE DATE(fecha_venta) = CURDATE()
        """)
        ventas = cursor.fetchone()
        
        # Total de productos activos
        cursor.execute("""
            SELECT COUNT(*) as total
            FROM productos
            WHERE activo = TRUE
        """)
        productos = cursor.fetchone()
        
        # Productos con stock bajo
        cursor.execute("""
            SELECT COUNT(*) as total
            FROM productos
            WHERE activo = TRUE AND stock_actual < stock_minimo
        """)
        stock_bajo = cursor.fetchone()
        
        # Total de clientes
        cursor.execute("""
            SELECT COUNT(*) as total
            FROM clientes
        """)
        clientes = cursor.fetchone()
        
        conexion.close()
        
        return jsonify({
            'success': True,
            'data': {
                'ventas_hoy': float(ventas['ventas_hoy']),
                'total_productos': productos['total'],
                'productos_stock_bajo': stock_bajo['total'],
                'total_clientes': clientes['total']
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
```

**HTML - Estructura de KPIs (dashboard.html):**
```html
<!-- KPI Cards -->
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-icon blue">
            <i class="fas fa-dollar-sign"></i>
        </div>
        <div class="kpi-info">
            <span class="kpi-label">Ventas Hoy</span>
            <span class="kpi-value" id="ventasHoy">€0.00</span>
            <span class="kpi-change positive">+12.5%</span>
        </div>
    </div>
    
    <div class="kpi-card">
        <div class="kpi-icon green">
            <i class="fas fa-box"></i>
        </div>
        <div class="kpi-info">
            <span class="kpi-label">Total Productos</span>
            <span class="kpi-value" id="totalProductos">0</span>
        </div>
    </div>
    
    <div class="kpi-card">
        <div class="kpi-icon orange">
            <i class="fas fa-exclamation-triangle"></i>
        </div>
        <div class="kpi-info">
            <span class="kpi-label">Stock Bajo</span>
            <span class="kpi-value" id="stockBajo">0</span>
        </div>
    </div>
    
    <div class="kpi-card">
        <div class="kpi-icon purple">
            <i class="fas fa-users"></i>
        </div>
        <div class="kpi-info">
            <span class="kpi-label">Clientes</span>
            <span class="kpi-value" id="totalClientes">0</span>
        </div>
    </div>
</div>
```

Este ejemplo demuestra:
- **Autenticación client-side** con LocalStorage
- **Validación de sesión** al cargar páginas protegidas
- **Peticiones asíncronas** múltiples para cargar datos en paralelo
- **Actualización dinámica del DOM** con datos en tiempo real
- **Manejo de errores** en cada capa de la aplicación
```
---

Este proyecto de ERP Inteligente integra los conocimientos del ciclo en una aplicación funcional que combina gestión empresarial con inteligencia artificial.

He implementado una arquitectura en tres capas que separa claramente presentación, lógica y datos. En el backend decidí crear dos servicios independientes: uno para la IA (puerto 5000) que procesa lenguaje natural con Ollama, y otro para la API REST (puerto 5001) que gestiona el CRUD. Esta separación facilita el mantenimiento y permite escalar cada servicio según la carga. La IA es el elemento más innovador, ya que transforma preguntas normales en consultas SQL, haciendo el sistema accesible sin conocimientos técnicos.

En el frontend apliqué el patrón SPA con JavaScript vanilla, demostrando que no siempre es necesario usar React o Vue para crear interfaces modernas. El uso correcto de async/await y la actualización del DOM aseguran una buena experiencia de usuario. Para el acceso a datos, he seguido buenas prácticas con consultas parametrizadas en PyMySQL para prevenir SQL Injection y siempre cierro las conexiones correctamente.

El proyecto integra conceptos de varios módulos: **Acceso a Datos** (conexiones MySQL y consultas complejas), **Servicios y Procesos** (arquitectura REST y servicios concurrentes), **Desarrollo de Interfaces** (SPA y diseño responsivo) y **Gestión Empresarial** (módulos de productos, ventas e inventario). La IA, aunque no está en el temario oficial, complementa perfectamente lo aprendido y me prepara para tecnologías actuales.

En resumen, el proyecto funciona completamente, está probado con XAMPP, Python y Ollama, y demuestra que puedo aplicar lo aprendido en un caso real de desarrollo de software empresarial.