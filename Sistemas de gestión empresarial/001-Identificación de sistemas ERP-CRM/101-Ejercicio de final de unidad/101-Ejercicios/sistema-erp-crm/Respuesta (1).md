El proyecto consiste en el desarrollo de un sistema de gestión empresarial orientado a un gimnasio. Su finalidad es centralizar y automatizar procesos clave como la gestión de socios, entrenadores, clases, membresías, asistencias e informes.  
Este sistema se utiliza en contextos donde la organización requiere controlar operaciones internas mediante un panel unificado accesible desde navegador.

---

El sistema sigue una arquitectura **cliente-servidor** compuesta por:
- **Backend (Python + Flask)**: expone una API REST con operaciones CRUD para todas las entidades.
- **Base de datos SQLite**: almacena socios, entrenadores, clases, membresías, asistencias y reportes.
- **Frontend (HTML/CSS/JS)**: consume la API y muestra la información de forma estructurada y usable.

### Funcionamiento del backend
El archivo `app.py` define endpoints como:
```python
@app.route('/api/socios', methods=['GET'])
def obtener_socios():
    socios = socio_model.obtener_todos()
    return jsonify({'success': True, 'data': socios})
```
Los modelos contenidos en `models.py` encapsulan la lógica de acceso a datos, por ejemplo la creación de un socio:
```python
def crear(self, numero_socio, nombre, apellidos, email=None, telefono=None, ...):
    cursor.execute('INSERT INTO socios (...) VALUES (...)')
```

### Funcionamiento del frontend
El archivo `script.js` implementa controladores para cada módulo.  
Ejemplo de carga dinámica de socios:
```javascript
const response = await fetch(`${API_BASE}/socios`);
appState.datos.socios = data.data;
sociosController.renderizarSocios(data.data);
```

### Diseño
El estilo se gestiona desde `style.css`, usando un diseño responsive y componentes reutilizables como tarjetas, tablas y alertas.

---

En ejecución, el sistema permite:
- Registrar un nuevo socio mediante la API.
- Consultar clases activas, su capacidad y disponibilidad.
- Generar informes: ingresos por mes, asistencias, clases populares.

### Ejemplo de uso real
Crear una membresía desde frontend:
```javascript
fetch(`${API_BASE}/membresias`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
      socio_id: 1,
      tipo_membresia_id: 2,
      fecha_inicio: "2025-01-10",
      duracion_meses: 1,
      precio_pagado: 45.00
  })
});
```

### Errores comunes y prevención
- **Campos vacíos en el formulario** → Validar antes de enviar al backend.
- **IDs incorrectos** → El backend responde con error 404 si no existen.
- **Bloqueo CORS** → Resuelto mediante `CORS(app)` en Flask.

---

El sistema desarrollado integra los contenidos de la unidad: conceptos ERP/CRM, arquitectura multicapa, API REST, diseño de base de datos y gestión de procesos.  
Permite automatizar operaciones internas del gimnasio, demostrando el valor de los sistemas de gestión empresarial.

