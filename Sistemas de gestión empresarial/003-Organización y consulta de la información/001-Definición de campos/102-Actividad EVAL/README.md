# Documentación de la Práctica de Enrutamiento en PHP

## Resumen de Cambios Realizados

### 1. Estructura del Sistema de Enrutamiento

El sistema de enrutamiento implementado utiliza un array asociativo `$routes` que organiza las rutas por método HTTP (GET, POST, etc.). Cada ruta está asociada a una función anónima que se ejecuta cuando se accede a ella.

```php
$routes = [
    'GET' => [
        '/' => function() { ... },
        '/contacto' => function() { ... },
        '/hola' => function() { ... }
    ]
];
```

### 2. Rutas Disponibles

#### Rutas Principales:
- **`/`** (Ruta raíz): Muestra la página principal con un mensaje de bienvenida
- **`/contacto`**: Muestra información de contacto
- **`/acerca`**: Muestra información acerca del sistema
- **`/hola`** ⭐ (NUEVA): Ruta personalizada que muestra un mensaje de bienvenida con la fecha y hora actual
- **`/menu`**: Devuelve un JSON con elementos del menú
- **`/tabla`**: Devuelve un JSON con información de alumnos

### 3. Nueva Ruta Personalizada: `/hola`

Se ha agregado la ruta `/hola` que:
- Muestra un título de bienvenida
- Incluye un mensaje descriptivo
- Muestra la fecha y hora actual del servidor

```php
'/hola' => function() {
    echo "<h1>¡Bienvenido/a!</h1>";
    echo "<p>Esta es una ruta personalizada creada para la práctica de enrutamiento.</p>";
    echo "<p>Fecha y hora actual: " . date('d/m/Y H:i:s') . "</p>";
},
```

### 4. Manejo Mejorado de Errores 404

Se ha modificado el manejo de rutas no encontradas para mostrar:
- Un mensaje amigable al usuario
- Una explicación clara del error
- Una lista de rutas disponibles con enlaces clickeables

```php
if (isset($routes[$method][$finalPath])) {
    $routes[$method][$finalPath]();
} else {
    echo "<h2>404 - Ruta no encontrada</h2>";
    echo "<p>Lo siento, la página que estás buscando no existe.</p>";
    echo "<p>Rutas disponibles:</p>";
    echo "<ul>";
    foreach (array_keys($routes['GET']) as $route) {
        echo "<li><a href='$route'>$route</a></li>";
    }
    echo "</ul>";
}
```

### 5. Cómo Funciona el Enrutamiento

1. **Captura de la solicitud**: El servidor recibe la solicitud HTTP y extrae:
   - El método HTTP (`$_SERVER['REQUEST_METHOD']`)
   - La ruta solicitada (`$_SERVER['REQUEST_URI']`)

2. **Limpieza de la ruta**: 
   - Se parsea la URL para obtener solo el path
   - Se elimina la ruta base del proyecto
   - Si la ruta está vacía, se establece como `/`

3. **Búsqueda y ejecución**:
   - Se busca la ruta en el array `$routes`
   - Si existe, se ejecuta la función asociada
   - Si no existe, se muestra el error 404 personalizado

### 6. Manejo de Diferentes Métodos HTTP

El sistema está preparado para manejar diferentes métodos HTTP:
- **GET**: Para obtener información
- **POST**: Para enviar datos (se puede agregar fácilmente)
- **PUT, DELETE, etc.**: Pueden agregarse siguiendo el mismo patrón

Ejemplo de cómo agregar una ruta POST:
```php
$routes = [
    'GET' => [ ... ],
    'POST' => [
        '/guardar' => function() {
            // Procesar datos del formulario
            $datos = $_POST;
            echo "Datos guardados correctamente";
        }
    ]
];
```

### 7. Ventajas de Este Sistema

- **Organización**: Todas las rutas están centralizadas en un solo lugar
- **Flexibilidad**: Fácil agregar, modificar o eliminar rutas
- **Escalabilidad**: Se puede extender para incluir middleware, validaciones, etc.
- **Mantenibilidad**: Código claro y fácil de entender

### 8. Instrucciones de Uso

1. Iniciar el servidor: `php -S localhost:8000`
2. Acceder desde el navegador: `http://localhost:8000/`
3. Probar las diferentes rutas agregando el path al final de la URL

### 9. Próximos Pasos (Mejoras Posibles)

- Implementar rutas dinámicas con parámetros (ej: `/usuario/{id}`)
- Agregar middleware para autenticación
- Separar las rutas en diferentes archivos según su funcionalidad
- Implementar un sistema de plantillas para las vistas
- Agregar soporte para rutas POST con validación de datos
