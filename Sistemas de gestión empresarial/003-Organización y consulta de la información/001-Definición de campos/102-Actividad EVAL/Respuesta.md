El **enrutamiento (routing)** es el mecanismo fundamental en aplicaciones web que permite gestionar las diferentes URLs que un usuario solicita y asociarlas con las acciones correspondientes que debe ejecutar el servidor. En lugar de crear un archivo PHP separado para cada página (como `contacto.php`, `acerca.php`), el enrutamiento centraliza todas las peticiones en un único punto de entrada, determinando dinámicamente qué código ejecutar según la ruta solicitada.

Este concepto es **esencial en el desarrollo web moderno** porque:

- Permite crear **APIs RESTful** para comunicación entre aplicaciones
- Facilita el desarrollo de **aplicaciones de página única (SPA)**
- Mejora la **escalabilidad** y **mantenibilidad** del código
- Implementa **URLs amigables** para el SEO y la experiencia de usuario
- Separa las responsabilidades entre la captura de peticiones y la lógica de negocio

El enrutamiento se utiliza en prácticamente todos los frameworks modernos como Laravel, Symfony, Express.js, Django y en cualquier aplicación que necesite gestionar múltiples recursos de forma organizada y profesional.

---

### Estructura de Datos de Rutas

Un sistema de enrutamiento se basa en un **array asociativo multidimensional** que organiza las rutas por **método HTTP** y **path**:

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

**Terminología técnica fundamental:**

- **Método HTTP**: Verbo que indica el tipo de operación (GET para obtener, POST para crear, PUT para actualizar, DELETE para eliminar, PATCH para modificaciones parciales)
- **Path/Ruta**: La URL específica que el cliente solicita (ej: `/contacto`)
- **Handler/Controlador**: La función anónima (closure) que contiene el código a ejecutar cuando se accede a la ruta
- **Callback**: Término alternativo para referirse al handler
- **Request URI**: URL completa capturada desde el servidor
- **Response**: La salida generada que se envía al cliente

### Proceso de Enrutamiento Paso a Paso

#### Paso 1: Captura de la Solicitud HTTP
```php
$method = $_SERVER['REQUEST_METHOD'];  // Obtiene el método: 'GET', 'POST', etc.
$path = $_SERVER['REQUEST_URI'];      // Obtiene la URL completa solicitada
```

El servidor web captura automáticamente toda la información de la solicitud HTTP en la superglobal `$_SERVER`, incluyendo el método, la URI, headers, y otros metadatos.

#### Paso 2: Análisis y Limpieza de la URL
```php
$parsed = parse_url($path);           // Separa componentes: scheme, host, path, query
$cleanPath = $parsed['path'];         // Extrae solo el path sin query strings (?param=value)
```

La función `parse_url()` descompone la URL en sus partes constituyentes, permitiendo trabajar solo con el path y eliminar parámetros de consulta que podrían interferir con la comparación de rutas.

#### Paso 3: Normalización del Path
```php
// Eliminar la ruta base del proyecto para trabajar con rutas relativas
$base = '/dam-2/Sistemas%20de%20gesti%C3%B3n%20empresarial/003-Organizaci%C3%B3n%20y%20consulta%20de%20la%20informaci%C3%B3n/001-Definici%C3%B3n%20de%20campos/102-Actividad%20EVAL';
$finalPath = str_replace($base, '', $cleanPath);

// Manejar el caso de la ruta raíz
if (empty($finalPath)) {
    $finalPath = '/';
}
```

Este paso es crucial porque las aplicaciones PHP en subdirectorios necesitan eliminar el prefijo del proyecto para que las rutas definidas coincidan correctamente.

#### Paso 4: Resolución y Ejecución de la Ruta
```php
if (isset($routes[$method][$finalPath])) {
    // Ruta encontrada: ejecutar el handler correspondiente
    $routes[$method][$finalPath]();
} else {
    // Ruta no encontrada: responder con error 404
    http_response_code(404);
    echo "<h2>404 - Ruta no encontrada</h2>";
    echo "<p>Lo siento, la página que estás buscando no existe.</p>";
}
```

El sistema verifica primero que el método HTTP coincida y luego que la ruta exista. Si ambos coinciden, ejecuta la función asociada; de lo contrario, genera una respuesta HTTP 404.

### Tipos de Respuestas en Rutas

#### Respuestas HTML (para navegadores web)
```php
'/hola' => function() {
    echo "<h1>¡Bienvenido/a!</h1>";
    echo "<p>Esta es una ruta personalizada.</p>";
}
```

#### Respuestas JSON (para APIs)
```php
'/menu' => function() {
    $datos = ['Productos', 'Servicios', 'Empleados'];
    header('Content-Type: application/json');
    echo json_encode($datos, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
}
```

Las constantes `JSON_UNESCAPED_UNICODE` y `JSON_PRETTY_PRINT` mejoran la legibilidad al no escapar caracteres Unicode y formatear el JSON con indentación.

---

### Implementación Real en el Proyecto

En nuestra práctica, hemos implementado un sistema completo de enrutamiento en el archivo **index.php**:

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
            echo "<p>Esta es una ruta personalizada creada para la práctica de enrutamiento.</p>";
            echo "<p>Fecha y hora actual: " . date('d/m/Y H:i:s') . "</p>";
        },
        '/menu' => function() { 
            $elementos = ['Productos','Servicios','Empleados'];
            echo json_encode($elementos, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        },
        '/tabla' => function() { 
            $alumnos = [
                ["id" => 1, "nombre" => "Ana", "apellidos" => "García López", 
                 "curso" => "DAM 1", "nota" => 8.5, "estado" => "Aprobado"],
                ["id" => 2, "nombre" => "Luis", "apellidos" => "Martínez Pérez", 
                 "curso" => "DAW 2", "nota" => 6.7, "estado" => "Aprobado"],
                ["id" => 3, "nombre" => "María", "apellidos" => "Sánchez Ruiz", 
                 "curso" => "ASIR 1", "nota" => 4.9, "estado" => "Suspenso"]
            ];
            echo json_encode($alumnos, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        },
    ]
];

$method = $_SERVER['REQUEST_METHOD'];
$path = $_SERVER['REQUEST_URI'];
$parsed = parse_url($path);
$cleanPath = $parsed['path'];

$base = '/dam-2/Sistemas%20de%20gesti%C3%B3n%20empresarial/003-Organizaci%C3%B3n%20y%20consulta%20de%20la%20informaci%C3%B3n/001-Definici%C3%B3n%20de%20campos/102-Actividad%20EVAL';
$finalPath = str_replace($base, '', $cleanPath);

if (empty($finalPath)) {
    $finalPath = '/';
}

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

### Ejemplo de Flujo Completo: Ruta `/hola`

**Solicitud del usuario:**
```
http://localhost:8000/hola
```

**Procesamiento interno:**
1. Usuario escribe la URL en el navegador
2. Servidor captura: `$_SERVER['REQUEST_METHOD']` = `'GET'`
3. Servidor captura: `$_SERVER['REQUEST_URI']` = `/dam-2/.../102-Actividad%20EVAL/hola`
4. Se parsea la URL y se extrae el path limpio
5. Se elimina la ruta base: `/hola`
6. Se busca en el array: `$routes['GET']['/hola']`
7. Se ejecuta la función anónima asociada
8. Se genera el HTML y se envía al navegador
9. El usuario ve el mensaje de bienvenida con la fecha y hora

### Errores Comunes y Cómo Evitarlos

#### ❌ Error 1: No normalizar la ruta base del proyecto
```php
// INCORRECTO: Usar directamente $_SERVER['REQUEST_URI']
$finalPath = $_SERVER['REQUEST_URI'];  
// Resultado: '/dam-2/.../102-Actividad%20EVAL/contacto'
// Problema: No coincide con '/contacto' en el array $routes
```

**✅ Solución:** Siempre eliminar la ruta base antes de buscar en el array de rutas.
```php
$base = '/dam-2/.../102-Actividad%20EVAL';
$finalPath = str_replace($base, '', $cleanPath);
```

#### ❌ Error 2: No diferenciar entre métodos HTTP
```php
// INCORRECTO: No validar el método HTTP
if (isset($routes[$finalPath])) { 
    $routes[$finalPath](); 
}
// Problema: Un POST a /guardar podría ejecutar un GET accidentalmente
```

**✅ Solución:** Siempre validar el método HTTP primero.
```php
if (isset($routes[$method][$finalPath])) {
    $routes[$method][$finalPath]();
}
```

#### ❌ Error 3: No manejar la ruta raíz vacía
```php
// INCORRECTO: No contemplar cuando $finalPath queda vacío tras normalizar
// Problema: La ruta '/' nunca funcionará
```

**✅ Solución:** Validar y asignar `/` si el path está vacío.
```php
if (empty($finalPath)) {
    $finalPath = '/';
}
```

#### ❌ Error 4: No enviar códigos de estado HTTP apropiados
```php
// INCORRECTO: Solo mostrar mensaje sin cabecera HTTP
else {
    echo "Página no encontrada";
}
// Problema: El navegador recibe código 200 (OK) cuando debería ser 404
```

**✅ Solución:** Usar `http_response_code()` para establecer el código correcto.
```php
else {
    http_response_code(404);
    echo "<h2>404 - Ruta no encontrada</h2>";
}
```

#### ❌ Error 5: No codificar/decodificar URLs con caracteres especiales
```php
// INCORRECTO: Comparar sin considerar caracteres codificados
$base = '/carpeta con espacios/';  
// Problema: No coincidirá con '/carpeta%20con%20espacios/'
```

**✅ Solución:** Usar URLs ya codificadas o aplicar `urlencode()`/`urldecode()` consistentemente.

### Pruebas Realizadas y Resultados

| URL Solicitada | Método | Resultado Esperado | Estado |
|----------------|--------|-------------------|--------|
| `http://localhost:8000/` | GET | Página principal | ✅ OK |
| `http://localhost:8000/contacto` | GET | Página de contacto | ✅ OK |
| `http://localhost:8000/acerca` | GET | Acerca de nosotros | ✅ OK |
| `http://localhost:8000/hola` | GET | Mensaje de bienvenida personalizado | ✅ OK |
| `http://localhost:8000/menu` | GET | JSON con elementos del menú | ✅ OK |
| `http://localhost:8000/tabla` | GET | JSON con datos de alumnos | ✅ OK |
| `http://localhost:8000/inexistente` | GET | Error 404 amigable con rutas disponibles | ✅ OK |

### Mejoras Implementadas en el Error 404

Nuestro manejo de error 404 incluye **características adicionales** que mejoran la experiencia de usuario:

1. **Código HTTP correcto:** `http_response_code(404)`
2. **Mensaje amigable:** Explicación clara del error
3. **Lista de rutas disponibles:** Enlaces clickeables a todas las rutas GET
4. **Navegación facilitada:** El usuario puede ir directamente a una ruta válida

Esto transforma un error frustrante en una oportunidad de navegación.

---

El enrutamiento es un **pilar fundamental en la arquitectura de aplicaciones web modernas** que hemos implementado exitosamente en esta práctica. Los conceptos clave dominados son:

1. **Separación de responsabilidades:** Cada ruta tiene su lógica independiente y bien definida
2. **Centralización:** Un único punto de entrada (`index.php`) gestiona todas las peticiones de forma organizada
3. **Escalabilidad:** Es sencillo agregar nuevas rutas sin modificar la estructura existente
4. **Experiencia de usuario:** URLs limpias, legibles y mensajes de error informativos
5. **Versatilidad:** Manejo de diferentes tipos de respuesta (HTML para vistas, JSON para APIs)

### Conexión con Otros Contenidos de la Unidad

El enrutamiento se relaciona directamente con múltiples aspectos del temario de **Sistemas de Gestión Empresarial**:

**Organización de la información:**
- El enrutamiento es el primer paso para estructurar cómo se accede a los datos
- Define la interfaz pública de nuestra aplicación
- Establece el punto de entrada para consultas y operaciones

**Definición de campos:**
- Las rutas determinan qué campos de información se exponen y en qué formato
- Ejemplo: `/tabla` expone campos como `id`, `nombre`, `curso`, `nota`, `estado`
- El formato de respuesta (HTML vs JSON) define cómo se presentan estos campos

**APIs RESTful:**
- El enrutamiento con métodos HTTP es la base de las arquitecturas REST
- GET para lectura, POST para creación, PUT para actualización, DELETE para eliminación
- Ejemplo: `GET /alumnos` lista alumnos, `POST /alumnos` crearía uno nuevo

**Bases de datos:**
- Las rutas actúan como interfaz entre el cliente y las consultas a la base de datos
- Ejemplo: `/tabla` en el futuro podría consultar `SELECT * FROM alumnos`
- El enrutamiento separa la petición HTTP de la lógica de acceso a datos

**Arquitectura MVC (Modelo-Vista-Controlador):**
- El router es el componente que conecta las peticiones HTTP con los controladores apropiados
- Facilita la implementación del patrón MVC en proyectos más complejos

### Proyección hacia Aplicaciones Reales

En entornos profesionales, este concepto se amplía con funcionalidades como:

- **Rutas dinámicas con parámetros:** `/usuario/{id}`, `/producto/{categoria}/{id}`
- **Middleware:** Validación, autenticación, logging antes de ejecutar el handler
- **Grupos de rutas:** Organización por módulos (admin, api, public)
- **Gestión de sesiones:** Control de acceso y permisos por ruta
- **CORS y seguridad:** Configuración de políticas de acceso entre dominios

Los frameworks profesionales como **Laravel** o **Symfony** utilizan estos mismos principios fundamentales que hemos aprendido, pero con mayor complejidad, abstracción y características adicionales.

El dominio del enrutamiento es **esencial para cualquier desarrollador web**, ya que es la base sobre la que se construyen aplicaciones escalables, mantenibles y profesionales en cualquier tecnología o framework moderno.