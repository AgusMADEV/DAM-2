He desarrollado un sistema completo de gestión empresarial que permite administrar datos de forma eficiente a través de una interfaz web. El propósito principal de este sistema es proporcionar una herramienta práctica para gestionar información empresarial de manera organizada y accesible.

Como aficionado a la organización y la tecnología, siempre me ha fascinado cómo las empresas gestionan grandes volúmenes de información. Este proyecto me ha permitido aplicar mis conocimientos de programación y bases de datos para crear algo realmente útil. Mi hobby de coleccionar y catalogar cosas (ya sean libros, juegos o cualquier tipo de colección) me ha enseñado la importancia de tener un sistema bien estructurado donde pueda consultar, añadir y eliminar elementos fácilmente.

El sistema que he creado simula exactamente ese proceso: permite visualizar diferentes "colecciones" (tablas), añadir nuevos elementos y eliminar los que ya no son necesarios. Es como tener un inventario digital profesional donde toda la información está al alcance de un clic.

---

### Estructura de la Base de Datos

He creado una base de datos llamada `empresarial` con la siguiente estructura:

```sql
- clientes: Almacena información de los clientes
- productos: Catálogo de productos con precios y stock
- pedidos: Registros de pedidos realizados
- lineaspedidos: Detalles de cada línea de pedido
- pedidosconlineas: Tabla resumen de pedidos
- vista_pedidos: Vista que combina información de múltiples tablas
```

Cada tabla utiliza el campo `Identificador` como clave primaria con auto-incremento, siguiendo las convenciones vistas en clase.

### Conexión a la Base de Datos

La conexión se establece de forma consistente en todos los archivos:

```php
$conexion = mysqli_connect("localhost","usuarioempresarial","usuarioempresarial","empresarial");
```

He creado un usuario específico (`usuarioempresarial`) con permisos limitados únicamente a la base de datos `empresarial`, lo que mejora la seguridad del sistema al aplicar el principio de mínimo privilegio.

### Archivos Desarrollados

#### 1. **listar_tablas.php**
Este archivo es el punto de entrada al sistema. Realiza una consulta `SHOW TABLES` para obtener dinámicamente todas las tablas de la base de datos y genera un menú de navegación:

```php
$resultado = mysqli_query($conexion, "SHOW TABLES;");
while($fila = mysqli_fetch_assoc($resultado)){
    $nombre_tabla = $fila['Tables_in_empresarial'];
    echo "<a href='mostrar_tabla.php?tabla=".$nombre_tabla."'>".$nombre_tabla."</a>";
}
```

#### 2. **mostrar_tabla.php**
Muestra los registros de la tabla seleccionada mediante parámetros GET. Implementa:
- Visualización de datos en formato tabla HTML
- Encabezados dinámicos basados en los campos de la tabla
- Botón de eliminación por cada registro
- Confirmación JavaScript antes de eliminar

```php
$resultado = mysqli_query($conexion, "SELECT * FROM ".$tabla.";");
while($fila = mysqli_fetch_assoc($resultado)){
    // Generación dinámica de filas
}
```

La funcionalidad de eliminación está integrada en el mismo archivo:

```php
if(isset($_GET['operacion']) && $_GET['operacion'] == "eliminar"){
    mysqli_query($conexion, "DELETE FROM ".$tabla." WHERE Identificador = ".$id_eliminar.";");
    header("Location: mostrar_tabla.php?tabla=".$tabla);
}
```

#### 3. **añadir_registro.php**
Formulario dinámico que se adapta a la estructura de cada tabla:

```php
$resultado = mysqli_query($conexion, "SELECT * FROM ".$tabla." LIMIT 1;");
if($fila = mysqli_fetch_assoc($resultado)){
    foreach($fila as $clave=>$valor){
        if($clave != 'Identificador'){
            echo "<input type='text' name='".$clave."' placeholder='".$clave."'>";
        }
    }
}
```

El procesamiento del formulario construye la consulta INSERT dinámicamente:

```php
$campos = array();
$valores = array();
foreach($_POST as $clave=>$valor){
    if($clave != 'tabla' && $valor != ''){
        $campos[] = $clave;
        $valores[] = "'".$valor."'";
    }
}
$sql = "INSERT INTO ".$tabla." (".implode(", ", $campos).") VALUES (".implode(", ", $valores).");";
```

### Seguridad y Estabilidad

He implementado varias medidas de seguridad:
- Usuario de base de datos con permisos específicos
- Redirecciones después de operaciones POST para evitar reenvío de formularios
- Confirmación JavaScript antes de eliminar registros
- Validación de existencia de parámetros GET con `isset()`

---

### Conceptos SQL Aplicados

**1. SHOW TABLES**
```php
mysqli_query($conexion, "SHOW TABLES;");
```
Este comando nos permite obtener dinámicamente todas las tablas, haciendo el sistema escalable. Si añadimos más tablas en el futuro, el menú se actualiza automáticamente.

**2. SELECT con comodín**
```php
mysqli_query($conexion, "SELECT * FROM ".$tabla.";");
```
Recupera todos los campos y registros de la tabla seleccionada.

**3. INSERT dinámico**
```php
INSERT INTO clientes (nombre, apellidos, email) VALUES ('Juan', 'García', 'juan@email.com');
```
Construido dinámicamente según los campos del formulario.

**4. DELETE con condición**
```php
DELETE FROM clientes WHERE Identificador = 5;
```
Elimina un registro específico usando su identificador único.

### Integración de Hobbies Personales

Mi pasión por la organización y los sistemas de catalogación se refleja en cada aspecto de este proyecto:

- **Navegación intuitiva:** Como cuando organizo mi colección de videojuegos, he diseñado un sistema donde puedo acceder rápidamente a cualquier "categoría" (tabla).

- **Visualización clara:** El diseño de las tablas con colores alternados me recuerda a las hojas de cálculo donde llevo el control de mis gastos personales, facilitando la lectura de grandes cantidades de datos.

- **Gestión completa CRUD:** Al igual que cuando actualizo mi biblioteca personal (añadir libros nuevos, quitar los que he prestado, consultar cuáles tengo), este sistema permite hacer todo tipo de operaciones sobre los datos.

### Ejemplo de Uso Real

Imaginemos que gestiono una pequeña tienda online:

1. **Consulto el inventario:** Accedo a `listar_tablas.php` y selecciono "productos"
2. **Veo que un producto se agotó:** En `mostrar_tabla.php` veo que el "Ratón inalámbrico" tiene stock 0
3. **Lo elimino del catálogo:** Hago clic en el botón "x" junto al producto
4. **Recibo un nuevo producto:** Accedo a `añadir_registro.php?tabla=productos` y añado el nuevo artículo

Este flujo de trabajo es exactamente igual al que usaría en mi colección personal de cualquier hobby.

---

Esta actividad ha consolidado los conceptos fundamentales de la unidad: consultas SQL (SELECT, INSERT, DELETE, SHOW TABLES), conexión PHP-MySQL con mysqli, programación dinámica mediante parámetros GET, diseño con CSS variables y flexbox, y seguridad básica con validaciones y permisos de usuario.

Como apasionado de la organización desde pequeño, siempre he llevado listas y catalogado colecciones personales. Esta necesidad de orden me llevó naturalmente a la programación. El proyecto me ha permitido aplicar esa experiencia personal al ámbito profesional, creando un sistema donde la simplicidad y la reutilización del código son clave.

Este prototipo será fundamental para el proyecto final de gestión empresarial, especialmente las técnicas de generación dinámica de interfaces. He aprendido que PHP y MySQL, sin frameworks complejos, son herramientas potentes para crear soluciones funcionales donde la experiencia de usuario importa tanto como la funcionalidad técnica.

Estoy preparado para abordar proyectos más complejos incorporando funcionalidades avanzadas como búsqueda, edición de registros, autenticación de usuarios y exportación de datos.
