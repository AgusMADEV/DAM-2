En esta actividad he desarrollado un sistema ERP accesible a través de una **interfaz web**, con el objetivo de gestionar clientes, productos, inventario y ventas.  
Para la parte visual del proyecto he utilizado **HTML, CSS y JavaScript**, ya que son los lenguajes estándar para construir interfaces web interactivas.  
El backend lo he implementado con **PHP**, conectándolo a una base de datos **MySQL**, siguiendo las tecnologías vistas en clase y evitando herramientas no permitidas como Node.js o TypeScript.

---

Para comunicar el sistema ERP con la base de datos he utilizado **PDO en PHP**, ya que permite una conexión segura y preparada para manejar excepciones.

### Ejemplo real de conexión (`database.php`)
```php
$host = "localhost";
$dbname = "erp_sistema";
$username = "erp_sistema";
$password = "erp_sistema";

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Error de conexión: " . $e->getMessage());
}
```

También he aplicado funciones de seguridad como:  
- **Sanitización de datos** con `htmlspecialchars()`  
- **Validación de campos obligatorios**  
- **Uso de sentencias preparadas** para evitar inyecciones SQL  

---

Para demostrar la interacción entre el frontend y el backend, presento como ejemplo el proceso de **inicio de sesión** del ERP.  

### Ejemplo real: petición desde JavaScript (`login.js`)
```javascript
const response = await fetch('../backend/api/login.php', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        username: username,
        password: password
    })
});
```

### Ejemplo real: validación del usuario en PHP (`login.php`)
```php
$stmt = $pdo->prepare("SELECT id, username, password FROM usuarios WHERE username = ? AND activo = 1");
$stmt->execute([$username]);
$user = $stmt->fetch();

if ($user && password_verify($password, $user['password'])) {
    echo json_encode(['success' => true, 'message' => 'Login exitoso']);
} else {
    echo json_encode(['success' => false, 'message' => 'Credenciales inválidas']);
}
```

Con esto el sistema valida al usuario contra la base de datos y permite el acceso al panel principal.

---

Para finalizar, he seguido todos los pasos necesarios para construir un sistema ERP funcional:  
- Selección adecuada de tecnologías vistas en clase (HTML, CSS, JS, PHP y MySQL).  
- Implementación de una conexión segura con la base de datos usando PDO.  
- Creación de endpoints reales que permiten interactuar con la base de datos (login, clientes, productos, etc.).  
- Desarrollo de un ejemplo práctico donde el frontend consume el backend mediante fetch.

Considero que esta actividad me ha permitido entender cómo se integra un ERP real en un entorno web y por qué es importante seleccionar tecnologías adecuadas en entornos empresariales.
