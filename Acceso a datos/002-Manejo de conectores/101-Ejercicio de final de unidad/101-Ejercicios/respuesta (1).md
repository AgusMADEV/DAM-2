He desarrollado un **componente de acceso a datos** llamado `AMA` (en `AMA.py`) que encapsula operaciones habituales contra **MySQL**: conexión, consultas, **CRUD** (insertar/seleccionar/actualizar/eliminar), introspección de tablas y ejecución de SQL personalizado. El componente devuelve los resultados en **JSON** para facilitar su integración con servicios web y capas de presentación.

**¿Para qué sirve y en qué contexto se usa?**  
Sirve como **librería integrable en el backend** de cualquier proyecto Python que necesite persistir y recuperar información desde MySQL. Lo empleo en un **escenario de aplicación** tipo “usuarios”, mostrando un flujo completo de *setup → inserciones → consultas → actualización → estadísticas* tal como demuestro en `demo_usage.py`.

---

### Diseño, validación y seguridad básica
- La clase principal es `AMA`, con conexión gestionada mediante `mysql.connector.connect(...)` y *cursor* dedicado.  
- Para **higiene de SQL** implemento `_validar_ident()` con una **expresión regular** segura `^[A-Za-z_][A-Za-z0-9_]*$` que restringe nombres de **tablas/columnas** a identificadores válidos.
- Todas las consultas que reciben datos del usuario usan **parámetros** (`%s`) para evitar inyecciones SQL, por ejemplo en `buscar()` y en `ejecutar_sql()` cuando paso `parametros`.

Fragmentos de código del proyecto que ilustran lo anterior:

```python
# AMA.py
_re_ident = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
def _validar_ident(self, nombre):
    if not isinstance(nombre, str) or not self._re_ident.match(nombre):
        raise ValueError(f"Identificador inválido: {nombre!r}")
```

```python
# AMA.py (búsqueda parametrizada)
sql = f"SELECT * FROM `{tabla}` WHERE `{columna}` LIKE %s"
self.cursor.execute(sql, (f"%{valor}%",))
```

### API del componente (métodos principales)

- **Conexión y cierre**
  - `__init__(host, usuario, contrasena, basedatos)`: establece conexión y cursor.
  - `cerrar()`: cierra cursor y conexión de forma segura.

- **Lectura**
  - `seleccionar(tabla)`: `SELECT *` de la tabla indicada → **JSON** (lista de diccionarios).
  - `buscar(tabla, columna, valor)`: `LIKE` parametrizado sobre una columna → **JSON**.
  - `tablas()`: `SHOW TABLES` → **JSON** con `{ "tabla": <nombre> }`.
  - `describir(tabla)`: `DESCRIBE <tabla>` → **JSON** con metadatos de columnas.

- **Escritura y mantenimiento**
  - `insertar(tabla, datos: dict)`: **INSERT** parametrizado. Valida identificadores y columnas; devuelve `lastrowid`.
  - `actualizar(tabla, datos: dict, condiciones: dict)`: **UPDATE** con `SET`/`WHERE` parametrizados; devuelve filas afectadas.
  - `eliminar(tabla, condiciones: dict)`: **DELETE** parametrizado; devuelve filas eliminadas.

- **SQL personalizado**
  - `ejecutar_sql(sql, parametros=None)`: ejecuta **cualquier** SQL; si es `SELECT` devuelve **JSON**, si no, devuelve filas afectadas (y hace `commit`).

```python
# AMA.py
def seleccionar(self, tabla):
    self._validar_ident(tabla)
    self.cursor.execute(f"SELECT * FROM `{tabla}`")
    columnas = self.cursor.column_names
    filas = self.cursor.fetchall()
    datos = [dict(zip(columnas, fila)) for fila in filas]
    return json.dumps(datos, ensure_ascii=False, indent=2, default=str)
```

```python
# AMA.py
def insertar(self, tabla, datos):
    self._validar_ident(tabla)
    for columna in datos.keys():
        self._validar_ident(columna)
    columnas = list(datos.keys())
    valores = list(datos.values())
    placeholders = ', '.join(['%s'] * len(valores))
    sql = f"INSERT INTO `{tabla}` ({', '.join([f'`{c}`' for c in columnas])}) VALUES ({placeholders})"
    self.cursor.execute(sql, valores)
    self.conexion.commit()
    return self.cursor.lastrowid
```

### Flujo de funcionamiento (paso a paso, según `demo_usage.py`)

1. **Conexión**:
   ```python
   conexion = AMA(host="localhost", usuario="futbol_amadev",
                  contrasena="futbol_amadev", basedatos="futbol_amadev")
   ```

2. **Inspección inicial** de tablas:
   ```python
   tablas_json = conexion.tablas()
   ```

3. **Creación de tabla** de ejemplo (SQL personalizado):
   ```python
   sql_crear_tabla = """
   CREATE TABLE IF NOT EXISTS usuarios_ama (
       id INT AUTO_INCREMENT PRIMARY KEY,
       nombre VARCHAR(100) NOT NULL,
       email VARCHAR(100) NOT NULL,
       edad INT,
       activo BOOLEAN DEFAULT TRUE
   )
   """
   conexion.ejecutar_sql(sql_crear_tabla)
   ```

4. **Inserciones** con `insertar(...)`:
   ```python
   usuario1_id = conexion.insertar("usuarios_ama", {
       "nombre": "Ana García",
       "email": "ana@example.com",
       "edad": 28,
       "activo": True
   })
   ```

5. **Selección** y **búsqueda**:
   ```python
   usuarios = conexion.seleccionar("usuarios_ama")
   busqueda = conexion.buscar("usuarios_ama", "email", "ana")
   ```

6. **Actualización** y nueva lectura:
   ```python
   filas_actualizadas = conexion.actualizar(
       "usuarios_ama",
       {"edad": 29, "email": "ana.garcia@example.com"},
       {"id": usuario1_id}
   )
   usuarios_actualizados = conexion.seleccionar("usuarios_ama")
   ```

7. **Consultas personalizadas** (p. ej., usuarios activos) y **DESCRIBE**:
   ```python
   usuarios_activos = conexion.ejecutar_sql(
       "SELECT nombre, email, edad FROM usuarios_ama WHERE activo = %s ORDER BY edad",
       (True,)
   )
   estructura = conexion.describir("usuarios_ama") 
   ```

8. **Cierre**:
   ```python
   conexion.cerrar()
   ```

---

```py
import mysql.connector
import json
import re


class AMA():
    _re_ident = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
    
    def __init__(self, host, usuario, contrasena, basedatos):
        self.host = host
        self.usuario = usuario
        self.contrasena = contrasena
        self.basedatos = basedatos
        
        # Establecer conexión
        self.conexion = mysql.connector.connect(
            host=self.host,
            user=self.usuario,
            password=self.contrasena,
            database=self.basedatos
        )
        
        self.cursor = self.conexion.cursor()
    
    def _validar_ident(self, nombre):
        if not isinstance(nombre, str) or not self._re_ident.match(nombre):
            raise ValueError(f"Identificador inválido: {nombre!r}")
    
    def seleccionar(self, tabla):
        self._validar_ident(tabla)
        self.cursor.execute(f"SELECT * FROM `{tabla}`")
        columnas = self.cursor.column_names
        filas = self.cursor.fetchall()
        
        # Convertir a lista de diccionarios
        datos = [dict(zip(columnas, fila)) for fila in filas]
        
        return json.dumps(datos, ensure_ascii=False, indent=2, default=str)
    
    def buscar(self, tabla, columna, valor):
        self._validar_ident(tabla)
        self._validar_ident(columna)
        
        sql = f"SELECT * FROM `{tabla}` WHERE `{columna}` LIKE %s"
        self.cursor.execute(sql, (f"%{valor}%",))
        columnas = self.cursor.column_names
        filas = self.cursor.fetchall()
        
        # Convertir a lista de diccionarios
        datos = [dict(zip(columnas, fila)) for fila in filas]
        
        return json.dumps(datos, ensure_ascii=False, indent=2, default=str)
    
    def insertar(self, tabla, datos):
        self._validar_ident(tabla)
        
        if not datos:
            raise ValueError("Los datos no pueden estar vacíos")
        
        # Validar nombres de columnas
        for columna in datos.keys():
            self._validar_ident(columna)
        
        columnas = list(datos.keys())
        valores = list(datos.values())
        placeholders = ', '.join(['%s'] * len(valores))
        
        sql = f"INSERT INTO `{tabla}` ({', '.join([f'`{c}`' for c in columnas])}) VALUES ({placeholders})"
        self.cursor.execute(sql, valores)
        self.conexion.commit()
        
        return self.cursor.lastrowid
    
    def actualizar(self, tabla, datos, condiciones):
        self._validar_ident(tabla)
        
        if not datos:
            raise ValueError("Los datos a actualizar no pueden estar vacíos")
        if not condiciones:
            raise ValueError("Las condiciones no pueden estar vacías")
        
        # Validar identificadores
        for columna in list(datos.keys()) + list(condiciones.keys()):
            self._validar_ident(columna)
        
        # Construir SET
        set_clauses = [f"`{key}` = %s" for key in datos.keys()]
        where_clauses = [f"`{key}` = %s" for key in condiciones.keys()]
        
        sql = f"UPDATE `{tabla}` SET {', '.join(set_clauses)} WHERE {' AND '.join(where_clauses)}"
        valores = list(datos.values()) + list(condiciones.values())
        
        self.cursor.execute(sql, valores)
        self.conexion.commit()
        
        return self.cursor.rowcount
    
    def eliminar(self, tabla, condiciones):
        self._validar_ident(tabla)
        
        if not condiciones:
            raise ValueError("Las condiciones no pueden estar vacías")
        
        # Validar identificadores
        for columna in condiciones.keys():
            self._validar_ident(columna)
        
        where_clauses = [f"`{key}` = %s" for key in condiciones.keys()]
        sql = f"DELETE FROM `{tabla}` WHERE {' AND '.join(where_clauses)}"
        valores = list(condiciones.values())
        
        self.cursor.execute(sql, valores)
        self.conexion.commit()
        
        return self.cursor.rowcount
    
    def tablas(self):
        self.cursor.execute("SHOW TABLES")
        filas = self.cursor.fetchall()
        
        # Convertir a lista de diccionarios
        datos = [{"tabla": fila[0]} for fila in filas]
        
        return json.dumps(datos, ensure_ascii=False, indent=2)
    
    def describir(self, tabla):
        self._validar_ident(tabla)
        
        self.cursor.execute(f"DESCRIBE `{tabla}`")
        columnas = self.cursor.column_names
        filas = self.cursor.fetchall()
        
        # Convertir a lista de diccionarios
        datos = [dict(zip(columnas, fila)) for fila in filas]
        
        return json.dumps(datos, ensure_ascii=False, indent=2, default=str)
    
    def ejecutar_sql(self, sql, parametros=None):
        self.cursor.execute(sql, parametros or ())
        
        # Si es una consulta SELECT, devolver resultados
        if sql.strip().upper().startswith('SELECT'):
            columnas = self.cursor.column_names
            filas = self.cursor.fetchall()
            datos = [dict(zip(columnas, fila)) for fila in filas]
            return json.dumps(datos, ensure_ascii=False, indent=2, default=str)
        else:
            # Si es INSERT, UPDATE, DELETE, hacer commit y devolver filas afectadas
            self.conexion.commit()
            return self.cursor.rowcount
    
    def cerrar(self):
        """
        Cierra la conexión a la base de datos
        """
        try:
            if self.cursor:
                self.cursor.close()
            if self.conexion:
                self.conexion.close()
        except Exception:
            pass


# Función de conveniencia para crear una instancia
def crear_conexion(host="localhost", usuario="", contrasena="", basedatos=""):
    return AMA(host, usuario, contrasena, basedatos)


if __name__ == "__main__":
    # Ejemplo de uso básico
    print("Componente de Acceso a Datos AMA - Final de Unidad 2")
    print("=" * 50)
    print("Basado en el patrón visto en clase")
    print()
    print("Ejemplo de uso:")
    print("conexion = AMA('localhost', 'usuario', 'password', 'database')")
    print("print(conexion.tablas())")
    print("print(conexion.seleccionar('mi_tabla'))")
    print("conexion.cerrar()")
```

**Integración realista en un backend**  
El componente se puede integrar en controladores o servicios de una API. En `demo_usage.py` muestro llamadas que serían análogas a endpoints (listar, crear, buscar, actualizar). Este es un **ejemplo directo del proyecto** para ilustrar el uso:

```python
# demo_usage.py 
from AMA import AMA

def main():
    """Demostración principal del componente AMA"""
    
    print("🎯 DEMOSTRACIÓN COMPONENTE AMA")
    print("=" * 40)
    print("Basado en el patrón visto en clase\n")
    
    # PASO 1: Crear conexión (cambia estos datos por los tuyos)
    print("📡 Conectando a la base de datos...")
    try:
        conexion = AMA(
            host="localhost",
            usuario="futbol_amadev",      # Cambia por tu usuario
            contrasena="futbol_amadev",  # Cambia por tu contraseña
            basedatos="futbol_amadev"     # Cambia por tu base de datos
        )
        print("✅ Conexión establecida correctamente\n")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("Verifica tus credenciales de base de datos")
        return
    
    try:
        # PASO 2: Ver tablas disponibles
        print("📋 Tablas disponibles en la base de datos:")
        tablas_json = conexion.tablas()
        print(tablas_json)
        print()
        
        # PASO 3: Crear tabla de ejemplo si no existe
        print("🏗️  Creando tabla de ejemplo...")
        sql_crear_tabla = """
        CREATE TABLE IF NOT EXISTS usuarios_ama (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            edad INT,
            activo BOOLEAN DEFAULT TRUE
        )
        """
        conexion.ejecutar_sql(sql_crear_tabla)
        print("✅ Tabla 'usuarios_ama' lista\n")
        
        # PASO 4: Insertar datos de ejemplo
        print("➕ Insertando usuarios de ejemplo...")
        
        # Usuario 1
        usuario1_id = conexion.insertar("usuarios_ama", {
            "nombre": "Ana García",
            "email": "ana@example.com",
            "edad": 28,
            "activo": True
        })
        print(f"   Usuario Ana insertado con ID: {usuario1_id}")
        
        # Usuario 2
        usuario2_id = conexion.insertar("usuarios_ama", {
            "nombre": "Carlos López",
            "email": "carlos@example.com",
            "edad": 35,
            "activo": True
        })
        print(f"   Usuario Carlos insertado con ID: {usuario2_id}")
        
        # Usuario 3
        usuario3_id = conexion.insertar("usuarios_ama", {
            "nombre": "Elena Botezatu",
            "email": "elena@example.com", 
            "edad": 29,
            "activo": False
        })
        print(f"   Usuario Elena insertado con ID: {usuario3_id}\n")
        
        # PASO 5: Seleccionar todos los usuarios
        print("👥 Todos los usuarios en la tabla:")
        usuarios = conexion.seleccionar("usuarios_ama")
        print(usuarios)
        print()
        
        # PASO 6: Buscar usuarios por criterio
        print("🔍 Buscando usuarios por email que contenga 'ana':")
        busqueda = conexion.buscar("usuarios_ama", "email", "ana")
        print(busqueda)
        print()
        
        # PASO 7: Actualizar un usuario
        print("✏️  Actualizando edad de Ana...")
        filas_actualizadas = conexion.actualizar(
            "usuarios_ama",
            {"edad": 29, "email": "ana.garcia@example.com"},
            {"id": usuario1_id}
        )
        print(f"   {filas_actualizadas} fila(s) actualizada(s)\n")
        
        # PASO 8: Ver usuarios después de la actualización
        print("👥 Usuarios después de la actualización:")
        usuarios_actualizados = conexion.seleccionar("usuarios_ama")
        print(usuarios_actualizados)
        print()
        
        # PASO 9: Consulta personalizada
        print("📊 Consulta personalizada - Usuarios activos:")
        usuarios_activos = conexion.ejecutar_sql(
            "SELECT nombre, email, edad FROM usuarios_ama WHERE activo = %s ORDER BY edad",
            (True,)
        )
        print(usuarios_activos)
        print()
        
        # PASO 10: Describir estructura de tabla
        print("🔍 Estructura de la tabla usuarios_ama:")
        estructura = conexion.describir("usuarios_ama")
        print(estructura)
        print()
        
        # PASO 11: Estadísticas con consulta personalizada
        print("📈 Estadísticas de usuarios:")
        stats = conexion.ejecutar_sql("""
            SELECT 
                COUNT(*) as total_usuarios,
                AVG(edad) as edad_promedio,
                MIN(edad) as edad_minima,
                MAX(edad) as edad_maxima,
                SUM(CASE WHEN activo = 1 THEN 1 ELSE 0 END) as usuarios_activos
            FROM usuarios_ama
        """)
        print(stats)
        print()
        
        # PASO 12: Opcional - Limpiar datos de demostración
        respuesta = input("¿Quieres eliminar los datos de demostración? (s/n): ")
        if respuesta.lower() == 's':
            print("🗑️  Limpiando datos de demostración...")
            eliminados = conexion.eliminar("usuarios_ama", {"nombre": "Ana García"})
            eliminados += conexion.eliminar("usuarios_ama", {"nombre": "Carlos López"})
            eliminados += conexion.eliminar("usuarios_ama", {"nombre": "Elena Botezatu"})
            print(f"   {eliminados} registro(s) eliminado(s)")
            
            # Eliminar tabla si está vacía
            confirmar = input("¿Eliminar también la tabla usuarios_ama? (s/n): ")
            if confirmar.lower() == 's':
                conexion.ejecutar_sql("DROP TABLE usuarios_ama")
                print("   Tabla eliminada")
        
        print("\n🎉 ¡Demostración completada exitosamente!")
        print("\nEl componente JVDB está listo para usar en tus proyectos:")
        print("- ✅ Conexión simple a MySQL")
        print("- ✅ Operaciones CRUD básicas")
        print("- ✅ Consultas personalizadas") 
        print("- ✅ Resultados en formato JSON")
        print("- ✅ Validación de identificadores")
        
    except Exception as e:
        print(f"❌ Error durante la demostración: {e}")
    
    finally:
        # PASO 13: Cerrar conexión
        print("\n🔌 Cerrando conexión...")
        conexion.cerrar()
        print("✅ Conexión cerrada")


def ejemplo_integracion():
    """Ejemplo de cómo integrar AMA en un proyecto"""
    
    print("\n" + "=" * 50)
    print("📝 EJEMPLO DE INTEGRACIÓN EN PROYECTO")
    print("=" * 50)
    
    print("""
# En tu proyecto, podrías usarlo así:

from AMA import AMA

# 1. Crear conexión
db = AMA("localhost", "tu_usuario", "tu_password", "tu_database")

# 2. Usar en funciones de tu aplicación
def obtener_usuarios():
    return db.seleccionar("usuarios")

def crear_usuario(nombre, email, edad):
    return db.insertar("usuarios", {
        "nombre": nombre,
        "email": email,
        "edad": edad
    })

def buscar_usuario_por_email(email):
    return db.buscar("usuarios", "email", email)

# 3. Para APIs web (Flask, etc.)
@app.route('/api/usuarios')
def api_usuarios():
    usuarios_json = db.seleccionar("usuarios")
    return usuarios_json  # Ya está en formato JSON

# 4. No olvides cerrar al terminar
db.cerrar()
    """)


if __name__ == "__main__":
    main()
    ejemplo_integracion()
```

**Errores comunes y cómo los evito/corrijo**  
1. **Identificadores inseguros o no válidos** → `_validar_ident()` rechaza nombres sospechosos (inyección por identificadores).  
2. **SQL injection por valores** → siempre uso **parámetros** (`%s`) en `buscar`, `actualizar`, `eliminar`, `ejecutar_sql` con `parametros`.  
3. **Olvidar `WHERE` en UPDATE/DELETE** → exijo `condiciones` no vacías en `actualizar()` y `eliminar()`.  
4. **Commit pendiente** → todas las operaciones de escritura hacen `self.conexion.commit()`.  
5. **Tablas inexistentes** → `describir("usuarios_jvdb")` en la demo puede fallar si no existe; es una **prueba** útil para verificar manejo de errores y coherencia con la tabla creada (`usuarios_ama`).  
6. **Conexión sin cerrar** → `cerrar()` asegura liberar recursos incluso en `finally` (como hago en `demo_usage.py`).

---

- He implementado un **componente reutilizable** (`AMA`) que encapsula conexión, **CRUD**, consultas parametrizadas, **introspección** y **formato JSON** de resultados.  
- La **demostración** (`demo_usage.py`) recorre un caso completo con creación de tabla, inserciones, listados, búsquedas, actualización y consultas agregadas.  
- Este trabajo se alinea con los objetivos de la unidad: **abstraer el acceso a datos** mediante una librería que pueda **integrarse** fácilmente en un backend, con prácticas de **validación** y **parametrización** coherentes con el temario.

**Relación con otros contenidos de la unidad**  
Conecta con conceptos de **conectores**, **validación de entrada**, **buenas prácticas de SQL parametrizado**, **mapeo de resultados a JSON** y **diseño de componentes reutilizables** en la capa de datos.
