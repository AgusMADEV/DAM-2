# Ejercicio Final de Unidad 2: Componente de Acceso a Datos

**Alumno:** [Tu Nombre]  
**Fecha:** 13 de noviembre de 2025  
**Unidad:** 002-Manejo de conectores  

---

## 1. Introducción breve y contextualización

### Concepto General

El **componente de acceso a datos** que he desarrollado es una abstracción que facilita la interacción entre aplicaciones Python y bases de datos MySQL. Este componente implementa el patrón **Data Access Object (DAO)** combinado con principios del **mapeo objeto-relacional (ORM)**, proporcionando una interfaz simplificada para operaciones CRUD sin exponer la complejidad del SQL directo.

### Contexto de Uso

Este tipo de componentes se utiliza en:
- **Desarrollo de APIs web** (Flask, Django, FastAPI) para gestionar la persistencia de datos
- **Aplicaciones de escritorio** que requieren almacenamiento relacional
- **Microservicios** que necesitan una capa de abstracción de base de datos
- **Sistemas empresariales** donde se requiere separar la lógica de negocio del acceso a datos

El objetivo principal es resolver el **desfase objeto-relacional** mencionado en la unidad, proporcionando una interfaz orientada a objetos para trabajar con estructuras relacionales.

---

## 2. Desarrollo detallado y preciso

### Definiciones y Terminología Técnica

**Componente de Acceso a Datos:** Capa de software que encapsula la lógica necesaria para interactuar con sistemas de almacenamiento persistente, proporcionando operaciones de alto nivel independientes del motor de base de datos específico.

**Patrón DAO:** Patrón de diseño que proporciona una interfaz abstracta para acceder a datos, ocultando los detalles de implementación del mecanismo de persistencia.

**ORM (Object-Relational Mapping):** Técnica de programación que permite convertir datos entre sistemas incompatibles (objetos en memoria vs. tablas relacionales).

### Arquitectura del Componente

Mi implementación (`AMA`) sigue esta estructura:

```python
class AMA():
    """
    Clase principal de acceso a datos basada en el patrón visto en clase.
    Proporciona métodos simples para operaciones con MySQL.
    """
    
    # Validación de seguridad
    _re_ident = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
    
    def __init__(self, host, usuario, contrasena, basedatos):
        # Establecimiento de conexión persistente
        
    def _validar_ident(self, nombre):
        # Validación de identificadores SQL para seguridad
```

### Funcionamiento Paso a Paso

#### 1. **Inicialización y Conexión**
```python
conexion = AMA("localhost", "usuario", "password", "database")
```
- Establece conexión MySQL usando `mysql.connector`
- Crea cursor persistente para operaciones
- Almacena credenciales para reconexión si es necesario

#### 2. **Operaciones CRUD**

**CREATE (Insertar):**
```python
usuario_id = conexion.insertar("usuarios", {
    "nombre": "Ana García",
    "email": "ana@example.com",
    "edad": 28
})
```
- Valida identificadores con regex
- Construye SQL dinámicamente usando placeholders
- Retorna ID del registro insertado

**READ (Consultar):**
```python
# Selección completa
usuarios = conexion.seleccionar("usuarios")

# Búsqueda con criterio
resultados = conexion.buscar("usuarios", "email", "ana")
```
- Ejecuta consultas SELECT
- Convierte resultados a diccionarios Python
- Serializa automáticamente a JSON

**UPDATE (Actualizar):**
```python
filas_afectadas = conexion.actualizar(
    "usuarios",
    {"edad": 29},           # Datos a cambiar
    {"id": usuario_id}      # Condiciones WHERE
)
```
- Construye cláusulas SET y WHERE dinámicamente
- Usa parametrización para evitar inyección SQL
- Retorna número de filas afectadas

**DELETE (Eliminar):**
```python
eliminados = conexion.eliminar("usuarios", {"id": usuario_id})
```
- Requiere condiciones obligatorias (seguridad)
- Confirma cambios con `commit()`
- Retorna cantidad de registros eliminados

#### 3. **Gestión de Metadatos**
```python
# Listar tablas
tablas = conexion.tablas()

# Describir estructura
estructura = conexion.describir("usuarios")
```

#### 4. **SQL Personalizado**
```python
# Para consultas complejas
resultados = conexion.ejecutar_sql(
    "SELECT COUNT(*) as total FROM usuarios WHERE activo = %s",
    (True,)
)
```

### Características Técnicas Implementadas

1. **Seguridad:**
   - Validación de identificadores con expresiones regulares
   - Uso obligatorio de placeholders para prevenir inyección SQL
   - Validación de entrada en todos los métodos

2. **Robustez:**
   - Manejo de errores con mensajes descriptivos
   - Validaciones de datos antes de operaciones
   - Gestión automática de transacciones

3. **Usabilidad:**
   - Interfaz simple y consistente
   - Conversión automática a JSON
   - Documentación completa en docstrings

---

## 3. Aplicación práctica

### Implementación Real en Proyecto

He desarrollado un ejemplo completo de uso (`demo_usage.py`) que muestra la integración práctica:

```python
from data_access_component import AMA

def main():
    # Conexión
    conexion = AMA("localhost", "usuario", "password", "database")
    
    try:
        # Crear tabla de ejemplo
        conexion.ejecutar_sql("""
            CREATE TABLE IF NOT EXISTS usuarios_ama (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                edad INT,
                activo BOOLEAN DEFAULT TRUE
            )
        """)
        
        # Insertar datos
        usuario_id = conexion.insertar("usuarios_ama", {
            "nombre": "Ana García",
            "email": "ana@example.com",
            "edad": 28
        })
        
        # Consultar datos
        usuarios = conexion.seleccionar("usuarios_ama")
        print(usuarios)  # Output: JSON formateado
        
    finally:
        conexion.cerrar()
```

### Integración en API Web (Ejemplo Flask)

```python
from flask import Flask, jsonify
from data_access_component import AMA

app = Flask(__name__)
db = AMA("localhost", "usuario", "password", "database")

@app.route('/api/usuarios')
def obtener_usuarios():
    usuarios_json = db.seleccionar("usuarios")
    return usuarios_json  # Ya está en formato JSON

@app.route('/api/usuarios', methods=['POST'])
def crear_usuario():
    datos = request.json
    usuario_id = db.insertar("usuarios", datos)
    return {"id": usuario_id}, 201
```

### Errores Comunes y Cómo Evitarlos

#### ❌ **Error 1: Inyección SQL**
```python
# INCORRECTO
sql = f"SELECT * FROM usuarios WHERE nombre = '{nombre}'"
cursor.execute(sql)
```

#### ✅ **Solución:** Usar placeholders
```python
# CORRECTO - Mi implementación
sql = "SELECT * FROM usuarios WHERE nombre = %s"
cursor.execute(sql, (nombre,))
```

#### ❌ **Error 2: No cerrar conexiones**
```python
# INCORRECTO
conexion = AMA(...)
# ... usar conexion ...
# No cerrar -> memory leaks
```

#### ✅ **Solución:** Gestión de recursos
```python
# CORRECTO
try:
    conexion = AMA(...)
    # ... operaciones ...
finally:
    conexion.cerrar()
```

#### ❌ **Error 3: Identificadores no validados**
```python
# INCORRECTO - vulnerable a inyección
tabla = "usuarios; DROP TABLE usuarios; --"
sql = f"SELECT * FROM {tabla}"
```

#### ✅ **Solución:** Validación con regex (mi implementación)
```python
# CORRECTO
def _validar_ident(self, nombre):
    if not self._re_ident.match(nombre):
        raise ValueError(f"Identificador inválido: {nombre}")
```

### Comparación con Enfoques Anteriores

**Antes (Enfoque básico visto en clase):**
```python
# Código repetitivo para cada operación
cursor.execute("SELECT * FROM usuarios")
filas = cursor.fetchall()
# Manejo manual de resultados
```

**Ahora (Mi componente):**
```python
# Una línea, resultado automático en JSON
usuarios = conexion.seleccionar("usuarios")
```

### Beneficios Demostrados

1. **Reutilización:** Una vez configurado, se puede usar en cualquier proyecto
2. **Mantenibilidad:** Cambios centralizados en una sola clase
3. **Seguridad:** Validaciones automáticas integradas
4. **Productividad:** Reduce código repetitivo significativamente

---

## 4. Conclusión breve

### Puntos Clave

El componente `AMA` que he desarrollado logra exitosamente:

1. **Abstracción efectiva:** Oculta la complejidad del SQL directo manteniendo flexibilidad
2. **Aplicación práctica de la unidad:** Integra todos los conceptos vistos desde el desfase objeto-relacional hasta la gestión de transacciones
3. **Solución production-ready:** Incluye validaciones de seguridad, manejo de errores y documentación completa
4. **Patrón escalable:** Base sólida para futuras extensiones (pooling de conexiones, múltiples SGBD, etc.)

### Enlace con Contenidos de la Unidad

Este proyecto sintetiza **todos los temas tratados en la unidad 002**:

- **Unidad 001 (Desfase objeto-relacional):** Resuelto mediante la conversión automática objeto ↔ JSON ↔ SQL
- **Unidad 002 (Protocolos de acceso):** Implementado con `mysql.connector` siguiendo buenas prácticas
- **Unidad 003 (Establecimiento de conexiones):** Gestión automática en constructor y método `cerrar()`
- **Unidades 004-006 (Sentencias SQL):** Encapsuladas en métodos específicos con validación
- **Unidad 008 (Gestión de transacciones):** Commits automáticos en operaciones de modificación

### Proyección Futura

Este componente constituye una **base sólida para el desarrollo de aplicaciones de acceso a datos** que puede evolucionar hacia:
- Soporte para múltiples SGBD (PostgreSQL, SQLite, etc.)
- Pool de conexiones para mejor rendimiento
- Sistema de caché para optimizar consultas frecuentes
- Integración con frameworks ORM más complejos

**El objetivo de crear un "componente abstraído de acceso a datos integrable en el back de un proyecto" ha sido cumplido completamente**, proporcionando una solución práctica, segura y eficiente para el manejo de conectores de base de datos.

---

## Archivos del Proyecto

- `data_access_component.py`: Implementación completa de la clase AMA
- `demo_usage.py`: Demostración práctica con ejemplos de uso
- `Respuesta.md`: Esta documentación técnica

**Total de líneas de código:** ~500 líneas (incluyendo documentación y ejemplos)