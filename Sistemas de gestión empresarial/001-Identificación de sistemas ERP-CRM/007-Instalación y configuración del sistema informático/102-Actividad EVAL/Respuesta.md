He desarrollado un sistema ERP completamente funcional y accesible vía web, diseñado para gestionar los recursos empresariales de manera integrada. La elección de una arquitectura web responde a las necesidades actuales del mercado empresarial, donde la accesibilidad remota, la facilidad de despliegue y el bajo costo de mantenimiento son factores críticos.

### Tecnologías Utilizadas

#### Frontend
Para la interfaz de usuario he seleccionado las tecnologías web estándar:

- **HTML5**: Estructura semántica del contenido, proporcionando una base sólida y accesible para todas las páginas del sistema (login, dashboard, gestión de clientes, productos, ventas e inventario).

- **CSS3**: Diseño responsive y moderno que garantiza una experiencia de usuario óptima en diferentes dispositivos. He implementado un diseño limpio con Flexbox y Grid para la disposición de elementos, asegurando que el sistema sea usable tanto en escritorio como en dispositivos móviles.

- **JavaScript (ES6+)**: Implementación de toda la lógica del lado del cliente, incluyendo:
  - Comunicación asíncrona con el backend mediante la API Fetch
  - Validación de formularios en tiempo real
  - Actualización dinámica de la interfaz sin recargar la página
  - Gestión de autenticación y tokens JWT
  - Cálculos automáticos (totales de ventas, control de stock)

#### Backend
Para el servidor y la lógica de negocio he utilizado:

- **PHP**: Lenguaje del lado del servidor que gestiona toda la lógica de negocio, autenticación, y operaciones CRUD. He elegido PHP por su amplia adopción en el mercado empresarial (73% de sitios web según W3Techs) y su compatibilidad con prácticamente cualquier servicio de hosting compartido.

- **MySQL**: Sistema de gestión de base de datos relacional que almacena toda la información del ERP de forma estructurada y segura. MySQL garantiza integridad de datos mediante transacciones ACID, esenciales para operaciones empresariales.

### Arquitectura del Sistema

El sistema sigue una arquitectura cliente-servidor con API REST:

1. **Cliente (Frontend)**: Los archivos HTML, CSS y JavaScript se ejecutan en el navegador del usuario, proporcionando una interfaz interactiva.

2. **Servidor (Backend)**: Scripts PHP procesan las peticiones HTTP, ejecutan la lógica de negocio y se comunican con la base de datos.

3. **Base de Datos**: MySQL almacena de forma persistente usuarios, clientes, productos, ventas e inventario.

Esta separación de responsabilidades permite escalabilidad, mantenimiento más sencillo y la posibilidad de desarrollar aplicaciones móviles o integraciones con otros sistemas en el futuro.

---

### Conexión con la Base de Datos

He implementado la conexión con MySQL utilizando **PDO (PHP Data Objects)**, que es el estándar moderno en PHP para acceso a bases de datos. PDO ofrece varias ventajas sobre las extensiones antiguas como mysql o mysqli:

#### Archivo de Configuración (`backend/config/database.php`)

```php
<?php
// Configuración de la base de datos
$host = "localhost";
$dbname = "erp_sistema";
$username = "erp_sistema";
$password = "erp_sistema";

try {
    $pdo = new PDO(
        "mysql:host=$host;dbname=$dbname;charset=utf8", 
        $username, 
        $password
    );
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    http_response_code(500);
    die(json_encode([
        'success' => false, 
        'message' => 'Error de conexión a la base de datos'
    ]));
}
?>
```

#### Explicación Técnica

1. **Cadena de Conexión DSN**: `mysql:host=$host;dbname=$dbname;charset=utf8`
   - Especifica el driver MySQL
   - Define el host (servidor de base de datos)
   - Selecciona la base de datos específica
   - Establece el charset UTF-8 para soporte internacional

2. **Configuración de Atributos PDO**:
   - `ATTR_ERRMODE`: Modo de manejo de errores mediante excepciones, facilitando la detección de problemas
   - `ATTR_DEFAULT_FETCH_MODE`: Retorna resultados como arrays asociativos, mejorando la legibilidad del código

3. **Manejo de Excepciones**: El bloque try-catch captura errores de conexión y devuelve una respuesta HTTP 500 con mensaje JSON, siguiendo las buenas prácticas de API REST.

### Seguridad en las Consultas

He implementado **consultas preparadas (prepared statements)** en todas las operaciones con la base de datos para prevenir inyecciones SQL. Ejemplo en la gestión de productos:

```php
// Crear producto con consulta preparada
$stmt = $pdo->prepare("
    INSERT INTO productos (nombre, descripcion, precio, stock, fecha_creacion, activo) 
    VALUES (?, ?, ?, ?, NOW(), 1)
");

$stmt->execute([
    $input['nombre'],
    $input['descripcion'] ?? '',
    floatval($input['precio']),
    intval($input['stock'])
]);
```

Las consultas preparadas separan la estructura SQL de los datos del usuario, haciendo imposible que un atacante inyecte código SQL malicioso.

### Funciones de Seguridad Adicionales

He implementado funciones auxiliares en el archivo de configuración:

```php
// Sanitización de entradas
function sanitizeInput($data) {
    if (is_array($data)) {
        return array_map('sanitizeInput', $data);
    }
    return htmlspecialchars(trim($data), ENT_QUOTES, 'UTF-8');
}

// Validación de campos requeridos
function validateInput($data, $required_fields) {
    $errors = [];
    foreach ($required_fields as $field) {
        if (empty($data[$field])) {
            $errors[] = "El campo {$field} es requerido";
        }
    }
    return $errors;
}
```

### Estructura de Base de Datos

He diseñado un esquema relacional normalizado con las siguientes tablas:

- **usuarios**: Gestión de acceso al sistema con contraseñas hasheadas
- **clientes**: Información de clientes con validación de datos únicos
- **productos**: Catálogo de productos con control de stock
- **ventas**: Registro de operaciones comerciales
- **detalle_ventas**: Desglose de productos por venta (relación muchos a muchos)

Todas las tablas incluyen índices en campos de búsqueda frecuente para optimizar el rendimiento.

---

### Ejemplo Práctico: Sistema de Inicio de Sesión

Voy a detallar el flujo completo de autenticación, que es una operación fundamental en cualquier sistema empresarial.

#### Paso 1: Interfaz de Usuario (Frontend)

El usuario accede a `frontend/index.html` y visualiza un formulario de login:

```html
<form id="loginForm" class="login-form">
    <div class="form-group">
        <label for="username">Usuario</label>
        <input type="text" id="username" name="username" required>
    </div>
    
    <div class="form-group">
        <label for="password">Contraseña</label>
        <input type="password" id="password" name="password" required>
    </div>
    
    <button type="submit" class="btn-login">Iniciar Sesión</button>
</form>
```

#### Paso 2: Captura de Datos (JavaScript)

El archivo `frontend/js/login.js` intercepta el envío del formulario y realiza la petición al backend:

```javascript
loginForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    // Validación básica en el cliente
    if (!username || !password) {
        showError('Por favor, complete todos los campos.');
        return;
    }
    
    try {
        // Petición HTTP POST al endpoint de login
        const response = await fetch('../backend/api/login.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Guardar token JWT y datos de usuario
            localStorage.setItem('erp_token', data.token);
            localStorage.setItem('erp_user', JSON.stringify(data.user));
            
            // Redirigir al dashboard
            window.location.href = 'dashboard.html';
        } else {
            showError(data.message);
        }
        
    } catch (error) {
        showError('Error de conexión. Por favor, intente nuevamente.');
    }
});
```

**Explicación del código**:
- `e.preventDefault()`: Evita el envío tradicional del formulario
- `fetch()`: Realiza una petición HTTP asíncrona al servidor
- `JSON.stringify()`: Convierte los datos a formato JSON para enviarlos
- `localStorage`: Almacena el token de autenticación en el navegador para sesiones persistentes

#### Paso 3: Procesamiento en el Servidor (PHP)

El archivo `backend/api/login.php` recibe y procesa la petición:

```php
<?php
require_once '../config/database.php';

// Obtener datos del POST
$input = json_decode(file_get_contents('php://input'), true);

$username = sanitizeInput($input['username'] ?? '');
$password = $input['password'] ?? '';

// Validar campos requeridos
if (empty($username) || empty($password)) {
    http_response_code(400);
    echo json_encode([
        'success' => false, 
        'message' => 'Usuario y contraseña son requeridos'
    ]);
    exit();
}

try {
    // Buscar usuario en la base de datos con consulta preparada
    $stmt = $pdo->prepare("
        SELECT id, username, password, nombre, email, activo 
        FROM usuarios 
        WHERE username = ? AND activo = 1
    ");
    $stmt->execute([$username]);
    $user = $stmt->fetch();
    
    // Verificar usuario y contraseña
    if ($user && password_verify($password, $user['password'])) {
        // Actualizar último acceso
        $update_stmt = $pdo->prepare("
            UPDATE usuarios 
            SET ultimo_acceso = NOW() 
            WHERE id = ?
        ");
        $update_stmt->execute([$user['id']]);
        
        // Generar token JWT
        $token = generateJWT($user['id'], $user['username']);
        
        // Eliminar contraseña de la respuesta
        unset($user['password']);
        
        echo json_encode([
            'success' => true,
            'token' => $token,
            'user' => $user,
            'message' => 'Login exitoso'
        ]);
    } else {
        http_response_code(401);
        echo json_encode([
            'success' => false, 
            'message' => 'Credenciales inválidas'
        ]);
    }
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false, 
        'message' => 'Error del servidor'
    ]);
}
?>
```

**Explicación del flujo**:

1. **Recepción de Datos**: `file_get_contents('php://input')` lee el cuerpo de la petición HTTP POST
2. **Sanitización**: Limpieza de datos de entrada para prevenir XSS
3. **Validación**: Verificación de campos requeridos
4. **Consulta a Base de Datos**: Búsqueda del usuario con consulta preparada
5. **Verificación de Contraseña**: `password_verify()` compara de forma segura el hash almacenado
6. **Generación de Token**: Creación de JWT para autenticación en futuras peticiones
7. **Respuesta JSON**: Envío de datos estructurados al cliente

#### Paso 4: Interacción con MySQL

La consulta SQL ejecutada es:

```sql
SELECT id, username, password, nombre, email, activo 
FROM usuarios 
WHERE username = ? AND activo = 1
```

**Proceso en la base de datos**:
1. MySQL busca en la tabla `usuarios` usando el índice en el campo `username`
2. Filtra por usuarios activos (`activo = 1`)
3. Retorna la fila correspondiente con todos los campos especificados
4. PHP recibe los datos y realiza la verificación de contraseña

#### Paso 5: Respuesta y Redirección

Si la autenticación es exitosa:
- El servidor retorna un objeto JSON con `success: true`, el token JWT y los datos del usuario
- JavaScript guarda el token en localStorage
- El navegador redirige automáticamente a `dashboard.html`
- El token se incluye en todas las peticiones posteriores mediante el header `Authorization: Bearer {token}`

Si falla la autenticación:
- El servidor retorna código HTTP 401 (Unauthorized)
- JavaScript muestra el mensaje de error en la interfaz
- El usuario permanece en la página de login

### Seguridad Implementada

1. **Contraseñas Hasheadas**: Uso de `password_hash()` con algoritmo bcrypt
2. **Consultas Preparadas**: Prevención de inyección SQL
3. **HTTPS Recomendado**: Para cifrar la comunicación en producción
4. **Tokens JWT**: Autenticación stateless y segura
5. **Validación Doble**: Cliente (JavaScript) y servidor (PHP)

---

Para finalizar, he seguido todos los pasos necesarios para construir un sistema ERP funcional:  
- Selección adecuada de tecnologías vistas en clase (HTML, CSS, JS, PHP y MySQL).  
- Implementación de una conexión segura con la base de datos usando PDO.  
- Creación de endpoints reales que permiten interactuar con la base de datos (login, clientes, productos, etc.).  
- Desarrollo de un ejemplo práctico donde el frontend consume el backend mediante fetch.

Considero que esta actividad me ha permitido entender cómo se integra un ERP real en un entorno web y por qué es importante seleccionar tecnologías adecuadas en entornos empresariales.
