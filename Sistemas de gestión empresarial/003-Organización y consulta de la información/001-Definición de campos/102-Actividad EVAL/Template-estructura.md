El **enrutamiento (routing)** en aplicaciones web es el mecanismo que permite gestionar las diferentes URLs que un usuario puede solicitar y asociarlas con las acciones correspondientes que debe ejecutar el servidor. En lugar de crear un archivo PHP diferente para cada página (como `/contacto.php`, `/acerca.php`), el enrutamiento centraliza todas las peticiones en un único punto de entrada, determinando dinámicamente qué código ejecutar según la ruta solicitada.

Este concepto es fundamental en el desarrollo de aplicaciones web modernas, ya que permite crear **APIs RESTful**, **aplicaciones de página única (SPA)** y sistemas escalables. Se utiliza en frameworks como Laravel, Symfony, Express.js y prácticamente cualquier aplicación que necesite gestionar múltiples recursos de forma organizada. El enrutamiento facilita la separación de responsabilidades, mejora la mantenibilidad del código y permite implementar URLs amigables para el SEO.

---

### Componentes del Sistema de Enrutamiento

Un sistema de enrutamiento básico en PHP consta de los siguientes elementos:

#### Estructura de Datos de Rutas
Se utiliza un **array asociativo multidimensional** que organiza las rutas por método HTTP y path:

```php
$routes = [
    'GET' => [
        '/' => function() { /* código a ejecutar */ },
        '/contacto' => function() { /* código a ejecutar */ }
    ],
    'POST' => [
        '/guardar' => function() { /* código a ejecutar */ }
    ]
];
```

**Terminología técnica:**
- **Método HTTP**: Indica el tipo de operación (GET, POST, PUT, DELETE, PATCH)
- **Path/Ruta**: La URL específica que el cliente solicita
- **Handler/Controlador**: La función anónima (closure) que se ejecuta cuando se accede a la ruta
- **Callback**: Término alternativo para referirse al handler

#### Proceso de Enrutamiento (Paso a Paso)

**Paso 1: Captura de la Solicitud HTTP**
```php
$method = $_SERVER['REQUEST_METHOD'];  // Ej: 'GET', 'POST'
$path = $_SERVER['REQUEST_URI'];      // Ej: '/dam-2/.../102-Actividad%20EVAL/contacto'
```

**Paso 2: Análisis y Limpieza de la URL**
```php
$parsed = parse_url($path);           // Separa componentes de la URL
$cleanPath = $parsed['path'];         // Obtiene solo el path sin query strings
```

**Paso 3: Normalización del Path**
```php
// Eliminar la ruta base del proyecto
$base = '/dam-2/Sistemas%20de%20gesti%C3%B3n%20empresarial/.../102-Actividad%20EVAL';
$finalPath = str_replace($base, '', $cleanPath);

// Manejar ruta raíz
if (empty($finalPath)) {
    $finalPath = '/';
}
```

**Paso 4: Resolución y Ejecución de la Ruta**
```php
if (isset($routes[$method][$finalPath])) {
    // Ruta encontrada: ejecutar el handler
    $routes[$method][$finalPath]();
} else {
    // Ruta no encontrada: mostrar error 404
    echo "<h2>404 - Ruta no encontrada</h2>";
}
```

#### Tipos de Rutas

**Rutas Estáticas**: Coincidencia exacta del path
```php
'/hola' => function() {
    echo "¡Bienvenido!";
}
```

**Rutas con Respuestas HTML**: Para vistas web
```php
'/' => function() {
    echo "<h1>Página Principal</h1>";
    echo "<p>Contenido...</p>";
}
```

**Rutas con Respuestas JSON**: Para APIs
```php
'/menu' => function() {
    $datos = ['Productos', 'Servicios', 'Empleados'];
    echo json_encode($datos, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
}
```

#### Manejo de Errores HTTP

El **código de estado 404 (Not Found)** se genera cuando una ruta no existe:
```php
else {
    // Cabecera HTTP 404 (opcional pero recomendado)
    http_response_code(404);
    
    // Mensaje amigable al usuario
    echo "<h2>404 - Ruta no encontrada</h2>";
    echo "<p>Lo siento, la página que estás buscando no existe.</p>";
    
    // Listado de rutas disponibles
    echo "<ul>";
    foreach (array_keys($routes['GET']) as $route) {
        echo "<li><a href='$route'>$route</a></li>";
    }
    echo "</ul>";
}
```

---

### Ejemplo Real Implementado: Ruta Personalizada `/hola`

En nuestra práctica, hemos implementado una ruta personalizada que demuestra los conceptos fundamentales:

#### Código de la Ruta:
```php
'/hola' => function() {
    echo "<h1>¡Bienvenido/a!</h1>";
    echo "<p>Esta es una ruta personalizada creada para la práctica de enrutamiento.</p>";
    echo "<p>Fecha y hora actual: " . date('d/m/Y H:i:s') . "</p>";
},
```

#### Flujo de Ejecución:
1. Usuario accede a `http://localhost:8000/hola`
2. El servidor captura: `$_SERVER['REQUEST_URI']` = `/hola`
3. Se normaliza el path eliminando la base del proyecto
4. Se busca en `$routes['GET']['/hola']`
5. Se ejecuta la función anónima asociada
6. El navegador recibe el HTML generado

#### Sistema Completo de Enrutamiento (archivo index.php):
```php
<?php
$routes = [
    'GET' => [
        '/' => function() { 
            echo "<h1>Página Principal</h1>";
            echo "<p>Bienvenido al sistema de enrutamiento</p>"; 
        },
        '/contacto' => function() { 
            echo "<h1>Página de Contacto</h1>";
            echo "<p>Contáctanos en: contacto@ejemplo.com</p>"; 
        },
        '/acerca' => function() { 
            echo "<h1>Acerca de Nosotros</h1>";
            echo "<p>Sistema de enrutamiento desarrollado para SGE</p>"; 
        },
        '/hola' => function() {
            echo "<h1>¡Bienvenido/a!</h1>";
            echo "<p>Esta es una ruta personalizada creada para la práctica.</p>";
            echo "<p>Fecha y hora actual: " . date('d/m/Y H:i:s') . "</p>";
        },
        '/menu' => function() { 
            $elementos = ['Productos','Servicios','Empleados'];
            echo json_encode($elementos, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        },
        '/tabla' => function() { 
            $alumnos = [
                ["id" => 1, "nombre" => "Ana", "curso" => "DAM 1", "nota" => 8.5],
                ["id" => 2, "nombre" => "Luis", "curso" => "DAW 2", "nota" => 6.7]
            ];
            echo json_encode($alumnos, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        },
    ]
];

// Captura de la solicitud
$method = $_SERVER['REQUEST_METHOD'];
$path = $_SERVER['REQUEST_URI'];

// Análisis de la URL
$parsed = parse_url($path);
$cleanPath = $parsed['path'];

// Normalización del path
$base = '/dam-2/.../102-Actividad%20EVAL';
$finalPath = str_replace($base, '', $cleanPath);

if (empty($finalPath)) {
    $finalPath = '/';
}

// Resolución y ejecución
if (isset($routes[$method][$finalPath])) {
    $routes[$method][$finalPath]();
} else {
    http_response_code(404);
    echo "<h2>404 - Ruta no encontrada</h2>";
    echo "<p>Lo siento, la página que estás buscando no existe.</p>";
    echo "<p>Rutas disponibles:</p>";
    echo "<ul>";
    foreach (array_keys($routes['GET']) as $route) {
        echo "<li><a href='$route'>$route</a></li>";
    }
    echo "</ul>";
}
?>
```

### Errores Comunes y Cómo Evitarlos

#### ❌ Error 1: No normalizar la ruta base
```php
// INCORRECTO: No eliminar la ruta base del proyecto
$finalPath = $_SERVER['REQUEST_URI'];  // '/dam-2/.../contacto'
```
**Solución:** Siempre eliminar la ruta base antes de buscar en el array de rutas.

#### ❌ Error 2: No validar el método HTTP
```php
// INCORRECTO: No diferenciar entre GET y POST
if (isset($routes[$finalPath])) { ... }
```
**Solución:** Siempre validar el método HTTP primero: `$routes[$method][$finalPath]`

#### ❌ Error 3: No manejar la ruta raíz vacía
```php
// INCORRECTO: No contemplar cuando $finalPath queda vacío
// Esto causaría que '/' no funcione
```
**Solución:** Validar: `if (empty($finalPath)) { $finalPath = '/'; }`

#### ❌ Error 4: No enviar cabeceras HTTP apropiadas
```php
// INCORRECTO: Solo mostrar mensaje sin cabecera 404
echo "Página no encontrada";
```
**Solución:** Usar `http_response_code(404);` antes del mensaje.

#### ❌ Error 5: URLs con espacios sin codificar
```php
// INCORRECTO: Comparar sin considerar caracteres codificados
$base = '/carpeta con espacios/';  // No coincidirá con '%20'
```
**Solución:** Usar `urlencode()` o trabajar con URLs ya codificadas.

### Pruebas Realizadas

| URL Solicitada | Resultado Esperado | Estado |
|----------------|-------------------|--------|
| `http://localhost:8000/` | Página principal | ✅ OK |
| `http://localhost:8000/contacto` | Página de contacto | ✅ OK |
| `http://localhost:8000/acerca` | Acerca de nosotros | ✅ OK |
| `http://localhost:8000/hola` | Mensaje de bienvenida personalizado | ✅ OK |
| `http://localhost:8000/menu` | JSON con elementos del menú | ✅ OK |
| `http://localhost:8000/tabla` | JSON con datos de alumnos | ✅ OK |
| `http://localhost:8000/inexistente` | Error 404 amigable con rutas disponibles | ✅ OK |

---

El enrutamiento es un **concepto fundamental en la arquitectura de aplicaciones web modernas** que permite organizar y gestionar eficientemente las diferentes URLs de un sistema. A través de esta práctica, hemos implementado un enrutador básico pero funcional en PHP que demuestra:

1. **Separación de responsabilidades**: Cada ruta tiene su lógica independiente
2. **Centralización**: Un único punto de entrada gestiona todas las peticiones
3. **Escalabilidad**: Fácil agregar nuevas rutas sin modificar la estructura
4. **Experiencia de usuario**: URLs limpias y mensajes de error informativos

Este conocimiento se conecta directamente con otros contenidos de la unidad:

- **Organización de la información**: El enrutamiento es el primer paso para estructurar cómo se accede a los datos en una aplicación
- **Definición de campos**: Las rutas determinan qué campos de información se exponen y cómo se presentan (HTML, JSON, etc.)
- **APIs REST**: El enrutamiento con métodos HTTP (GET, POST, PUT, DELETE) es la base de las arquitecturas RESTful
- **Bases de datos**: Las rutas actúan como interfaz entre el cliente y las consultas a la base de datos
- **MVC (Modelo-Vista-Controlador)**: El router es el componente que conecta las peticiones HTTP con los controladores apropiados

En proyectos reales, este concepto se amplía con:
- **Rutas dinámicas con parámetros**: `/usuario/{id}`, `/producto/{categoria}/{id}`
- **Middleware**: Validación, autenticación, logging antes de ejecutar el handler
- **Grupos de rutas**: Organización por módulos o funcionalidades
- **Gestión de sesiones y autenticación**: Control de acceso por ruta

El dominio del enrutamiento es esencial para cualquier desarrollador web, ya que es la base sobre la que se construyen aplicaciones escalables, mantenibles y profesionales. Los frameworks modernos (Laravel, Symfony, Express, Django) utilizan estos mismos principios, pero con mayor complejidad y funcionalidades adicionales.