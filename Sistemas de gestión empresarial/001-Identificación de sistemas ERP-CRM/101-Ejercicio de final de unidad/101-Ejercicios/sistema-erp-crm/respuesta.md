Un **Sistema ERP-CRM** es una solución informática integral que combina dos tipos de sistemas empresariales fundamentales:

- **ERP (Enterprise Resource Planning)**: Sistema de planificación de recursos empresariales que integra y gestiona los procesos operativos internos de una organización (inventario, producción, contabilidad, recursos humanos, etc.).

- **CRM (Customer Relationship Management)**: Sistema de gestión de relaciones con clientes que centraliza y optimiza las interacciones con los clientes, mejorando las ventas, el marketing y el servicio al cliente.

### Contexto de Uso

Este tipo de sistemas se utiliza en empresas que necesitan:
- Centralizar la información de múltiples departamentos en una única plataforma
- Mejorar la eficiencia operativa mediante la automatización de procesos
- Tener visibilidad en tiempo real del estado del negocio
- Optimizar las relaciones con clientes y mejorar su experiencia
- Tomar decisiones basadas en datos confiables y actualizados

En el caso específico de este proyecto, se ha desarrollado un sistema ERP-CRM adaptado a las necesidades de un **gimnasio**, integrando funcionalidades de gestión interna (ERP) como control de entrenadores, clases y membresías, con capacidades de gestión de socios (CRM) como registro de datos personales, seguimiento de asistencias y análisis de comportamiento.

---

### Arquitectura del Sistema

El proyecto implementa una **arquitectura cliente-servidor de tres capas**:

#### **Capa de Presentación (Frontend)**
- **Tecnologías**: HTML5, CSS3, JavaScript ES6+
- **Función**: Interfaz de usuario responsive que permite la interacción con el sistema
- **Características**:
  - Diseño modular con sistema de navegación por secciones
  - Formularios dinámicos para entrada de datos
  - Visualización de información mediante tablas y tarjetas (cards)
  - Interfaz tipo SPA (Single Page Application) para mejor experiencia de usuario

#### **Capa de Lógica de Negocio (Backend)**
- **Tecnologías**: Python 3.x con Flask
- **Función**: API REST que procesa las solicitudes del frontend y coordina operaciones con la base de datos
- **Características**:
  - Endpoints RESTful organizados por entidades
  - Manejo de CORS para comunicación cross-origin
  - Validación de datos antes de persistirlos
  - Gestión de errores con respuestas HTTP apropiadas

#### **Capa de Datos (Database)**
- **Tecnologías**: SQLite
- **Función**: Almacenamiento persistente de información
- **Características**:
  - Modelo relacional normalizado
  - Tablas con relaciones de integridad referencial
  - Índices para optimización de consultas

### Modelo de Datos Relacional

El sistema implementa las siguientes entidades principales:

#### **Tabla: socios (Módulo CRM)**
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
**Función CRM**: Centraliza toda la información de los clientes (socios) del gimnasio, permitiendo segmentación, análisis de comportamiento y personalización de servicios.

#### **Tabla: entrenadores (Módulo ERP)**
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
**Función ERP**: Gestiona los recursos humanos especializados del gimnasio, controlando disponibilidad, especialidades y asignación a clases.

#### **Tabla: clases (Módulo ERP)**
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
**Función ERP**: Planifica y organiza los recursos (entrenadores, horarios, espacios) para las actividades grupales.

#### **Tabla: membresias (Módulo ERP-CRM)**
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
**Función mixta**: Integra ERP (control financiero, inventario de servicios) con CRM (seguimiento del ciclo de vida del cliente).

#### **Tabla: asistencias (Módulo CRM)**
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
**Función CRM**: Registra el comportamiento y nivel de engagement de los socios para análisis de fidelización.

### Funcionalidad de la API REST

La API implementa el patrón **CRUD** (Create, Read, Update, Delete) para cada entidad:

#### **Ejemplo: Endpoint para Socios**

**1. Crear Socio (POST /api/socios)**
```python
@app.route('/api/socios', methods=['POST'])
def crear_socio():
    try:
        data = request.get_json()
        socio_id = socio_model.crear(
            numero_socio=data['numero_socio'],
            nombre=data['nombre'],
            apellidos=data['apellidos'],
            email=data.get('email'),
            telefono=data.get('telefono'),
            fecha_nacimiento=data.get('fecha_nacimiento'),
            direccion=data.get('direccion'),
            ciudad=data.get('ciudad')
        )
        return jsonify({
            'success': True,
            'data': {'id': socio_id},
            'message': 'Socio creado correctamente'
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

**Flujo de operación:**
1. El frontend envía una petición POST con datos JSON del nuevo socio
2. Flask recibe la petición y extrae los datos con `request.get_json()`
3. Se validan y pasan al modelo `Socio` que ejecuta la inserción SQL
4. Se retorna una respuesta JSON con el ID generado o un mensaje de error

**2. Leer Socios (GET /api/socios)**
```python
@app.route('/api/socios', methods=['GET'])
def obtener_socios():
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

**Flujo de operación:**
1. El frontend solicita la lista completa de socios
2. El backend consulta la base de datos mediante el modelo
3. Convierte las tuplas SQL en diccionarios Python
4. Serializa a JSON y envía al frontend

### Capa de Acceso a Datos (Models)

Los modelos implementan el **patrón DAO (Data Access Object)**, encapsulando todas las operaciones SQL:

```python
class Socio:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def crear(self, numero_socio, nombre, apellidos, email=None, telefono=None, 
              fecha_nacimiento=None, direccion=None, ciudad=None):
        """Crea un nuevo socio"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO socios (numero_socio, nombre, apellidos, email, telefono, 
                               fecha_nacimiento, direccion, ciudad)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (numero_socio, nombre, apellidos, email, telefono, 
              fecha_nacimiento, direccion, ciudad))
        
        socio_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return socio_id
```

**Ventajas de este patrón:**
- **Separación de responsabilidades**: La lógica SQL está aislada del código de negocio
- **Reutilización**: Los métodos pueden llamarse desde múltiples endpoints
- **Mantenibilidad**: Cambios en el esquema solo requieren modificar los modelos
- **Seguridad**: Uso de consultas parametrizadas previene SQL Injection

### Frontend Interactivo

El frontend implementa **programación orientada a objetos** para organizar la lógica:

```javascript
class SociosController {
    async cargarSocios() {
        try {
            const response = await fetch(`${API_BASE}/socios`);
            const data = await response.json();
            
            if (data.success) {
                appState.datos.socios = data.data;
                this.renderizarSocios(data.data);
            } else {
                this.mostrarError(data.error);
            }
        } catch (error) {
            console.error('Error al cargar socios:', error);
            this.mostrarError('Error de conexión con el servidor');
        }
    }
    
    renderizarSocios(socios) {
        const container = document.getElementById('socios-lista');
        container.innerHTML = '';
        
        socios.forEach(socio => {
            const card = this.crearTarjetaSocio(socio);
            container.appendChild(card);
        });
    }
    
    crearTarjetaSocio(socio) {
        const card = document.createElement('div');
        card.className = 'socio-card';
        card.innerHTML = `
            <h3>${socio.nombre} ${socio.apellidos}</h3>
            <p>Nº Socio: ${socio.numero_socio}</p>
            <p>Email: ${socio.email}</p>
            <p>Estado: <span class="badge ${socio.estado}">${socio.estado}</span></p>
            <p>Membresía: ${socio.estado_membresia}</p>
        `;
        return card;
    }
}
```

**Características clave:**
- **Programación asíncrona** con `async/await` para peticiones HTTP
- **Manipulación del DOM** dinámica sin recargar la página
- **Gestión de estado** centralizada en el objeto `appState`
- **Separación de responsabilidades**: carga de datos, renderizado y eventos en métodos distintos

---

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

```javascript
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
```python
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
```python
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

-- Resultado: Nuevo registro con ID=1
```

#### **Paso 6: Respuesta llega al Frontend**
```javascript
// El frontend recibe:
{
    "success": true,
    "data": {"id": 1},
    "message": "Socio creado correctamente"
}

// Y actualiza la interfaz mostrando el nuevo socio en la lista
```

### Ejemplo Real: Consulta Compleja con JOIN

Una de las funcionalidades más importantes es **obtener socios con su estado de membresía**. Esto requiere una consulta SQL con JOIN:

```python
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

**Explicación de la consulta:**
1. **SELECT**: Selecciona campos de la tabla socios y calcula el estado de membresía
2. **CASE WHEN**: Lógica condicional SQL que verifica si la fecha de fin de membresía es futura
3. **LEFT JOIN**: Incluye todos los socios, incluso los que no tienen membresía activa
4. **AND m.estado = 'activa'**: Filtra solo membresías activas en el JOIN
5. **ORDER BY fecha_registro DESC**: Ordena por fecha de registro descendente (más recientes primero)

**Resultado esperado:**
```
| id | numero_socio | nombre | apellidos | email | telefono | ciudad | estado | estado_membresia |
|----|--------------|--------|-----------|-------|----------|--------|--------|------------------|
| 1  | SOC-001      | Juan   | Pérez     | ...   | ...      | Madrid | activo | Con membresía    |
| 2  | SOC-002      | María  | García    | ...   | ...      | Madrid | activo | Sin membresía    |
```

### Errores Comunes y Cómo Evitarlos

#### **Error 1: SQL Injection**
**❌ Código vulnerable:**
```python
# NUNCA HACER ESTO
def crear_socio_inseguro(self, nombre):
    query = f"INSERT INTO socios (nombre) VALUES ('{nombre}')"
    cursor.execute(query)
```

**Problema:** Si un usuario malicioso ingresa `'); DROP TABLE socios; --` como nombre, destruiría la tabla.

**✅ Solución correcta:**
```python
# Usar parámetros
cursor.execute("INSERT INTO socios (nombre) VALUES (?)", (nombre,))
```

#### **Error 2: No cerrar conexiones a la base de datos**
**❌ Código problemático:**
```python
def obtener_socios(self):
    conn = self.db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM socios")
    return cursor.fetchall()
    # Falta conn.close() - ¡Memory leak!
```

**✅ Solución correcta:**
```python
def obtener_socios(self):
    conn = self.db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM socios")
    socios = cursor.fetchall()
    conn.close()  # Siempre cerrar
    return socios
```

#### **Error 3: No manejar errores de conexión en el Frontend**
**❌ Código sin manejo de errores:**
```javascript
async function cargarSocios() {
    const response = await fetch('/api/socios');
    const data = await response.json();
    renderizarSocios(data.data);
}
```

**Problema:** Si el servidor está caído, la aplicación se congela sin informar al usuario.

**✅ Solución correcta:**
```javascript
async function cargarSocios() {
    try {
        const response = await fetch('/api/socios');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (data.success) {
            renderizarSocios(data.data);
        } else {
            mostrarError(data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        mostrarError('No se pudo conectar con el servidor');
    }
}
```

#### **Error 4: No validar datos antes de insertar**
**❌ Código sin validación:**
```python
@app.route('/api/socios', methods=['POST'])
def crear_socio():
    data = request.get_json()
    socio_id = socio_model.crear(**data)  # Inserta sin validar
    return jsonify({'id': socio_id})
```

**✅ Solución correcta:**
```python
@app.route('/api/socios', methods=['POST'])
def crear_socio():
    data = request.get_json()
    
    # Validaciones
    if not data.get('nombre') or not data.get('apellidos'):
        return jsonify({
            'success': False,
            'error': 'Nombre y apellidos son obligatorios'
        }), 400
    
    if data.get('email') and '@' not in data['email']:
        return jsonify({
            'success': False,
            'error': 'Email inválido'
        }), 400
    
    socio_id = socio_model.crear(**data)
    return jsonify({'success': True, 'id': socio_id})
```

#### **Error 5: CORS no configurado**
**Problema:** El navegador bloquea peticiones del frontend al backend por política de mismo origen.

**✅ Solución:**
```python
# app.py
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permitir peticiones desde otros orígenes
```

### Integración ERP-CRM en el Proyecto

Este proyecto demuestra la **integración práctica de funcionalidades ERP y CRM**:

#### **Funcionalidades CRM (Gestión de Relación con Clientes)**
1. **Base de datos de socios**: Perfil completo con datos de contacto, preferencias y historial
2. **Seguimiento de asistencias**: Análisis de frecuencia y patrones de uso
3. **Gestión de membresías**: Control del ciclo de vida del cliente (adquisición, renovación, cancelación)
4. **Informes de comportamiento**: Identificación de clientes en riesgo de abandono

#### **Funcionalidades ERP (Gestión de Recursos Empresariales)**
1. **Gestión de recursos humanos**: Control de entrenadores, horarios y especialidades
2. **Planificación de recursos**: Organización de clases, asignación de espacios y entrenadores
3. **Control financiero**: Registro de pagos de membresías y análisis de ingresos
4. **Gestión de inventario**: Tipos de membresía como "productos" del gimnasio

#### **Ejemplo de Integración: Dashboard de Análisis**
```python
# Endpoint que combina datos ERP y CRM
@app.route('/api/informes/dashboard', methods=['GET'])
def obtener_dashboard():
    # Datos CRM
    total_socios = socio_model.contar_activos()
    socios_nuevos_mes = socio_model.contar_nuevos_mes()
    
    # Datos ERP
    total_entrenadores = entrenador_model.contar_activos()
    total_clases = clase_model.contar_activas()
    ingresos_mes = membresia_model.calcular_ingresos_mes()
    
    # Análisis integrado
    tasa_ocupacion = asistencia_model.calcular_tasa_ocupacion()
    
    return jsonify({
        'success': True,
        'data': {
            'crm': {
                'total_socios': total_socios,
                'socios_nuevos': socios_nuevos_mes
            },
            'erp': {
                'total_entrenadores': total_entrenadores,
                'total_clases': total_clases,
                'ingresos_mes': ingresos_mes,
                'tasa_ocupacion': tasa_ocupacion
            }
        }
    })
```

---

### Puntos Clave del Proyecto

1. **Arquitectura multicapa**: El proyecto implementa correctamente una separación clara entre presentación (frontend), lógica de negocio (backend) y datos (database), siguiendo principios de ingeniería de software moderna.

2. **Integración ERP-CRM**: Se demuestra cómo un mismo sistema puede gestionar tanto procesos internos (ERP: entrenadores, clases, recursos) como relaciones con clientes (CRM: socios, membresías, asistencias).

3. **API REST como puente**: El uso de una API REST permite la comunicación eficiente entre frontend y backend, facilitando la escalabilidad y el mantenimiento del sistema.

4. **Modelo de datos relacional**: El diseño normalizado de la base de datos con relaciones de integridad referencial garantiza la consistencia de los datos y evita redundancias.

5. **Buenas prácticas de seguridad**: Uso de consultas parametrizadas, validación de datos y manejo apropiado de errores protege el sistema de vulnerabilidades comunes.

### Relación con Contenidos de la Unidad

Este proyecto integra múltiples conceptos vistos en la unidad **"Identificación de sistemas ERP-CRM"**:

- **Características de sistemas ERP**: Gestión integrada de recursos (entrenadores, clases, instalaciones)
- **Características de sistemas CRM**: Base de datos de clientes, seguimiento de interacciones, análisis de comportamiento
- **Módulos típicos**: El sistema incluye módulos equivalentes a los de un ERP-CRM comercial (gestión de contactos, ventas/membresías, recursos humanos, informes)
- **Arquitectura de tres capas**: Implementación práctica de la arquitectura estándar en sistemas empresariales
- **Acceso a datos**: Aplicación de técnicas de persistencia, operaciones CRUD y consultas SQL complejas
- **Interfaces de usuario**: Desarrollo de una interfaz web profesional que permite la interacción eficiente con el sistema

### Proyección Profesional

Los conocimientos aplicados en este proyecto son directamente transferibles al mundo laboral:

- **Desarrollo full-stack**: Capacidad de trabajar en todas las capas de una aplicación empresarial
- **Integración de sistemas**: Habilidad para conectar diferentes componentes mediante APIs
- **Análisis de requisitos**: Traducción de necesidades de negocio en funcionalidades técnicas
- **Mantenimiento y escalabilidad**: Código organizado que facilita futuras ampliaciones

Este sistema de gestión de gimnasio es un ejemplo funcional de cómo los sistemas ERP-CRM modernizan la gestión empresarial, automatizando procesos, centralizando información y proporcionando herramientas de análisis que mejoran la toma de decisiones estratégicas.