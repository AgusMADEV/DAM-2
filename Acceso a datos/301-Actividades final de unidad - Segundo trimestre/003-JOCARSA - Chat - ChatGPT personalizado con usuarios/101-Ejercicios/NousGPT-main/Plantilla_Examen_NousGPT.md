# Oráculo Namek — Plantilla de Examen

**Alumno:** Luis Rodríguez Cedeño · **DNI:** 53945291X  
**Módulo:** Acceso a Datos · **Curso:** DAM2 2025/26

---

## 1. Introducción

- **Qué es:** Chat especializado en Dragon Ball con backend PHP + MySQL + frontend JS vanilla
- **Contexto:** Módulo de Acceso a Datos — sistema de chat temático con persistencia relacional, autenticación y API REST
- **Objetivos principales:**
  - Sistema multiusuario con auth (bcrypt, sesiones PHP)
  - CRUD conversaciones y mensajes sobre Dragon Ball
  - Integración con modelos IA especializados (Ollama local / OpenAI fallback)
  - Frontend SPA con dark mode, Markdown rendering, exportación
- **Tecnologías clave:**
  - PHP 8 (backend), MySQL (persistencia), JavaScript vanilla (frontend)
  - Ollama API (IA local), OpenAI API (fallback), bcrypt (hash contraseñas)
- **Arquitectura:** MVC — `api/` (controladores REST), `lib/` (motor IA Dragon Ball), `db.php` (PDO singleton), `config.php` (constantes), `index.php` (vista), `assets/` (JS+CSS)

---

## 2. Desarrollo de las partes

### 2.1 Base de datos y conexión PDO (Singleton)

- Patrón Singleton → una única conexión PDO reutilizada
- Base de datos `dragonball_chat`: tablas `usuarios`, `conversaciones`, `mensajes`
- Claves foráneas + índices de rendimiento

```php
// db.php — Singleton PDO
function get_pdo(): PDO {
    static $pdo = null;
    if ($pdo === null) {
        $dsn = 'mysql:unix_socket=' . DB_SOCKET . ';dbname=' . DB_NAME . ';charset=utf8mb4';
        $pdo = new PDO($dsn, DB_USER, DB_PASS, [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]);
    }
    return $pdo;
}
```

> **Explicación:** Se usa `static $pdo` para que solo se cree una conexión. El DSN conecta por socket UNIX a MySQL. Configuramos modo excepciones y fetch asociativo por defecto.

### 2.2 Autenticación con bcrypt

- Registro: `password_hash($password, PASSWORD_DEFAULT)` → hash bcrypt
- Login: `password_verify($password, $hash)` → verificación segura
- Sesiones PHP: `$_SESSION['user_id']`

```php
// api/auth.php — Registro
$hash = password_hash($password, PASSWORD_DEFAULT);
$stmt = $pdo->prepare("INSERT INTO usuarios (username, email, password_hash) VALUES (?, ?, ?)");
$stmt->execute([$username, $email, $hash]);

// api/auth.php — Login
$user = $pdo->query("SELECT * FROM usuarios WHERE email = ?")->fetch();
if ($user && password_verify($password, $user['password_hash'])) {
    $_SESSION['user_id'] = $user['id'];
}
```

> **Explicación:** `password_hash` genera un hash bcrypt seguro (salt automático). `password_verify` compara sin exponer el hash. La sesión PHP almacena el user_id autenticado.

### 2.3 API REST — Conversaciones y Mensajes

- `api/conversations.php`: GET (listar), POST create/rename/delete
- `api/messages.php`: GET (cargar historial), POST (enviar + generar respuesta IA)
- Rate limiting: máximo 12 mensajes/minuto por usuario

```php
// api/messages.php — Enviar mensaje y obtener respuesta IA
$history = build_chat_messages($conversation_id);
$reply = generate_assistant_reply($history, $model);

$pdo->beginTransaction();
$pdo->prepare("INSERT INTO mensajes (conversation_id, role, content) VALUES (?,?,?)")
    ->execute([$conversation_id, 'user', $user_message]);
$pdo->prepare("INSERT INTO mensajes (conversation_id, role, content) VALUES (?,?,?)")
    ->execute([$conversation_id, 'assistant', $reply]);
$pdo->commit();
```

> **Explicación:** Se construye el historial de la conversación, se envía al modelo IA, y ambos mensajes (usuario + asistente) se guardan en una transacción para garantizar consistencia.

### 2.4 Motor de IA con fallback en cascada

- Prioridad: Ollama (local) → OpenAI (nube) → Fallback local (pattern matching)
- Ollama: curl a `/api/chat` con stream=false  
- Fallback: respuestas predefinidas sobre Goku, Vegeta, transformaciones, técnicas, sagas de Dragon Ball

```php
// lib/assistant.php — Llamada a Ollama
$payload = json_encode([
    'model'   => $model,
    'messages'=> $messages,
    'stream'  => false,
    'options' => ['temperature' => 0.6, 'num_predict' => 2048],
]);
$ch = curl_init(OLLAMA_HOST . '/api/chat');
curl_setopt_array($ch, [
    CURLOPT_POST           => true,
    CURLOPT_POSTFIELDS     => $payload,
    CURLOPT_HTTPHEADER     => ['Content-Type: application/json'],
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT        => 120,
]);
$response = curl_exec($ch);
```

> **Explicación:** Se envía un POST JSON a la API de Ollama con el historial de chat. Si Ollama falla, se intenta OpenAI. Si ambos fallan, se usa un pattern matching local como último recurso.

### 2.5 Frontend SPA — Dark mode y Markdown

- JavaScript vanilla con objeto `state` global
- Parser Markdown→HTML (code blocks, bold, italic, headers, listas)
- Dark mode persistido en `localStorage`
- Exportación de conversaciones a TXT

````javascript
// assets/app.js — Markdown renderer
function renderMarkdown(text) {
  let html = escapeHtml(text);
  html = html.replace(
    /```(\w*)\n([\s\S]*?)```/g,
    '<pre><code class="lang-$1">$2</code></pre>',
  );
  html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
  html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/\n/g, "<br>");
  return html;
}
````

> **Explicación:** Función que convierte Markdown a HTML escapando primero el texto, luego aplicando regex para code blocks, inline code, negrita y saltos de línea.

---

## 3. Presentación del proyecto

- **Flujo usuario:** Registro → Login → Crear conversación sobre DB → Preguntar sobre personajes/sagas → Recibir respuesta IA experta → Exportar
- **Puntos fuertes:** IA especializada en Dragon Ball, fallback en cascada, transacciones MySQL, bcrypt, rate limiting, SPA con dark mode
- **Demo:** Abrir `http://localhost:8888/GitHub/Oráculo-Namek/`, registrar usuario, preguntar "¿Qué transformaciones tiene Goku?", cambiar modelo, exportar
- **Diseño:** Temática Dragon Ball, responsive, tema dual claro/oscuro

---

## 4. Conclusión

- **Competencias demostradas:** Persistencia MySQL, API REST PHP, autenticación bcrypt, integración IA
- **Patrón clave:** Singleton PDO → reutilización conexión
- **Seguridad:** bcrypt + prepared statements (anti SQL injection) + rate limiting + sesiones
- **Extensibilidad:** Cambiar modelo IA fácilmente, añadir endpoints, nuevas vistas
- **Valoración personal:** Proyecto completo fullstack PHP que integra IA con persistencia relacional
