# Chat Especializado Dragon Ball - Oráculo Namek

**DNI:** 53945291X  
**Curso:** DAM2 — Acceso a datos  
**Actividad:** 003-Chat especializado en universo Dragon Ball  
**Tecnologías:** PHP 8.2 · MySQL 8.0 · JavaScript · Ollama · OpenAI API  
**Fecha:** 10 de febrero de 2026

---

## 1. Introducción breve y contextualización (25%)

### Concepto general

Un chat especializado en Dragon Ball es una aplicación web que permite a múltiples usuarios (fans del anime/manga) interactuar con modelos de inteligencia artificial especializados en el universo Dragon Ball. El sistema gestiona autenticación de usuarios, conversaciones independientes por usuario, y persistencia del historial completo de mensajes en base de datos relacional.

### Contexto y utilidad

Los sistemas de chat con IA especializada son útiles para comunidades de fans porque:

- **Conocimiento profundo:** Cada usuario puede consultar sobre personajes, sagas, técnicas, transformaciones y cronología sin límites
- **Historial persistente:** Los fans mantienen un registro completo de todas sus consultas sobre el universo DB
- **Privacidad:** La información de cada usuario está aislada y protegida  
- **Flexibilidad:** Permite usar diferentes modelos de IA con distintos niveles de conocimiento sobre Dragon Ball

Este proyecto integra conocimientos de acceso a datos (MySQL), autenticación segura (hashing de contraseñas), arquitectura cliente-servidor (PHP + JavaScript), y consumo de APIs externas (Ollama/OpenAI).

---

## 2. Desarrollo detallado y preciso (25%)

### Arquitectura del sistema

El sistema utiliza una arquitectura de tres capas:

**Capa de presentación (Frontend):**

- Interfaz HTML/CSS con diseño responsive y sistema de temas (claro/oscuro)
- JavaScript para comunicación asíncrona con el backend mediante `fetch`
- Renderizado de Markdown en las respuestas del asistente
- Gestión de estado centralizada en el cliente

**Capa de lógica de negocio (Backend):**

- PHP 8.2 con `declare(strict_types=1)` para procesamiento de peticiones
- Autenticación con sesiones PHP
- API REST con cuerpo JSON (`php://input`)
- Integración con tres proveedores de IA en cascada (Ollama → OpenAI → Local)

**Capa de datos:**

- MySQL 8.0 para persistencia
- Tres tablas principales: usuarios, conversaciones, mensajes
- Auto-inicialización del esquema al primer acceso

### Modelo de base de datos

```sql
-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME NULL
) ENGINE=InnoDB;

-- Tabla de conversaciones
CREATE TABLE IF NOT EXISTS conversaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    titulo VARCHAR(120) NOT NULL,
    system_prompt TEXT NOT NULL,
    archivada TINYINT(1) NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_conversaciones_usuarios
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- Tabla de mensajes
CREATE TABLE IF NOT EXISTS mensajes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conversacion_id INT NOT NULL,
    role ENUM('user', 'assistant', 'system') NOT NULL,
    contenido MEDIUMTEXT NOT NULL,
    tokens_estimados INT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_mensajes_conversaciones
        FOREIGN KEY (conversacion_id) REFERENCES conversaciones(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- Índices para rendimiento
CREATE INDEX idx_conversaciones_usuario ON conversaciones(usuario_id, updated_at);
CREATE INDEX idx_mensajes_conversacion ON mensajes(conversacion_id, created_at);
```

### Conexión a base de datos con PDO

La conexión se gestiona mediante una función con patrón `static` que evita crear conexiones duplicadas. Además, `init_database()` auto-crea el esquema si no existe:

```php
<?php
// db.php — Conexión PDO y auto-migración
declare(strict_types=1);
require_once __DIR__ . '/config.php';

function get_pdo(): PDO
{
    static $pdo = null;

    if ($pdo instanceof PDO) {
        return $pdo;
    }

    $dsn = sprintf(
        'mysql:host=%s;port=%s;charset=utf8mb4;unix_socket=%s',
        DB_HOST, DB_PORT, DB_SOCKET
    );

    $pdo = new PDO($dsn, DB_USER, DB_PASS, [
        PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ]);

    return $pdo;
}

function init_database(PDO $pdo): void
{
    $pdo->exec('CREATE DATABASE IF NOT EXISTS `dragonball_chat`
                CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci');
    $pdo->exec('USE `dragonball_chat`');

    // CREATE TABLE IF NOT EXISTS para cada tabla...
    // Además, se crean índices compuestos verificando su existencia previa
}
```

### Utilidades compartidas (api/common.php)

Todas las rutas API comparten un conjunto de funciones comunes para parsing JSON, autenticación y saneamiento de datos:

```php
<?php
// api/common.php — Funciones compartidas
declare(strict_types=1);

ini_set('display_errors', '0');
error_reporting(0);
session_start();

require_once __DIR__ . '/../db.php';
require_once __DIR__ . '/../config.php';

header('Content-Type: application/json; charset=utf-8');

function json_response(array $data, int $statusCode = 200): void
{
    http_response_code($statusCode);
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit;
}

function parse_json_body(): array
{
    $raw = file_get_contents('php://input');
    if (!$raw) { return []; }
    $decoded = json_decode($raw, true);
    return is_array($decoded) ? $decoded : [];
}

function get_authenticated_user_id(): ?int
{
    return isset($_SESSION['user_id']) ? (int) $_SESSION['user_id'] : null;
}

function require_auth_user_id(): int
{
    $userId = get_authenticated_user_id();
    if ($userId === null) {
        json_response(['ok' => false, 'error' => 'No autenticado.'], 401);
    }
    return $userId;
}

function clean_text(string $value, int $maxLength): string
{
    $value = trim($value);
    if (mb_strlen($value) > $maxLength) {
        $value = mb_substr($value, 0, $maxLength);
    }
    return $value;
}
```

### Sistema de autenticación

**Registro de usuarios:**

```php
<?php
// api/auth.php — Registro
declare(strict_types=1);
require_once __DIR__ . '/common.php';

$pdo = get_pdo();
init_database($pdo);

$input  = parse_json_body();
$action = $input['action'] ?? '';

if ($action === 'register') {
    $username = clean_text((string) ($input['username'] ?? ''), 50);
    $email    = clean_text((string) ($input['email'] ?? ''), 120);
    $password = (string) ($input['password'] ?? '');

    if ($username === '' || $email === '' || $password === '') {
        json_response(['ok' => false, 'error' => 'Todos los campos son obligatorios.'], 400);
    }

    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        json_response(['ok' => false, 'error' => 'Email no válido.'], 400);
    }

    if (mb_strlen($password) < 6) {
        json_response(['ok' => false, 'error' => 'La contraseña debe tener al menos 6 caracteres.'], 400);
    }

    $hash = password_hash($password, PASSWORD_DEFAULT);

    try {
        $stmt = $pdo->prepare('INSERT INTO usuarios (username, email, password_hash) VALUES (?, ?, ?)');
        $stmt->execute([$username, $email, $hash]);
        $userId = (int) $pdo->lastInsertId();

        $_SESSION['user_id'] = $userId;

        json_response([
            'ok'   => true,
            'message' => 'Cuenta creada correctamente.',
            'user' => ['id' => $userId, 'username' => $username, 'email' => $email],
        ]);
    } catch (PDOException $exception) {
        $error = 'No se pudo registrar el usuario.';
        if ((int) $exception->getCode() === 23000) {
            $error = 'El usuario o el email ya existen.';
        }
        json_response(['ok' => false, 'error' => $error], 409);
    }
}
```

**Inicio de sesión:**

```php
<?php
// api/auth.php — Login
if ($action === 'login') {
    $email    = clean_text((string) ($input['email'] ?? ''), 120);
    $password = (string) ($input['password'] ?? '');

    if ($email === '' || $password === '') {
        json_response(['ok' => false, 'error' => 'Email y contraseña son obligatorios.'], 400);
    }

    $stmt = $pdo->prepare('SELECT id, username, email, password_hash FROM usuarios WHERE email = ?');
    $stmt->execute([$email]);
    $user = $stmt->fetch();

    if (!$user || !password_verify($password, $user['password_hash'])) {
        json_response(['ok' => false, 'error' => 'Credenciales no válidas.'], 401);
    }

    $_SESSION['user_id'] = (int) $user['id'];

    $upd = $pdo->prepare('UPDATE usuarios SET last_login = NOW() WHERE id = ?');
    $upd->execute([(int) $user['id']]);

    json_response([
        'ok'   => true,
        'message' => 'Login correcto.',
        'user' => [
            'id' => (int) $user['id'],
            'username' => $user['username'],
            'email' => $user['email'],
        ],
    ]);
}
```

### Gestión de conversaciones

```php
<?php
// api/conversations.php
declare(strict_types=1);
require_once __DIR__ . '/common.php';

$pdo    = get_pdo();
init_database($pdo);
$userId = require_auth_user_id();
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';

if ($method === 'GET') {
    $stmt = $pdo->prepare(
        'SELECT c.id, c.titulo, c.system_prompt, c.created_at, c.updated_at,
                (SELECT contenido FROM mensajes m WHERE m.conversacion_id = c.id ORDER BY m.id DESC LIMIT 1)
                    AS ultimo_mensaje,
                (SELECT COUNT(*) FROM mensajes m2 WHERE m2.conversacion_id = c.id)
                    AS total_mensajes
         FROM conversaciones c
         WHERE c.usuario_id = ? AND c.archivada = 0
         ORDER BY c.updated_at DESC'
    );
    $stmt->execute([$userId]);
    $rows = $stmt->fetchAll();

    json_response(['ok' => true, 'conversations' => $rows]);
}

if ($method === 'POST') {
    $input  = parse_json_body();
    $action = (string) ($input['action'] ?? '');

    if ($action === 'create') {
        $title        = clean_text((string) ($input['title'] ?? ''), 120);
        $systemPrompt = clean_text((string) ($input['system_prompt'] ?? DEFAULT_SYSTEM_PROMPT), 1000);

        if ($title === '') { $title = 'Conversación sin título'; }
        if ($systemPrompt === '') { $systemPrompt = DEFAULT_SYSTEM_PROMPT; }

        $stmt = $pdo->prepare('INSERT INTO conversaciones (usuario_id, titulo, system_prompt) VALUES (?, ?, ?)');
        $stmt->execute([$userId, $title, $systemPrompt]);
        $conversationId = (int) $pdo->lastInsertId();

        // Mensaje de bienvenida automático
        $insertWelcome = $pdo->prepare('INSERT INTO mensajes (conversacion_id, role, contenido) VALUES (?, ?, ?)');
        $insertWelcome->execute([$conversationId, 'assistant', '¡Hola! Soy ' . ASSISTANT_NAME . '. Estoy listo para ayudarte.']);

        json_response([
            'ok'           => true,
            'conversation' => ['id' => $conversationId, 'titulo' => $title, 'system_prompt' => $systemPrompt],
        ]);
    }

    if ($action === 'delete') {
        $conversationId = (int) ($input['conversation_id'] ?? 0);
        $stmt = $pdo->prepare('DELETE FROM conversaciones WHERE id = ? AND usuario_id = ?');
        $stmt->execute([$conversationId, $userId]);

        json_response(['ok' => true, 'message' => 'Conversación eliminada.']);
    }
}
```

### Integración con IA (Orquestador de 3 proveedores)

El sistema intenta generar respuestas con Ollama primero; si falla, prueba OpenAI; y como último recurso, usa un generador local inteligente con respuestas en Markdown:

```php
<?php
// lib/assistant.php — Orquestador IA
declare(strict_types=1);
require_once __DIR__ . '/../config.php';

function build_chat_messages(string $systemPrompt, string $message, array $history): array
{
    $messages = [['role' => 'system', 'content' => $systemPrompt]];

    $recentHistory = array_slice($history, -(MAX_HISTORY_MESSAGES));
    foreach ($recentHistory as $item) {
        $role    = $item['role'] ?? 'user';
        $content = trim((string) ($item['contenido'] ?? ''));
        if ($content !== '' && in_array($role, ['user', 'assistant', 'system'], true)) {
            $messages[] = ['role' => $role, 'content' => $content];
        }
    }

    $messages[] = ['role' => 'user', 'content' => $message];
    return $messages;
}

function estimate_tokens(string $text): int
{
    return (int) ceil(mb_strlen($text) / 3.5);
}

function generate_ollama_reply(string $systemPrompt, string $message, array $history, ?string $model = null): ?string
{
    if (!OLLAMA_ENABLED) { return null; }

    $endpoint = rtrim(OLLAMA_BASE_URL, '/') . '/api/chat';
    $messages = build_chat_messages($systemPrompt, $message, $history);
    $resolved = resolve_ollama_model($model);

    $payload = [
        'model'    => $resolved,
        'messages' => $messages,
        'stream'   => false,
        'options'  => ['temperature' => 0.6, 'num_predict' => 2048],
    ];

    $ch = curl_init($endpoint);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST           => true,
        CURLOPT_HTTPHEADER     => ['Content-Type: application/json'],
        CURLOPT_POSTFIELDS     => json_encode($payload, JSON_UNESCAPED_UNICODE),
        CURLOPT_TIMEOUT        => OLLAMA_TIMEOUT_SECONDS,
        CURLOPT_CONNECTTIMEOUT => 10,
    ]);

    $result   = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if (!is_string($result) || $httpCode < 200 || $httpCode >= 300) { return null; }

    $decoded = json_decode($result, true);
    $content = $decoded['message']['content'] ?? null;
    return is_string($content) && trim($content) !== '' ? trim($content) : null;
}

// Orquestador principal: Ollama → OpenAI → Local
function generate_assistant_reply(string $systemPrompt, string $message, array $history, ?string $model = null): string
{
    $ollama = generate_ollama_reply($systemPrompt, $message, $history, $model);
    if ($ollama !== null && trim($ollama) !== '') { return trim($ollama); }

    $openAI = generate_openai_reply($systemPrompt, $message, $history);
    if ($openAI !== null && trim($openAI) !== '') { return trim($openAI); }

    return generate_local_reply($systemPrompt, $message, $history);
}
```

### API de mensajes con rate limiting y métricas

```php
<?php
// api/messages.php
declare(strict_types=1);
require_once __DIR__ . '/common.php';
require_once __DIR__ . '/../lib/assistant.php';

$pdo    = get_pdo();
init_database($pdo);
$userId = require_auth_user_id();

function check_rate_limit(PDO $pdo, int $userId): bool
{
    $stmt = $pdo->prepare(
        'SELECT COUNT(*) AS total FROM mensajes m
         JOIN conversaciones c ON m.conversacion_id = c.id
         WHERE c.usuario_id = ? AND m.role = ? AND m.created_at >= DATE_SUB(NOW(), INTERVAL ? SECOND)'
    );
    $stmt->execute([$userId, 'user', RATE_LIMIT_WINDOW_SECONDS]);
    $count = (int) ($stmt->fetch()['total'] ?? 0);
    return $count < RATE_LIMIT_MESSAGES_PER_MINUTE;
}

// POST: enviar mensaje
$input          = parse_json_body();
$conversationId = (int) ($input['conversation_id'] ?? 0);
$message        = clean_text((string) ($input['message'] ?? ''), MAX_MESSAGE_LENGTH);
$selectedModel  = clean_text((string) ($input['model'] ?? ''), 100);

// Verificar rate limit
if (!check_rate_limit($pdo, $userId)) {
    json_response(['ok' => false, 'error' => 'Has enviado demasiados mensajes. Espera un momento.'], 429);
}

// Cargar historial y generar respuesta de IA
$stmtHistory = $pdo->prepare('SELECT role, contenido FROM mensajes WHERE conversacion_id = ? ORDER BY id ASC');
$stmtHistory->execute([$conversationId]);
$history = $stmtHistory->fetchAll();

$startTime      = microtime(true);
$assistantReply = generate_assistant_reply((string) $conversation['system_prompt'], $message, $history, $effectiveModel);
$responseTimeMs = (int) round((microtime(true) - $startTime) * 1000);

$userTokens      = estimate_tokens($message);
$assistantTokens = estimate_tokens($assistantReply);

// Guardar ambos mensajes en transacción
$pdo->beginTransaction();
try {
    $insertUser = $pdo->prepare('INSERT INTO mensajes (conversacion_id, role, contenido, tokens_estimados) VALUES (?, ?, ?, ?)');
    $insertUser->execute([$conversationId, 'user', $message, $userTokens]);

    $insertAssistant = $pdo->prepare('INSERT INTO mensajes (conversacion_id, role, contenido, tokens_estimados) VALUES (?, ?, ?, ?)');
    $insertAssistant->execute([$conversationId, 'assistant', $assistantReply, $assistantTokens]);

    $pdo->commit();
} catch (Throwable $error) {
    if ($pdo->inTransaction()) { $pdo->rollBack(); }
    json_response(['ok' => false, 'error' => 'No se pudo guardar el mensaje.'], 500);
}

json_response([
    'ok'              => true,
    'assistant_reply' => $assistantReply,
    'model'           => $effectiveModel,
    'response_time_ms'=> $responseTimeMs,
    'tokens'          => ['user' => $userTokens, 'assistant' => $assistantTokens],
]);
```

### Terminología técnica

- **Session:** Mecanismo de PHP para mantener estado entre peticiones HTTP
- **Password hashing:** Transformación irreversible de contraseña para almacenamiento seguro con `PASSWORD_DEFAULT`
- **PDO (PHP Data Objects):** Interfaz de acceso a bases de datos con soporte para prepared statements
- **ON DELETE CASCADE:** Borrado automático de registros relacionados cuando se elimina el padre
- **Rate limiting:** Técnica para limitar el número de peticiones por usuario en un intervalo de tiempo
- **Fetch API:** Interfaz JavaScript moderna para hacer peticiones HTTP asíncronas basadas en promesas
- **Fallback:** Mecanismo de respaldo que decide automáticamente qué proveedor de IA usar cuando uno falla

---

## 3. Aplicación práctica (25%)

### Flujo completo de uso

```javascript
// assets/app.js — Cliente JavaScript con estado centralizado

"use strict";

const state = {
  user: null,
  conversations: [],
  activeConversationId: null,
  models: [],
  selectedModel: "",
  sending: false,
  searchQuery: "",
};

// Capa de comunicación con la API
async function api(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const data = await response.json();
  if (!response.ok || data.ok === false) {
    throw new Error(data.error || `Error ${response.status}`);
  }
  return data;
}

// Cargar sesión al iniciar la aplicación
async function loadSession() {
  try {
    const data = await api("api/auth.php?action=me");
    if (data.authenticated) {
      state.user = data.user;
      renderAuth();
      await Promise.all([loadModels(), loadConversations()]);
    }
  } catch (err) {
    // No autenticado — se muestra la vista de login
  }
}

// Cargar conversaciones del usuario
async function loadConversations() {
  try {
    const data = await api("api/conversations.php");
    state.conversations = data.conversations || [];
  } catch {
    state.conversations = [];
  }
  renderConversations();

  if (state.activeConversationId) {
    await loadMessages(state.activeConversationId);
  }
}

// Cargar mensajes de una conversación específica
async function loadMessages(conversationId) {
  try {
    const data = await api(
      `api/messages.php?conversation_id=${conversationId}`,
    );
    state.activeConversationId = Number(conversationId);
    el.conversationTitle.textContent = data.conversation.titulo;
    renderMessages(data.messages || []);
  } catch (err) {
    showToast(err.message);
  }
}
```

### Renderizado de Markdown y mensajes

Las respuestas del asistente se renderizan con un parser de Markdown propio que soporta bloques de código, negritas, cursivas, cabeceras y listas:

````javascript
// Renderizador de Markdown ligero (sin dependencias)
function renderMarkdown(text) {
  if (!text) return "";
  let html = escapeHtml(text);

  // Bloques de código: ```lang\n...\n```
  html = html.replace(/```(\w*)\n([\s\S]*?)```/g, (_match, lang, code) => {
    const label = lang || "código";
    const id = "cb_" + Math.random().toString(36).slice(2, 8);
    return `<div class="code-block">
            <div class="code-block-header">
                <span>${escapeHtml(label)}</span>
                <button class="code-block-copy" onclick="copyCodeBlock(this, '${id}')">Copiar</button>
            </div>
            <code class="code-block-code" id="${id}">${code}</code>
        </div>`;
  });

  // Código en línea, negritas, cursivas, cabeceras, listas
  html = html.replace(/`([^`\n]+)`/g, "<code>$1</code>");
  html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/^### (.+)$/gm, "<h3>$1</h3>");
  html = html.replace(/^## (.+)$/gm, "<h2>$1</h2>");
  html = html.replace(/^- (.+)$/gm, "<li>$1</li>");
  html = html.replace(/\n\n/g, "</p><p>");

  return html;
}

// Renderizado de mensajes con distinción visual usuario/asistente
function renderMessages(messages = []) {
  el.messages.innerHTML = messages
    .map((msg) => {
      const isAssistant = msg.role === "assistant";
      const roleLabel = isAssistant ? "MentorIA" : "Tú";
      const bodyContent = isAssistant
        ? renderMarkdown(msg.contenido)
        : escapeHtml(msg.contenido);
      const timeStr = msg.created_at ? timeAgo(msg.created_at) : "";

      return `
            <article class="msg ${msg.role}">
                <div class="msg-header">${roleLabel}</div>
                <div class="msg-body">${bodyContent}</div>
                <div class="msg-footer"><span>${timeStr}</span></div>
            </article>`;
    })
    .join("");

  requestAnimationFrame(() => {
    el.messages.scrollTop = el.messages.scrollHeight;
  });
}
````

### Envío de mensajes con indicador de escritura

```javascript
// Enviar mensaje y recibir respuesta de IA
el.messageForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (state.sending || !state.activeConversationId) return;

  const message = el.messageInput.value.trim();
  if (!message) return;

  try {
    setSendingState(true); // Muestra indicador de escritura ⋯
    const data = await api("api/messages.php", {
      method: "POST",
      body: JSON.stringify({
        conversation_id: state.activeConversationId,
        message,
        model: state.selectedModel,
      }),
    });

    // Actualizar modelo si cambió
    if (data.model) {
      state.selectedModel = data.model;
      renderModelPicker();
    }

    el.messageInput.value = "";
    el.charCount.textContent = `0 / ${el.messageInput.maxLength}`;

    await loadMessages(state.activeConversationId);
    await loadConversations();
  } catch (err) {
    showToast(err.message);
  } finally {
    setSendingState(false); // Oculta indicador de escritura
    el.messageInput.focus();
  }
});
```

### Tema oscuro/claro con persistencia

```javascript
// Sistema de temas con CSS Custom Properties
function getStoredTheme() {
  return localStorage.getItem("nousgpt_theme") || "light";
}

function setTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("nousgpt_theme", theme);
}

function toggleTheme() {
  const current =
    document.documentElement.getAttribute("data-theme") || "light";
  setTheme(current === "light" ? "dark" : "light");
}

// Se aplica al cargar la página para evitar flash
setTheme(getStoredTheme());
```

### Errores comunes y soluciones

**Error 1:** No verificar autenticación en cada endpoint.

```php
// Incorrecto - No verifica sesión
$usuario_id = $_GET['usuario_id'];

// Correcto - Usa función reutilizable que aborta con 401
$userId = require_auth_user_id();
```

**Error 2:** Almacenar contraseñas en texto plano.

```php
// Incorrecto
$stmt->execute([$username, $password]);

// Correcto - PASSWORD_DEFAULT usa bcrypt
$hash = password_hash($password, PASSWORD_DEFAULT);
$stmt->execute([$username, $hash]);
```

**Error 3:** No usar prepared statements.

```php
// Incorrecto - Vulnerable a SQL injection
$query = "SELECT * FROM usuarios WHERE email = '$email'";

// Correcto - Sentencias preparadas con parámetros posicionales
$stmt = $pdo->prepare('SELECT * FROM usuarios WHERE email = ?');
$stmt->execute([$email]);
```

**Error 4:** No usar transacciones para operaciones múltiples.

```php
// Incorrecto - Si falla el segundo INSERT, queda inconsistente
$pdo->exec("INSERT INTO mensajes ...");
$pdo->exec("INSERT INTO mensajes ...");

// Correcto - Transacción con rollback
$pdo->beginTransaction();
try {
    $pdo->prepare('INSERT INTO mensajes ...')->execute([...]);
    $pdo->prepare('INSERT INTO mensajes ...')->execute([...]);
    $pdo->commit();
} catch (Throwable $e) {
    $pdo->rollBack();
}
```

---

## 4. Conclusión breve (25%)

### Resumen de puntos clave

Este proyecto de chat académico demuestra:

1. **Autenticación segura:** Hashing de contraseñas con `password_hash(PASSWORD_DEFAULT)` y gestión de sesiones PHP con limpieza completa en logout
2. **Arquitectura multicapa:** Separación clara entre frontend (JavaScript SPA), backend (API REST PHP) y datos (MySQL), con utilidades compartidas en `common.php`
3. **Integración con IA:** Orquestador de tres proveedores en cascada (Ollama → OpenAI → Local) con resolución dinámica de modelos y estimación de tokens
4. **Base de datos relacional:** Modelo normalizado con integridad referencial mediante claves foráneas y `ON DELETE CASCADE`, índices compuestos para rendimiento, y auto-inicialización del esquema
5. **Rate limiting:** Control de abuso limitando mensajes por usuario en ventanas de tiempo configurables
6. **UX moderna:** Modo oscuro con persistencia, renderizado de Markdown, indicador de escritura, exportación de conversaciones y búsqueda en el sidebar

### Enlace con contenidos de la unidad

Este proyecto integra conceptos clave del módulo:

- **Manejo de conectores (Unidad 2):** PDO con MySQL, prepared statements, transacciones con `beginTransaction() / commit() / rollBack()`
- **Bases de datos relacionales (Unidad 4):** Diseño normalizado con tres tablas relacionadas, claves foráneas, índices compuestos y tipo `MEDIUMTEXT` para mensajes largos
- **Componentes de acceso a datos (Unidad 6):** API REST JSON con PHP para operaciones CRUD, funciones reutilizables (`json_response`, `require_auth_user_id`, `clean_text`)
- **Seguridad:** Validación de entrada con `filter_var()` y `clean_text()`, hashing de contraseñas, control de acceso basado en sesiones, rate limiting, errores ocultos en producción

La arquitectura de este sistema es escalable y puede aplicarse a otros proyectos que requieran autenticación de usuarios, gestión de contenido personalizado y consumo de servicios externos. El uso de prepared statements y validación de sesiones en cada endpoint garantiza la seguridad del sistema frente a ataques comunes como SQL injection y acceso no autorizado. La auto-inicialización de la base de datos y la configuración centralizada en constantes facilita el despliegue y mantenimiento del proyecto.
