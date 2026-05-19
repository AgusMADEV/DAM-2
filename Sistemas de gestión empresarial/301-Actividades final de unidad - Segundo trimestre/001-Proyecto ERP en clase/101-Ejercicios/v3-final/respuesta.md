Este proyecto consiste en el desarrollo de **TotalKit ERP**, un sistema de planificación de recursos empresariales (ERP) personalizado para la gestión integral de una tienda online de camisetas de fútbol. 

Como estudiante de DAM, he implementado este sistema para demostrar la aplicación práctica de los conceptos vistos en las unidades 001 (Identificación de sistemas ERP-CRM), 002 (Instalación y configuración) y 003 (Organización y consulta de la información). Este tipo de sistema se utiliza en contextos empresariales para centralizar la gestión de productos, inventarios, pedidos y relaciones con clientes, automatizando procesos que tradicionalmente requerirían múltiples sistemas independientes.

El objetivo principal es proporcionar una plataforma web que permita la administración completa del catálogo de productos (camisetas de equipos y selecciones nacionales), con funcionalidades avanzadas de búsqueda, filtrado y visualización de datos, manteniendo la integridad referencial a través de una base de datos relacional bien estructurada.

---

### Arquitectura del Sistema

He desarrollado TotalKit ERP siguiendo una **arquitectura de tres capas**:

- **Capa de Presentación**: Interface web HTML/CSS con JavaScript vanilla para interactividad del lado del cliente
- **Capa de Lógica de Negocio**: Scripts PHP que procesan las peticiones, validan datos y ejecutan operaciones CRUD
- **Capa de Datos**: Base de datos MySQL con esquema normalizado y relaciones bien definidas

Esta arquitectura garantiza la **separación de responsabilidades** (Separation of Concerns), un principio fundamental en el desarrollo de sistemas empresariales que facilita el mantenimiento y la escalabilidad.

### Modelo de Datos Relacional

La base de datos `tienda_camisetas` está diseñada siguiendo los principios de **normalización de bases de datos** (hasta la tercera forma normal - 3NF), lo cual vimos en la unidad 003 cuando estudiamos la organización y consulta de la información.

**Estructura de tablas principales**:

```sql
-- Tablas maestras (entidades fuertes)
- paises
- estados_pedido
- temporadas
- tallas
- tipos_camiseta
- ligas
- marcas
- clientes
- metodos_pago
- metodos_envio

-- Tablas de negocio (con claves foráneas)
- equipos (referencia a ligas y países)
- productos (referencia a equipos, marcas, temporadas, tipos_camiseta, tallas)
- pedidos (referencia a clientes, estados, métodos de pago/envío)
- articulos_pedido (tabla intermedia productos-pedidos)
- resenas_producto (referencia a productos y clientes)
- imagenes_producto (referencia a productos)
- direcciones (referencia a clientes y países)
```

La tabla central del sistema es **productos**, que actúa como hub de información y tiene las siguientes claves foráneas:

```sql
CREATE TABLE productos (
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    codigo_producto VARCHAR(50) NOT NULL UNIQUE,
    nombre_producto VARCHAR(200) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0,
    jugador VARCHAR(100),
    numero_dorsal INT,
    version_jugador TINYINT(1) DEFAULT 0,
    destacado TINYINT(1) DEFAULT 0,
    activo TINYINT(1) DEFAULT 1,
    
    -- Claves foráneas
    id_equipo INT NOT NULL,
    id_marca INT NOT NULL,
    id_temporada INT NOT NULL,
    id_tipo_camiseta INT NOT NULL,
    id_talla INT NOT NULL,
    
    FOREIGN KEY (id_equipo) REFERENCES equipos(id_equipo),
    FOREIGN KEY (id_marca) REFERENCES marcas(id_marca),
    FOREIGN KEY (id_temporada) REFERENCES temporadas(id_temporada),
    FOREIGN KEY (id_tipo_camiseta) REFERENCES tipos_camiseta(id_tipo_camiseta),
    FOREIGN KEY (id_talla) REFERENCES tallas(id_talla)
);
```

Este diseño garantiza la **integridad referencial**, evitando inconsistencias como productos sin equipo asignado o referencias a temporadas inexistentes.

### Sistema de Autenticación y Gestión de Sesiones

Implementé un sistema de autenticación basado en **sesiones de PHP** (`$_SESSION`), siguiendo las mejores prácticas de seguridad vistas en la unidad 002 sobre instalación y configuración:

**Proceso de login paso a paso**:

1. El usuario envía credenciales mediante POST
2. El servidor valida contra constantes definidas en `config.php`
3. Si las credenciales son correctas, se crea una sesión con `$_SESSION['usuario']`
4. Todas las páginas verifican la existencia de `$_SESSION['usuario']` antes de permitir acceso
5. El logout destruye la sesión con `session_destroy()`

```php
// Login - config.php
define('LOGIN_USUARIO', 'admin');
define('LOGIN_PASSWORD', 'admin123');

// Validación - index.php
if ($user === LOGIN_USUARIO && $pass === LOGIN_PASSWORD) {
    $_SESSION['usuario'] = $user;
    header("Location: ?");
    exit;
} else {
    $login_error = "Usuario o contraseña incorrectos";
}

// Verificación de sesión
$logged_in = isset($_SESSION['usuario']);
```

**Mejoras de seguridad implementadas**:
- Uso de `htmlspecialchars()` para prevenir XSS (Cross-Site Scripting)
- `mysqli_real_escape_string()` para prevenir inyección SQL
- Redirecciones con `header()` después de operaciones críticas
- Validación de entrada en el servidor antes de procesamiento

### Sistema de Búsqueda Avanzada con Filtros Dinámicos

Una de las funcionalidades más complejas que implementé es el **buscador profesional de productos** con múltiples filtros y paginación, utilizando tecnología AJAX para evitar recargas de página completa.

**Componentes del sistema de búsqueda**:

**Backend (buscar_productos.php)**:
- API REST que devuelve respuestas JSON
- Construcción dinámica de consultas SQL con filtros opcionales
- Paginación con límites y offsets
- Ordenamiento configurable por diferentes campos

**Frontend (buscador.js)**:
- Clase `BuscadorProductos` con encapsulación de lógica
- Manejo de eventos con debouncing para optimizar peticiones
- Actualización dinámica del DOM sin recargar la página
- Cambio de vista entre grid y lista

**Ejemplo de construcción dinámica de consulta**:

```php
function construir_consulta_busqueda($conexion, $filtros) {
    $sql = "SELECT 
        p.id_producto,
        p.nombre_producto,
        p.precio,
        p.stock,
        e.nombre_equipo,
        m.nombre_marca,
        t.nombre_temporada
    FROM productos p
    INNER JOIN equipos e ON p.id_equipo = e.id_equipo
    INNER JOIN marcas m ON p.id_marca = m.id_marca
    WHERE p.activo = 1";
    
    // Agregar filtros dinámicamente
    if (!empty($filtros['texto'])) {
        $texto = mysqli_real_escape_string($conexion, $filtros['texto']);
        $sql .= " AND (p.nombre_producto LIKE '%$texto%' 
                  OR p.descripcion LIKE '%$texto%')";
    }
    
    if (!empty($filtros['id_equipo'])) {
        $sql .= " AND p.id_equipo = " . intval($filtros['id_equipo']);
    }
    
    // ...más filtros
    
    return $sql;
}
```

Este enfoque implementa el patrón de **consultas parametrizadas dinámicas**, permitiendo flexibilidad sin comprometer la seguridad.

### Funcionalidades CRUD Completas

Implementé operaciones **CRUD completas** (Create, Read, Update, Delete) para todas las entidades principales:

**CREATE (Crear)**:
```php
// Inserción con verificación de claves foráneas
$sql = "INSERT INTO productos (
    codigo_producto, nombre_producto, descripcion, precio, 
    stock, id_equipo, id_marca, id_temporada, 
    id_tipo_camiseta, id_talla
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

$stmt = mysqli_prepare($conexion, $sql);
mysqli_stmt_bind_param($stmt, "sssdiiiiii", 
    $codigo, $nombre, $desc, $precio, $stock, 
    $id_equipo, $id_marca, $id_temporada, $id_tipo, $id_talla
);
```

**READ (Leer)**:
- Consultas simples para listados
- Consultas con JOIN para obtener datos relacionados
- Uso de INFORMATION_SCHEMA para metadatos

**UPDATE (Actualizar)**:
```php
// Actualización con validación previa
$sql = "UPDATE productos SET 
    nombre_producto = ?, 
    precio = ?, 
    stock = ? 
WHERE id_producto = ?";
```

**DELETE (Eliminar)**:
- Borrado lógico con campo `activo` cuando hay dependencias
- Borrado físico cuando no hay referencias

### Gestión de Claves Foráneas Automática

Desarrollé una función auxiliar que **detecta automáticamente las claves foráneas** de cualquier tabla consultando el esquema de información de MySQL:

```php
function obtener_claves_foraneas($conexion, $tabla, $bd = DB_NAME) {
    $fk = [];
    $sql = "
        SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = '" . mysqli_real_escape_string($conexion, $bd) . "'
          AND TABLE_NAME = '" . mysqli_real_escape_string($conexion, $tabla) . "'
          AND REFERENCED_TABLE_NAME IS NOT NULL
    ";
    $resultado = mysqli_query($conexion, $sql);
    if ($resultado) {
        while ($fila = mysqli_fetch_assoc($resultado)) {
            $fk[$fila['COLUMN_NAME']] = [
                'tabla' => $fila['REFERENCED_TABLE_NAME'],
                'columna' => $fila['REFERENCED_COLUMN_NAME']
            ];
        }
    }
    return $fk;
}
```

Esta función permite que el sistema sea **genérico y reutilizable**, pudiendo trabajar con cualquier tabla sin necesidad de hardcodear las relaciones. Es un ejemplo de **metaprogramación** aplicada a bases de datos.

### Organización del Código y Configuración

Seguí el principio de **separación de configuración y lógica** mediante el archivo `config.php`:

```php
// Configuración centralizada
define('DB_HOST', 'localhost');
define('DB_NAME', 'tienda_camisetas');
define('DB_USER', 'totalkit');
define('DB_PASS', 'totalkit');

define('APP_NAME', 'TotalKit ERP');
define('APP_VERSION', '1.0.0');
define('TIMEZONE', 'Europe/Madrid');
```

Este enfoque facilita:
- Cambio de entorno (desarrollo → producción) modificando un solo archivo
- Reutilización de credenciales
- Mantenimiento centralizado

### Interface de Usuario con Componentes Reutilizables

Implementé un sistema de **iconos SVG modulares** mediante una función generadora:

```php
function svg_icon($type, $size = 20, $color = 'currentColor') {
    $icons = [
        'check' => '<svg>...</svg>',
        'search' => '<svg>...</svg>',
        'edit' => '<svg>...</svg>',
        // ...más iconos
    ];
    return $icons[$type] ?? '';
}

// Uso
echo svg_icon('search', 18, '#2563eb');
```

Esto permite:
- Consistencia visual en toda la aplicación
- Fácil modificación de diseño
- No depender de librerías externas de iconos
- Mejor rendimiento (SVG inline vs. solicitudes HTTP)

---

### Ejemplo Real: Flujo Completo de Búsqueda de Productos

Voy a explicar cómo funciona una búsqueda de productos paso a paso, mostrando el código real implementado:

**PASO 1: Usuario escribe en el buscador**

El usuario escribe "Real Madrid" en el campo de búsqueda de la interface web.

**PASO 2: JavaScript captura el evento con debouncing**

```javascript
// buscador.js
configurarEventos() {
    const inputBusqueda = document.getElementById('busqueda-texto');
    
    inputBusqueda.addEventListener('input', (e) => {
        // Cancelar búsqueda anterior si existe
        clearTimeout(this.timeoutBusqueda);
        
        // Esperar 300ms antes de buscar (debouncing)
        this.timeoutBusqueda = setTimeout(() => {
            this.filtros.q = e.target.value;
            this.pagina = 1;
            this.realizarBusqueda();
        }, 300);
    });
}
```

El **debouncing** evita hacer una petición HTTP por cada tecla pulsada, esperando 300ms de inactividad. Esto mejora el rendimiento significativamente.

**PASO 3: Se construye la URL con parámetros**

```javascript
async realizarBusqueda() {
    const params = new URLSearchParams({
        accion: 'buscar',
        q: this.filtros.q,
        equipo: this.filtros.equipo,
        pagina: this.pagina,
        por_pagina: this.por_pagina,
        orden: this.orden,
        dir: this.dir
    });
    
    const url = `buscar_productos.php?${params.toString()}`;
    
    const response = await fetch(url);
    const data = await response.json();
    
    if (data.success) {
        this.mostrarResultados(data.productos);
        this.actualizarPaginacion(data.paginacion);
    }
}
```

**PASO 4: El servidor recibe y procesa la petición**

```php
// buscar_productos.php
session_start();
require_once 'config.php';

// Verificar autenticación
if (!isset($_SESSION['usuario'])) {
    http_response_code(401);
    echo json_encode(['error' => 'No autorizado']);
    exit;
}

$conexion = obtener_conexion();

// Recibir parámetros
$texto = $_GET['q'] ?? '';
$id_equipo = $_GET['equipo'] ?? '';
$pagina = max(1, intval($_GET['pagina'] ?? 1));
$por_pagina = min(50, max(5, intval($_GET['por_pagina'] ?? 12)));

// Construir consulta SQL
$sql = "SELECT 
    p.id_producto,
    p.nombre_producto,
    p.precio,
    p.stock,
    e.nombre_equipo,
    m.nombre_marca
FROM productos p
INNER JOIN equipos e ON p.id_equipo = e.id_equipo
INNER JOIN marcas m ON p.id_marca = m.id_marca
WHERE p.activo = 1";

$params = [];

if (!empty($texto)) {
    $sql .= " AND (p.nombre_producto LIKE ? OR e.nombre_equipo LIKE ?)";
    $textoLike = '%' . $texto . '%';
    $params[] = $textoLike;
    $params[] = $textoLike;
}

if (!empty($id_equipo)) {
    $sql .= " AND p.id_equipo = ?";
    $params[] = $id_equipo;
}

// Contar total de resultados
$sqlCount = "SELECT COUNT(*) as total FROM (" . $sql . ") as subquery";
$resultado = mysqli_query($conexion, $sqlCount);
$total = mysqli_fetch_assoc($resultado)['total'];

// Aplicar paginación
$offset = ($pagina - 1) * $por_pagina;
$sql .= " ORDER BY p.fecha_creacion DESC LIMIT $por_pagina OFFSET $offset";

$resultado = mysqli_query($conexion, $sql);

$productos = [];
while ($fila = mysqli_fetch_assoc($resultado)) {
    $productos[] = $fila;
}

// Devolver JSON
header('Content-Type: application/json');
echo json_encode([
    'success' => true,
    'productos' => $productos,
    'paginacion' => [
        'total' => $total,
        'pagina_actual' => $pagina,
        'total_paginas' => ceil($total / $por_pagina),
        'por_pagina' => $por_pagina
    ]
]);
```

**PASO 5: JavaScript actualiza el DOM con los resultados**

```javascript
mostrarResultados(productos) {
    const contenedor = document.getElementById('resultados-productos');
    
    if (productos.length === 0) {
        contenedor.innerHTML = '<p class="no-resultados">No se encontraron productos</p>';
        return;
    }
    
    let html = '<div class="productos-grid">';
    
    productos.forEach(producto => {
        html += `
            <div class="producto-card" data-id="${producto.id_producto}">
                <h3>${this.escaparHTML(producto.nombre_producto)}</h3>
                <p class="equipo">${this.escaparHTML(producto.nombre_equipo)}</p>
                <p class="marca">${this.escaparHTML(producto.nombre_marca)}</p>
                <p class="precio">${parseFloat(producto.precio).toFixed(2)}€</p>
                <p class="stock">Stock: ${producto.stock}</p>
                <div class="acciones">
                    <button onclick="editarProducto(${producto.id_producto})">
                        Editar
                    </button>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    contenedor.innerHTML = html;
}

// Prevención de XSS
escaparHTML(texto) {
    const div = document.createElement('div');
    div.textContent = texto;
    return div.innerHTML;
}
```

**Resultado final**: El usuario ve una lista actualizada de productos que contienen "Real Madrid" en menos de 1 segundo, sin recargar la página.

### 3.2. Ejemplo de Código: Inserción de Producto con Validación

```php
// Función completa para insertar producto
function insertar_producto($conexion, $datos) {
    // VALIDACIÓN DE DATOS
    $errores = [];
    
    if (empty($datos['codigo_producto'])) {
        $errores[] = "El código de producto es obligatorio";
    }
    
    if (empty($datos['nombre_producto'])) {
        $errores[] = "El nombre del producto es obligatorio";
    }
    
    if (!is_numeric($datos['precio']) || $datos['precio'] <= 0) {
        $errores[] = "El precio debe ser un número positivo";
    }
    
    if (!is_numeric($datos['stock']) || $datos['stock'] < 0) {
        $errores[] = "El stock debe ser un número no negativo";
    }
    
    // Verificar que las claves foráneas existen
    $tablas_validar = [
        'equipos' => $datos['id_equipo'],
        'marcas' => $datos['id_marca'],
        'temporadas' => $datos['id_temporada'],
        'tipos_camiseta' => $datos['id_tipo_camiseta'],
        'tallas' => $datos['id_talla']
    ];
    
    foreach ($tablas_validar as $tabla => $id) {
        $id_campo = "id_" . substr($tabla, 0, -1); // equipos -> id_equipo
        $sql_check = "SELECT COUNT(*) as existe FROM $tabla WHERE $id_campo = " . intval($id);
        $resultado = mysqli_query($conexion, $sql_check);
        $existe = mysqli_fetch_assoc($resultado)['existe'];
        
        if (!$existe) {
            $errores[] = "El $tabla con ID $id no existe";
        }
    }
    
    if (!empty($errores)) {
        return ['success' => false, 'errores' => $errores];
    }
    
    // INSERCIÓN CON PREPARED STATEMENT
    $sql = "INSERT INTO productos (
        codigo_producto, nombre_producto, descripcion, 
        precio, stock, jugador, numero_dorsal, version_jugador,
        id_equipo, id_marca, id_temporada, id_tipo_camiseta, id_talla,
        destacado, activo
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
    
    $stmt = mysqli_prepare($conexion, $sql);
    
    if (!$stmt) {
        return ['success' => false, 'error' => mysqli_error($conexion)];
    }
    
    mysqli_stmt_bind_param(
        $stmt,
        "sssdiiiiiiiiii",
        $datos['codigo_producto'],
        $datos['nombre_producto'],
        $datos['descripcion'],
        $datos['precio'],
        $datos['stock'],
        $datos['jugador'],
        $datos['numero_dorsal'],
        $datos['version_jugador'],
        $datos['id_equipo'],
        $datos['id_marca'],
        $datos['id_temporada'],
        $datos['id_tipo_camiseta'],
        $datos['id_talla'],
        $datos['destacado'],
        $datos['activo']
    );
    
    $exito = mysqli_stmt_execute($stmt);
    
    if ($exito) {
        $id_insertado = mysqli_insert_id($conexion);
        return [
            'success' => true, 
            'id_producto' => $id_insertado,
            'mensaje' => 'Producto insertado correctamente'
        ];
    } else {
        return [
            'success' => false, 
            'error' => mysqli_stmt_error($stmt)
        ];
    }
}

// USO
$nuevo_producto = [
    'codigo_producto' => 'RM-2024-TIT-M',
    'nombre_producto' => 'Camiseta Real Madrid 2024/25 - Titular',
    'descripcion' => 'Camiseta oficial de la temporada 2024/25',
    'precio' => 89.99,
    'stock' => 50,
    'jugador' => 'Vinicius Jr',
    'numero_dorsal' => 7,
    'version_jugador' => 1,
    'id_equipo' => 1,
    'id_marca' => 2, // Adidas
    'id_temporada' => 5,
    'id_tipo_camiseta' => 1, // Titular
    'id_talla' => 3, // M
    'destacado' => 1,
    'activo' => 1
];

$resultado = insertar_producto($conexion, $nuevo_producto);

if ($resultado['success']) {
    echo "✅ Producto creado con ID: " . $resultado['id_producto'];
} else {
    echo "❌ Errores: " . implode(", ", $resultado['errores']);
}
```

Este código demuestra:
- Validación exhaustiva de datos de entrada
- Verificación de integridad referencial antes de insertar
- Uso de prepared statements para prevenir inyección SQL
- Manejo de errores robusto
- Respuestas estructuradas con arrays asociativos

### Errores Comunes y Cómo Evitarlos

Durante el desarrollo de TotalKit ERP me encontré con varios errores típicos que documenté para evitarlos en el futuro:

**ERROR 1: Inyección SQL**

❌ **INCORRECTO** (vulnerable a SQL injection):
```php
$equipo_id = $_GET['equipo'];
$sql = "SELECT * FROM productos WHERE id_equipo = $equipo_id";
```

✅ **CORRECTO** (usando prepared statements):
```php
$equipo_id = $_GET['equipo'];
$sql = "SELECT * FROM productos WHERE id_equipo = ?";
$stmt = mysqli_prepare($conexion, $sql);
mysqli_stmt_bind_param($stmt, "i", $equipo_id);
mysqli_stmt_execute($stmt);
```

**ERROR 2: Cross-Site Scripting (XSS)**

❌ **INCORRECTO** (permite inyección de JavaScript):
```php
echo "<h1>" . $_POST['nombre'] . "</h1>";
```

✅ **CORRECTO** (escapa caracteres especiales):
```php
echo "<h1>" . htmlspecialchars($_POST['nombre'], ENT_QUOTES, 'UTF-8') . "</h1>";
```

**ERROR 3: No verificar sesión en APIs**

❌ **INCORRECTO** (permite acceso sin autenticación):
```php
<?php
require_once 'config.php';
$conexion = obtener_conexion();
// ... código que devuelve datos
```

✅ **CORRECTO** (verifica sesión antes de continuar):
```php
<?php
session_start();
if (!isset($_SESSION['usuario'])) {
    http_response_code(401);
    echo json_encode(['error' => 'No autorizado']);
    exit;
}
require_once 'config.php';
// ... resto del código
```

**ERROR 4: No validar claves foráneas antes de insertar**

❌ **INCORRECTO** (puede provocar errores de MySQL):
```php
$sql = "INSERT INTO productos (id_equipo, ...) VALUES ($id_equipo, ...)";
mysqli_query($conexion, $sql);
// Error: Cannot add or update a child row: a foreign key constraint fails
```

✅ **CORRECTO** (valida existencia primero):
```php
// Verificar que el equipo existe
$check_sql = "SELECT COUNT(*) as existe FROM equipos WHERE id_equipo = ?";
$stmt = mysqli_prepare($conexion, $check_sql);
mysqli_stmt_bind_param($stmt, "i", $id_equipo);
mysqli_stmt_execute($stmt);
$resultado = mysqli_stmt_get_result($stmt);
$existe = mysqli_fetch_assoc($resultado)['existe'];

if ($existe == 0) {
    die("Error: El equipo con ID $id_equipo no existe");
}

// Ahora sí insertar
$sql = "INSERT INTO productos (id_equipo, ...) VALUES (?, ...)";
```

**ERROR 5: No usar transacciones para operaciones múltiples**

❌ **INCORRECTO** (puede dejar datos inconsistentes):
```php
// Crear pedido
mysqli_query($conexion, "INSERT INTO pedidos ...");
$id_pedido = mysqli_insert_id($conexion);

// Insertar artículos (si falla, queda pedido vacío)
mysqli_query($conexion, "INSERT INTO articulos_pedido ...");
```

✅ **CORRECTO** (usa transacciones):
```php
mysqli_begin_transaction($conexion);

try {
    // Crear pedido
    mysqli_query($conexion, "INSERT INTO pedidos ...");
    $id_pedido = mysqli_insert_id($conexion);
    
    // Insertar artículos
    mysqli_query($conexion, "INSERT INTO articulos_pedido ...");
    
    // Si todo va bien, confirmar
    mysqli_commit($conexion);
} catch (Exception $e) {
    // Si algo falla, revertir todo
    mysqli_rollback($conexion);
    die("Error en la transacción: " . $e->getMessage());
}
```

**ERROR 6: No cerrar conexiones a la base de datos**

❌ **INCORRECTO** (puede agotar el pool de conexiones):
```php
$conexion = obtener_conexion();
$resultado = mysqli_query($conexion, $sql);
// ... usar resultado
// No cierra la conexión
```

✅ **CORRECTO** (libera recursos):
```php
$conexion = obtener_conexion();
$resultado = mysqli_query($conexion, $sql);
// ... usar resultado
mysqli_close($conexion);
```

### Relación con Contenidos de las Unidades

Este proyecto integra los siguientes conceptos aprendidos en clase:

**De la Unidad 001 - Identificación de sistemas ERP-CRM**:
- Concepto de ERP como sistema integrado de gestión empresarial
- Módulos de un ERP (en mi caso: gestión de productos, inventarios, pedidos)
- Diferencia entre ERP propietario y desarrollo personalizado

**De la Unidad 002 - Instalación y configuración**:
- Configuración de base de datos MySQL compatible con el sistema
- Parámetros de configuración centralizados (`config.php`)
- Gestión de usuarios y permisos (sistema de autenticación)
- Entorno de desarrollo local con XAMPP

**De la Unidad 003 - Organización y consulta de la información**:
- Definición de campos en tablas de base de datos
- Consultas de acceso a datos con JOIN para relacionar información
- Interfaces de entrada de datos (formularios)
- Informes y listados generados dinámicamente
- Uso de INFORMATION_SCHEMA para metadatos

---

En este proyecto he aplicado de forma práctica los conocimientos adquiridos en las tres primeras unidades de Sistemas de Gestión Empresarial, desarrollando un **ERP funcional completo** para un caso de uso real: la gestión de una tienda de camisetas de fútbol.

**Puntos clave del proyecto**:

1. **Arquitectura de tres capas** con separación clara de responsabilidades
2. **Base de datos normalizada** con integridad referencial mediante claves foráneas
3. **Sistema CRUD completo** con validación de datos y manejo de errores
4. **Búsqueda avanzada con AJAX** para una experiencia de usuario fluida
5. **Seguridad implementada** con sesiones, prepared statements y sanitización de datos
6. **Código modular y reutilizable** con funciones auxiliares genéricas

Este sistema demuestra cómo los conceptos teóricos vistos en clase (ERP, módulos, gestión de datos, interfaces, consultas) se traducen en código real que resuelve problemas empresariales. He aprendido especialmente la importancia de:

- La **integridad de datos** a través del diseño correcto de la base de datos
- La **seguridad** como prioridad desde el inicio del desarrollo
- La **experiencia de usuario** mediante interfaces dinámicas con AJAX
- El **mantenimiento futuro** gracias al código modular y documentado

Como próximos pasos de mejora, podría implementar:
- Módulo CRM para gestión de clientes (conectando con la unidad 001)
- Dashboards con gráficos estadísticos (visto en unidad 003)
- Sistema de roles y permisos más granular (profundizando en unidad 002)
- API REST completa para integración con otros sistemas (preparando para unidad 005 - Desarrollo de componentes)

Este proyecto me ha permitido consolidar los conocimientos de forma práctica y entender la complejidad real de desarrollar sistemas ERP empresariales, valorando aún más las soluciones comerciales como SAP u Odoo, pero también demostrando que con los conocimientos adquiridos puedo desarrollar soluciones personalizadas adaptadas a necesidades específicas.