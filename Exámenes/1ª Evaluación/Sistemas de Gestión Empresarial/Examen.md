El proyecto que voy a presentar para la asignatura de Sistemas de Gestión Empresarial, es un software que consiste en un sistema de gestión empresarial orientada a un gimnasio. La finalidad del proyecto es centralizar y automatizar procesos claves como puede ser la gestión de socios, entrenadores, clases, membresías, asistencia a las clases e informes.
Este sistema es utilizado en contextos donde la organización requiere de un control de operaciones internas que se realicen mediante un panel unificado, accesible, desde el navegador.

Un **Sistema ERP-CRM** es una solución informática integral que combina dos tipos de sistemas empresariales fundamentales:

-**`ERP(Enterprise Resource Planning)`**: Sistema de planificación de recursos empresariales que integra y gestiona los procesos operativos internos de una organización (inventario, producción, contabilidad, recursos humanos, etc.).

- **`CRM (Customer Relationship Management)`**: Sistema de gestión de relaciones con clientes que centraliza y optimiza las interacciones con los clientes, mejorando las ventas, el marketing y el servicio al cliente.

---

El sistema sigue un arquitectura **cliente-servidor de tres capas** que está compuesta por:
-`Backend(Python + Flask)`: expone una API REST con operaciones CRUD para todas las entidades
-`Base de datos SQLite`: almacena la información, como, socios, entrenadores, clases, membresías, asistencias y reportes
-`Frontend(HTML5 + CSS3 + JS)`: Consume la API y muestra la información de forma estructurada y usable

### Modelo de Datos Relacional

El sistema implementa las siguientes entidades principales:

 **Tabla: socios (Módulo CRM)**
```sql
CREATE TABLE socios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_socio TEXT UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    email TEXT UNIQUE,
    telefono TEXT,
    fecha_nacimiento DATE,
    direccion TEXT,
    ciudad TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado TEXT DEFAULT 'activo',
    foto TEXT
)
```
**`Función CRM`**: Centraliza toda la información de los clientes (socios) del gimnasio, permitiendo segmentación, análisis de comportamiento y personalización de servicios.

**Tabla: entrenadores (Módulo ERP)**
```sql
CREATE TABLE entrenadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_empleado TEXT UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    email TEXT UNIQUE,
    telefono TEXT,
    especialidad TEXT,
    certificaciones TEXT,
    fecha_contratacion DATE,
    horario TEXT,
    estado TEXT DEFAULT 'activo',
    foto TEXT
)
```
**`Función ERP`**: Gestiona los recursos humanos especializados del gimnasio, controlando disponibilidad, especialidades y asignación a clases.

 **Tabla: clases (Módulo ERP)**
```sql
CREATE TABLE clases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    entrenador_id INTEGER,
    dia_semana TEXT NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    capacidad_maxima INTEGER DEFAULT 20,
    activa BOOLEAN DEFAULT 1,
    FOREIGN KEY (entrenador_id) REFERENCES entrenadores(id)
)
```
**`Función ERP`**: Planifica y organiza los recursos (entrenadores, horarios, espacios) para las actividades grupales.

**Tabla: membresias (Módulo ERP-CRM)**
```sql
CREATE TABLE membresias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    socio_id INTEGER,
    tipo_membresia_id INTEGER,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    precio_pagado DECIMAL(10,2) NOT NULL,
    estado TEXT DEFAULT 'activa',
    fecha_pago DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (socio_id) REFERENCES socios(id),
    FOREIGN KEY (tipo_membresia_id) REFERENCES tipos_membresia(id)
)
```
**`Función mixta`**: Integra ERP (control financiero, inventario de servicios) con CRM (seguimiento del ciclo de vida del cliente).

**Tabla: asistencias (Módulo CRM)**
```sql
CREATE TABLE asistencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    socio_id INTEGER,
    fecha DATE NOT NULL,
    hora_entrada TIME NOT NULL,
    hora_salida TIME,
    clase_id INTEGER,
    FOREIGN KEY (socio_id) REFERENCES socios(id),
    FOREIGN KEY (clase_id) REFERENCES clases(id)
)
```
**`Función CRM`**: Registra el comportamiento y nivel de engagement de los socios para análisis de fidelización.

### Funcionamiento del backend

El archivo `app.py` es el que se encarga de definir los endopints como: 
```py
@app.route('/api/socios', methods=['GET'])
def obtener_socios():
    """Obtener todos los socios"""
    try:
        socios = socio_model.obtener_todos()
        socios_dict = []
        for socio in socios:
            socios_dict.append({
                'id': socio[0],
                'numero_socio': socio[1],
                'nombre': socio[2],
                'apellidos': socio[3],
                'email': socio[4],
                'telefono': socio[5],
                'ciudad': socio[6],
                'estado': socio[7],
                'estado_membresia': socio[8]
            })
        return jsonify({
            'success': True,
            'data': socios_dict
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```
Los modelos obtenidos en `models.py` encapsulan la lógica lógica de acceso a datos, por ejemplo la creación de un socio:
```py
def crear(self, nombre, descripcion, entrenador_id, capacidad_maxima=20, 
              duracion_minutos=60, dia_semana=None, hora_inicio=None, sala=None, nivel='intermedio'):
        """Crea una nueva clase grupal"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO clases (nombre, descripcion, entrenador_id, capacidad_maxima,
                              duracion_minutos, dia_semana, hora_inicio, sala, nivel)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, descripcion, entrenador_id, capacidad_maxima, duracion_minutos,
              dia_semana, hora_inicio, sala, nivel))
```

### Funcionamiento del frontend

El archivo `script.js` implementa controladores para cada módulo.  
Ejemplo de carga dinámica de socios:
```js
async cargarSocios() {
        const tbody = document.getElementById('tabla-socios');
        tbody.innerHTML = '<tr><td colspan="8" class="text-center">Cargando...</td></tr>';
        
        try {
            const response = await fetch(`${API_BASE}/socios`);
            const data = await response.json();
            
            if (data.success) {
                appState.datos.socios = data.data;
                this.renderizarSocios(data.data);
            }
        } catch (error) {
            console.error('Error al cargar socios:', error);
            tbody.innerHTML = '<tr><td colspan="8" class="text-center text-danger">Error al cargar socios</td></tr>';
        }
    }
```

El frontend implementa ``programación orientada a objetos`` para organizar la lógica:
```js
class DashboardController {
    async cargarDatos() {
        try {
            const response = await fetch(`${API_BASE}/informes/dashboard`);
            const data = await response.json();
            
            if (data.success) {
                this.actualizarEstadisticas(data.data);
            }
        } catch (error) {
            console.error('Error al cargar dashboard:', error);
            // Datos de ejemplo si falla la API
            this.actualizarEstadisticas({
                total_socios: 4,
                socios_activos: 3,
                total_entrenadores: 3,
                total_clases: 5,
                ingresos_mes: 465.00
            });
        }
    }

    actualizarEstadisticas(stats) {
        document.getElementById('total-socios').textContent = stats.total_socios;
        document.getElementById('socios-activos').textContent = stats.socios_activos;
        document.getElementById('total-entrenadores').textContent = stats.total_entrenadores;
        document.getElementById('total-clases').textContent = stats.total_clases;
        
        this.cargarAlertas();
    }

    async cargarAlertas() {
        const alertasContainer = document.getElementById('alertas-sistema');
        
        try {
            const response = await fetch(`${API_BASE}/informes/membresias-vencer`);
            const data = await response.json();
            
            if (data.success && data.data.length > 0) {
                alertasContainer.innerHTML = `
                    <div class="alert alert-warning">
                        <i class="fas fa-exclamation-triangle"></i>
                        <span>${data.data.length} membresías próximas a vencer en los próximos 7 días</span>
                    </div>
                `;
            } else {
                alertasContainer.innerHTML = `
                    <div class="alert alert-success">
                        <i class="fas fa-check-circle"></i>
                        <span>No hay alertas pendientes. Todo funcionando correctamente.</span>
                    </div>
                `;
            }
        } catch (error) {
            alertasContainer.innerHTML = `
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i>
                    <span>Sistema operativo. Conectando con la base de datos...</span>
                </div>
            `;
        }
    }
}
```
**Características clave:**
- **Programación asíncrona** con `async/await` para peticiones HTTP
- **Manipulación del DOM** dinámica sin recargar la página
- **Gestión de estado** centralizada en el objeto `appState`
- **Separación de responsabilidades**: carga de datos, renderizado y eventos en métodos distintos

### Diseño

El estilo se gestiona desde `style.css`, usando un diseño responsive y componentes reutilizables como tarjetas, tablas y alertas.

`Un pequeño ejemplo de **style.css** `
```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary-color: #8b5cf6;
    --secondary-color: #64748b;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --danger-color: #ef4444;
    --info-color: #3b82f6;
    --dark-color: #1e293b;
    --light-color: #f8fafc;
    --border-color: #e2e8f0;
    --purple-color: #8b5cf6;
    --shadow-light: 0 1px 3px rgba(0, 0, 0, 0.1);
    --shadow-medium: 0 4px 6px rgba(0, 0, 0, 0.1);
    --transition: all 0.3s ease;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--light-color);
    color: var(--dark-color);
    line-height: 1.6;
}

/* Header */
.header {
    background: linear-gradient(135deg, #8b5cf6, #a78bfa);
    color: white;
    padding: 1rem 2rem;
    box-shadow: var(--shadow-medium);
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    height: 70px;
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1400px;
    margin: 0 auto;
}

.logo {
    display: flex;
    align-items: center;
    font-size: 1.5rem;
    font-weight: bold;
}

.logo i {
    margin-right: 0.5rem;
    font-size: 2rem;
}

.user-info {
    display: flex;
    align-items: center;
    gap: 1rem;
}

/* Sidebar */
.sidebar {
    background: white;
    width: 260px;
    height: calc(100vh - 70px);
    position: fixed;
    top: 70px;
    left: 0;
    box-shadow: var(--shadow-medium);
    border-right: 1px solid var(--border-color);
    z-index: 900;
    overflow-y: auto;
}

.nav-menu {
    list-style: none;
    padding: 1rem 0;
}

.nav-menu li {
    margin: 0;
}

.nav-link {
    display: flex;
    align-items: center;
    padding: 1rem 1.5rem;
    color: var(--secondary-color);
    text-decoration: none;
    transition: var(--transition);
    border-left: 3px solid transparent;
}
```
---

En ejecución, el sistema permite:
- Registrar un nuevo socio mediante la API.
- Consultar clases activas, su capacidad y disponibilidad.
- Generar informes: ingresos por mes, asistencias, clases populares.

### Flujo Completo de una Operación Real

Vamos a analizar el **flujo completo de creación de un nuevo socio**, desde que el usuario hace clic en "Agregar Socio" hasta que el dato se persiste en la base de datos:

#### **Paso 1: Usuario interactúa con el formulario (Frontend)**

```html
<!-- index.html -->
<form id="form-nuevo-socio">
    <input type="text" name="numero_socio" placeholder="Número de socio" required>
    <input type="text" name="nombre" placeholder="Nombre" required>
    <input type="text" name="apellidos" placeholder="Apellidos" required>
    <input type="email" name="email" placeholder="Email">
    <input type="tel" name="telefono" placeholder="Teléfono">
    <button type="submit">Crear Socio</button>
</form>
```
```js
// script.js
document.getElementById('form-nuevo-socio').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const socioData = {
        numero_socio: formData.get('numero_socio'),
        nombre: formData.get('nombre'),
        apellidos: formData.get('apellidos'),
        email: formData.get('email'),
        telefono: formData.get('telefono')
    };
    
    await sociosController.crearSocio(socioData);
});
```

#### **Paso 2: Petición HTTP al Backend**

```javascript
// script.js - Método del controlador
async crearSocio(socioData) {
    try {
        const response = await fetch(`${API_BASE}/socios`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(socioData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            this.mostrarMensaje('Socio creado correctamente', 'success');
            this.cargarSocios(); // Recargar lista
        } else {
            this.mostrarError(result.error);
        }
    } catch (error) {
        this.mostrarError('Error de conexión');
    }
}
```

#### **Paso 3: Backend procesa la petición**
```py
# app.py
@app.route('/api/socios', methods=['POST'])
def crear_socio():
    try:
        # 1. Recibir datos JSON del frontend
        data = request.get_json()
        
        # 2. Llamar al modelo para crear el socio
        socio_id = socio_model.crear(
            numero_socio=data['numero_socio'],
            nombre=data['nombre'],
            apellidos=data['apellidos'],
            email=data.get('email'),
            telefono=data.get('telefono')
        )
        
        # 3. Retornar respuesta exitosa
        return jsonify({
            'success': True,
            'data': {'id': socio_id},
            'message': 'Socio creado correctamente'
        }), 201
        
    except Exception as e:
        # 4. Manejo de errores
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

#### **Paso 4: Modelo ejecuta la inserción SQL**

```py
# models.py
class Socio:
    def crear(self, numero_socio, nombre, apellidos, email=None, telefono=None):
        # 1. Obtener conexión a la BD
        conn = self.db.get_connection()
        cursor = conn.cursor()
        # 2. Ejecutar INSERT con parámetros (previene SQL Injection)
        cursor.execute('''
            INSERT INTO socios (numero_socio, nombre, apellidos, email, telefono)
            VALUES (?, ?, ?, ?, ?)
        ''', (numero_socio, nombre, apellidos, email, telefono))
        # 3. Obtener ID autogenerado
        socio_id = cursor.lastrowid
        # 4. Confirmar transacción
        conn.commit()
        conn.close()
        # 5. Retornar ID al controlador
        return socio_id
```

#### **Paso 5: Base de datos persiste el registro**

```sql
-- SQLite ejecuta internamente:
INSERT INTO socios (numero_socio, nombre, apellidos, email, telefono, fecha_registro, estado)
VALUES ('SOC-001', 'Juan', 'Pérez', 'juan@email.com', '123456789', CURRENT_TIMESTAMP, 'activo');
```

#### **Paso 6: Respuesta llega al Frontend**

```js
// El frontend recibe:
{
    "success": true,
    "data": {"id": 1},
    "message": "Socio creado correctamente"
}
```

``**Ejemplo Real: Consulta Compleja con JOIN**``

Una de las funcionalidades más importantes es **obtener socios con su estado de membresía**. Esto requiere una consulta SQL con JOIN:

```py
# models.py - Método obtener_todos() de la clase Socio
def obtener_todos(self):
    conn = self.db.get_connection()
    cursor = conn.cursor()
    # Consulta con LEFT JOIN para incluir socios sin membresía
    cursor.execute('''
        SELECT 
            s.id, 
            s.numero_socio, 
            s.nombre, 
            s.apellidos, 
            s.email, 
            s.telefono, 
            s.ciudad, 
            s.estado,
            CASE 
                WHEN m.fecha_fin >= date('now') THEN 'Con membresía'
                ELSE 'Sin membresía'
            END as estado_membresia
        FROM socios s
        LEFT JOIN membresias m ON s.id = m.socio_id AND m.estado = 'activa'
        ORDER BY s.fecha_registro DESC
    ''')
    
    socios = cursor.fetchall()
    conn.close()
    return socios
```
`Lo que hace la consulta`:

1. **SELECT**: Selecciona los campos de la tabla socios y calcula el estado de membresía
2. **CASE WHEN**: Lógica condicional SQL que verifica si la fecha de fin de membresía es futura
3. **LEFT JOIN**: Incluye todos los socios, incluso los que no tienen membresía activa
4. **AND m.estado = 'activa'**: Filtra solo membresías activas en el JOIN
5. **ORDER BY fecha_registro DESC**: Ordena por fecha de registro descendente (más recientes primero)

``**Resultado esperado:**``
```
| id | numero_socio | nombre | apellidos | email | telefono | ciudad | estado | estado_membresia |
|----|--------------|--------|-----------|-------|----------|--------|--------|------------------|
| 1  | SOC-001      | Juan   | Pérez     | ...   | ...      | Madrid | activo | Con membresía    |
| 2  | SOC-002      | María  | García    | ...   | ...      | Madrid | activo | Sin membresía    |
```

### Errores comunes y prevención
- **Campos vacíos en el formulario** → Validar los campos antes de enviar la información al backend.
- **IDs incorrectos** → El backend responde con error 404 si no existen los IDs.
- **CORS no configurado**: El navegador bloquea peticiones del frontend al backend por política de mismo origen.
    **✅ Solución:**
    ```py
    # app.py
    from flask_cors import CORS

    app = Flask(__name__)
    CORS(app) 
    ```

### **Integración ERP-CRM en el Proyecto**

Este proyecto demuestra la **integración práctica de funcionalidades ERP y CRM**:

**``Funcionalidades CRM (Gestión de Relación con Clientes)``**
-**Base de datos de socios**: Perfil completo con datos de contacto, preferencias y historial
-**Seguimiento de asistencias**: Análisis de frecuencia y patrones de uso
-**Gestión de membresías**: Control del ciclo de vida del cliente (adquisición, renovación, cancelación)
-**Informes de comportamiento**: Identificación de clientes en riesgo de abandono

**``Funcionalidades ERP (Gestión de Recursos Empresariales)``**
-**Gestión de recursos humanos**: Control de entrenadores, horarios y especialidades
-**Planificación de recursos**: Organización de clases, asignación de espacios y entrenadores
- **Control financiero**: Registro de pagos de membresías y análisis de ingresos
-**Gestión de inventario**: Tipos de membresía como "productos" del gimnasio

#### **Ejemplo de Integración: Dashboard de Análisis**
```py
@app.route('/api/informes/dashboard', methods=['GET'])
def obtener_estadisticas_dashboard():
    try:
        socios = socio_model.obtener_todos()
        entrenadores = entrenador_model.obtener_todos()
        clases = clase_model.obtener_todas()
        membresias = membresia_model.obtener_todas()
        
        total_socios = len(socios)
        total_entrenadores = len(entrenadores)
        total_clases = len(clases)
        
        # Calcular ingresos del mes actual
        ingresos_mes = sum(float(m[6]) for m in membresias if m[7] == 'activa')
        
        # Contar socios con membresía activa
        socios_activos = sum(1 for s in socios if s[8] == 'Con membresía')
        
        return jsonify({
            'success': True,
            'data': {
                'total_socios': total_socios,
                'socios_activos': socios_activos,
                'total_entrenadores': total_entrenadores,
                'total_clases': total_clases,
                'ingresos_mes': ingresos_mes
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/informes/ingresos-mes', methods=['GET'])
def obtener_ingresos_por_mes():
    try:
        datos = reporte_model.ingresos_por_mes()
        reporte = []
        for item in datos:
            reporte.append({
                'mes': item[0],
                'total_membresias': item[1],
                'total_ingresos': float(item[2])
            })
        return jsonify({
            'success': True,
            'data': reporte
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/informes/membresias-vencer', methods=['GET'])
def obtener_membresias_por_vencer():
    try:
        membresias = reporte_model.membresias_por_vencer()
        membresias_dict = []
        for membresia in membresias:
            membresias_dict.append({
                'numero_socio': membresia[0],
                'socio': membresia[1],
                'telefono': membresia[2],
                'email': membresia[3],
                'fecha_fin': membresia[4],
                'tipo_membresia': membresia[5]
            })
        return jsonify({
            'success': True,
            'data': membresias_dict
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/informes/clases-populares', methods=['GET'])
def obtener_clases_populares():
    try:
        clases = reporte_model.clases_mas_populares()
        clases_dict = []
        for clase in clases:
            clases_dict.append({
                'clase': clase[0],
                'entrenador': clase[1],
                'dia_semana': clase[2],
                'hora_inicio': clase[3],
                'total_reservas': clase[4],
                'capacidad_maxima': clase[5],
                'porcentaje_ocupacion': float(clase[6])
            })
        return jsonify({
            'success': True,
            'data': clases_dict
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/informes/asistencias-mensuales', methods=['GET'])
def obtener_asistencias_mensuales():
    try:
        datos = reporte_model.asistencias_mensuales()
        reporte = []
        for item in datos:
            reporte.append({
                'mes': item[0],
                'socios_unicos': item[1],
                'total_visitas': item[2],
                'promedio_visitas': float(item[3])
            })
        return jsonify({
            'success': True,
            'data': reporte
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

---

Este sistema de gestión de gimnasio representa, yo creo, mucho más que un ejercicio del ciclo, es un `ejemplo tangible y que además funciona` de cómo los sistemas ERP-CRM transforman la gestión empresarial moderna, automatizando procesos operativos, y manejando información centralizada en repositórios únicos.

La experiencia de contruir un sistema más completo, proporciona mucha comprensión que a veces es difícil de obtener mediante el estudio teórico. Entender cómo una acción del usuario en el frontend desencadena una cascada de operaciones que atraviesan capas de software, ejecutan consultas SQL y finalmente persisten información en una base de datos, para luego retornar una respuesta visualizable, es fundamental para cualquier profesional del desarrollo de software.

En definitiva, este proyecto consolida la transición del conocimiento conceptual sobre sistemas ERP-CRM hacia la **``capacidad práctica de diseñar, implementar y mantener``** soluciones empresariales reales, preparando el camino para afrontar con solvencia los desafíos técnicos del desarrollo de aplicaciones empresariales en contextos profesionales.