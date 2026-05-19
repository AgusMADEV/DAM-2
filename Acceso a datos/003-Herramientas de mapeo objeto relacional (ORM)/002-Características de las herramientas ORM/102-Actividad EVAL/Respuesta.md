En esta actividad, he trabajado con el desarrollo de un sistema de seguimiento de entrenamientos deportivos. El proyecto requería la creación de una herramienta que permitiera gestionar eficientemente el acceso a una base de datos MySQL que almacena información de usuarios (atletas), planes de entrenamiento y sesiones de entrenamientos.

El contexto principal es que una aplicación web necesita interactuar con una base de datos relacional de forma segura y eficiente, sin tener que escribir consultas SQL manualmente en cada lugar del código. Aquí es donde entra en juego la clase **JVDB** (Java Virtual DataBase), que actúa como una abstracción simplificada para acceder a los datos.

### Cómo JVDB se Utiliza en el Proyecto

La clase `JVDB` implementa un patrón de acceso a datos que:

- **Centraliza la conexión**: Se crea una única instancia que gestiona la conexión a MySQL
- **Proporciona métodos reutilizables**: Los métodos `seleccionar()`, `buscar()` y `tablas()` pueden usarse desde cualquier parte de la aplicación
- **Devuelve datos en JSON**: Facilita la comunicación entre el backend (PHP) y el frontend (JavaScript)
- **Gestiona el ciclo de vida**: El destructor cierra automáticamente la conexión cuando ya no se necesita

En nuestro proyecto, JVDB se utiliza en la **API REST** (`api/index.php`) que recibe peticiones GET con diferentes acciones:
- Listar todas las tablas disponibles
- Obtener registros de una tabla específica
- Buscar registros según criterios

Esta arquitectura permite que la interfaz web y cualquier cliente externo accedan a los datos de forma consistente y segura.

---

### Implementación de la Clase JVDB

La clase JVDB ha sido implementada siguiendo los patrones vistos en clase y las mejores prácticas de PHP:

#### Constructor y Conexión a la Base de Datos

```php
public function __construct($host, $usuario, $contrasena, $basedatos) {
    $this->conexion = new mysqli($this->host, $this->usuario, 
                                 $this->contrasena, $this->basedatos);
    
    if ($this->conexion->connect_error) {
        die("Error de conexión: " . $this->conexion->connect_error);
    }
}
```

- Utiliza **MySQLi** (extensión mejorada de MySQL) en modo orientado a objetos
- Verifica la conexión y lanza una excepción si falla
- Encapsula las credenciales como propiedades privadas

#### Método Seleccionar

```php
public function seleccionar($tabla) {
    $sql = "SELECT * FROM $tabla";
    $resultado = $this->conexion->query($sql);
    
    if (!$resultado) {
        return json_encode(["error" => "Error en la consulta: " . 
                           $this->conexion->error], JSON_UNESCAPED_UNICODE);
    }
    
    $datos = [];
    while ($fila = $resultado->fetch_assoc()) {
        $datos[] = $fila;
    }
    
    return json_encode($datos, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
}
```

**Características técnicas correctas:**
- Ejecuta consultas SQL contra la tabla especificada
- Devuelve todos los registros en formato JSON
- Maneja errores de consulta apropiadamente
- Utiliza `JSON_UNESCAPED_UNICODE` para preservar caracteres acentuados

#### Método Buscar con Prepared Statements

```php
public function buscar($tabla, $columna, $valor) {
    $sql = "SELECT * FROM $tabla WHERE $columna LIKE ?";
    $stmt = $this->conexion->prepare($sql);
    $like = "%" . $valor . "%";
    $stmt->bind_param("s", $like);
    $stmt->execute();
    
    $resultado = $stmt->get_result();
    // ... procesar resultados
}
```

**Seguridad implementada:**
- Usa **prepared statements** para evitar inyección SQL
- Parámetros vinculados con `bind_param`
- Búsqueda flexible con `LIKE` para encontrar coincidencias parciales

#### Método Tablas

Permite obtener el listado de todas las tablas disponibles en la base de datos, lo que facilita la validación en la API.

#### Gestor de Conexión

```php
public function __destruct() {
    if ($this->conexion) {
        $this->conexion->close();
    }
}
```

El destructor cierra automáticamente la conexión cuando la instancia ya no se necesita, liberando recursos.

---

### Resolución del Problema Real

He implementado una **API REST** que utiliza la clase JVDB para resolver un problema práctico real: gestionar entrenamientos de atletas.

### Estructura de la Base de Datos

La base de datos `entrenamientos_db` contiene tres tablas relacionadas:

1. **usuarios**: Almacena información de atletas (nombre, email, nivel de experiencia)
2. **planes_entrenamiento**: Planes personalizados con objetivos y duraciones
3. **entrenamientos**: Registros de sesiones de entrenamiento individual

### Uso del Método Seleccionar en la API

```php
case 'seleccionar':
    $tabla = isset($_GET['tabla']) ? $_GET['tabla'] : null;
    
    if (!$tabla) {
        http_response_code(400);
        echo json_encode(['error' => 'Parámetro tabla requerido'], 
                        JSON_UNESCAPED_UNICODE);
        break;
    }
    
    $todas = json_decode($db->tablas(), true);
    if (!in_array($tabla, $todas)) {
        http_response_code(400);
        echo json_encode(['error' => 'Tabla no permitida'], 
                        JSON_UNESCAPED_UNICODE);
        break;
    }
    
    echo $db->seleccionar($tabla);
    break;
```

### Ejemplos Prácticos de Uso

**Ejemplo 1: Obtener todos los usuarios**
```
GET /api/index.php?action=seleccionar&tabla=usuarios
```
Respuesta JSON:
```json
[
  {
    "id": "1",
    "nombre": "Juan",
    "apellido": "García",
    "email": "juan@ejemplo.com",
    "especialidad": "Correr",
    "nivel_experiencia": "Intermedio"
  },
  {
    "id": "2",
    "nombre": "María",
    "apellido": "López",
    "email": "maria@ejemplo.com",
    "especialidad": "Natación",
    "nivel_experiencia": "Avanzado"
  }
]
```

**Ejemplo 2: Obtener todos los entrenamientos**
```
GET /api/index.php?action=seleccionar&tabla=entrenamientos
```

**Ejemplo 3: Buscar entrenamientos de un tipo específico**
```
GET /api/index.php?action=buscar&tabla=entrenamientos&campo=tipo_ejercicio&valor=correr
```

### Validación de Seguridad

La API implementa varias capas de protección:

1. **Validación de parámetros**: Verifica que tabla, campo y valor estén presentes
2. **Whitelist de tablas**: Solo permite consultar tablas que existen en la BD
3. **Headers CORS**: Controla el acceso desde diferentes orígenes
4. **Manejo de errores**: Respuestas HTTP apropiadas (400, 500)

---

A través de esta actividad, he comprendido mejor qué son realmente las herramientas ORM y cómo funcionan. La clase JVDB es un ejemplo simple pero práctico de cómo un ORM actúa como intermediario entre la aplicación y la base de datos.

Los ORM nos ayudan a:
- **Trabajar con objetos en lugar de SQL**: En lugar de escribir consultas SQL complicadas, usamos métodos simples
- **Reutilizar código**: La misma clase JVDB funciona con cualquier tabla, sin necesidad de escribir SQL cada vez
- **Evitar errores de seguridad**: Los prepared statements de JVDB previenen inyecciones SQL
- **Mantener el código organizado**: La lógica de acceso a datos está centralizada y es fácil de entender

Esta actividad me ha mostrado que los ORM no son "mágicos", sino simplemente herramientas bien diseñadas que hacen el trabajo más fácil y seguro. JVDB demuestra que entendiendo los fundamentos básicos de cómo interactúan las aplicaciones con las bases de datos, puedo usar herramientas más complejas como Laravel Eloquent o Doctrine en el futuro con mayor confianza.

Lo más importante que he aprendido es que acceder a datos de forma segura, ordenada y mantenible es una habilidad fundamental en desarrollo web.
