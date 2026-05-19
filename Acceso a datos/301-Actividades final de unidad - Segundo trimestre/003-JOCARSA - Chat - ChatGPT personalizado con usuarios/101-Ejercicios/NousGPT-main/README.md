<p align="center">
  <img src="https://img.shields.io/badge/PHP-8.2-777BB4?style=for-the-badge&logo=php&logoColor=white" alt="PHP 8.2">
  <img src="https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL 8.0">
  <img src="https://img.shields.io/badge/JavaScript-ES2022-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/Ollama-Local_AI-000000?style=for-the-badge&logo=ollama&logoColor=white" alt="Ollama">
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI">
</p>

<h1 align="center">🐉 Oráculo Namek</h1>

<p align="center">
  <strong>Chat especializado en Dragon Ball con Inteligencia Artificial</strong><br>
  Experto virtual en DB/DBZ/DBGT/DBS · Historial persistente · Arquitectura en tres capas
</p>

<p align="center">
  <img src="https://img.shields.io/badge/versión-2.0.0-blue?style=flat-square" alt="v2.0.0">
  <img src="https://img.shields.io/badge/licencia-MIT-green?style=flat-square" alt="MIT">
  <img src="https://img.shields.io/badge/estado-producción-brightgreen?style=flat-square" alt="Producción">
</p>

---

## Descripción

**Oráculo Namek** es una aplicación web full-stack que permite a fans de Dragon Ball interactuar con modelos de IA especializados en el universo creado por Akira Toriyama. El sistema gestiona autenticación de usuarios, conversaciones independientes por usuario, y persistencia del historial completo de consultas sobre personajes, sagas, técnicas y todo lo relacionado con Dragon Ball.

Diseñado como proyecto de referencia para **Acceso a datos** (DAM2), demuestra dominio de PHP moderno, MySQL, APIs REST, autenticación segura y una interfaz JavaScript reactiva sin dependencias externas.

---

## Características principales

| Módulo             | Funcionalidad                                                                                                    |
| ------------------ | ---------------------------------------------------------------------------------------------------------------- |
| **Autenticación**  | Registro / login con `password_hash()`, sesiones PHP seguras, cookie cleanup en logout                           |
| **Conversaciones** | CRUD completo, renombrado, archivado, mensaje de bienvenida automático                                           |
| **Chat con IA**    | Orquestador de 3 proveedores: Ollama → OpenAI → Fallback local inteligente                                       |
| **Markdown**       | Renderizado en tiempo real de código, negritas, cursivas, listas y cabeceras                                     |
| **Modo oscuro**    | Tema claro/oscuro con `localStorage`, CSS Custom Properties y transiciones suaves                                |
| **Exportación**    | Descarga la conversación completa como archivo `.txt`                                                            |
| **Rate limiting**  | Control de mensajes por minuto para prevenir abuso                                                               |
| **Métricas**       | Estimación de tokens, tiempo de respuesta del modelo, contador de mensajes                                       |
| **UX moderna**     | Indicador de escritura, auto-resize del textarea, búsqueda de conversaciones, copiar código, toast notifications |
| **Responsive**     | Diseño adaptativo con breakpoints a 960px y 480px                                                                |

---

## Stack tecnológico

```
┌─ Frontend ──────────────────────────────────────┐
│  HTML5 semántico · CSS3 Custom Properties       │
│  JavaScript ES2022 · Google Fonts (Inter)       │
│  Markdown renderer propio · Sin dependencias    │
├─ Backend ───────────────────────────────────────┤
│  PHP 8.2 strict_types · PDO MySQL               │
│  API REST JSON · Sesiones server-side            │
│  cURL para Ollama y OpenAI                       │
├─ Base de datos ─────────────────────────────────┤
│  MySQL 8.0 · InnoDB · utf8mb4                   │
│  3 tablas con FK + CASCADE                       │
│  Índices compuestos para rendimiento             │
├─ IA ────────────────────────────────────────────┤
│  Ollama (local) → OpenAI (cloud) → Fallback     │
│  Selección dinámica de modelos                   │
│  System prompt personalizable por conversación   │
└─────────────────────────────────────────────────┘
```

---

## Arquitectura

```
Cliente (JavaScript SPA)
    │
    ├── api/auth.php          → Registro, login, logout, sesión
    ├── api/conversations.php → CRUD de conversaciones
    ├── api/messages.php      → Envío/recepción de mensajes + IA
    └── api/models.php        → Listado y selección de modelos Ollama
         │
         ├── lib/assistant.php → Orquestador IA (Ollama → OpenAI → Local)
         ├── api/common.php    → Utilidades compartidas (auth, JSON, limpieza)
         ├── db.php            → Conexión PDO + auto-migración de esquema
         └── config.php        → Constantes centralizadas
              │
              └── MySQL (dragonball_chat)
                   ├── usuarios
                   ├── conversaciones
                   └── mensajes
```

---

## Modelo de datos

```sql
usuarios (id, username, email, password_hash, created_at, last_login)
    │
    └── conversaciones (id, usuario_id FK, titulo, system_prompt, archivada, created_at, updated_at)
            │
            └── mensajes (id, conversacion_id FK, role, contenido, tokens_estimados, created_at)
```

- **Integridad referencial** con `ON DELETE CASCADE`
- **Índices compuestos** para consultas frecuentes
- **Auto-inicialización**: el esquema se crea automáticamente al primer acceso

---

## Instalación

### Requisitos previos

- PHP ≥ 8.0
- MySQL ≥ 5.7 / MariaDB ≥ 10.3
- Servidor web (Apache/Nginx) o MAMP/XAMPP
- [Ollama](https://ollama.ai) (opcional, para IA local)

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/luisrocedev/NousGPT.git
cd NousGPT

# 2. Configurar la base de datos
#    Editar config.php con tus credenciales MySQL
#    (El esquema se auto-crea al primer acceso)

# 3. (Opcional) Instalar un modelo local con Ollama
ollama pull qwen2.5-coder:7b

# 4. (Opcional) Configurar OpenAI como fallback
export OPENAI_API_KEY="sk-..."

# 5. Abrir en el navegador
#    http://localhost:8888/NousGPT  (MAMP)
#    http://localhost/NousGPT       (Apache)
```

### Configuración

Todas las constantes se centralizan en [`config.php`](config.php):

| Constante                        | Descripción                     | Valor por defecto        |
| -------------------------------- | ------------------------------- | ------------------------ |
| `OLLAMA_BASE_URL`                | URL del servidor Ollama         | `http://127.0.0.1:11434` |
| `OLLAMA_MODEL`                   | Modelo por defecto              | `qwen2.5-coder:7b`       |
| `OPENAI_MODEL`                   | Modelo de fallback en la nube   | `gpt-4o-mini`            |
| `RATE_LIMIT_MESSAGES_PER_MINUTE` | Límite de mensajes/min          | `12`                     |
| `MAX_MESSAGE_LENGTH`             | Caracteres máximos por mensaje  | `5000`                   |
| `MAX_HISTORY_MESSAGES`           | Mensajes de contexto para la IA | `30`                     |

---

## API REST

### Autenticación — `api/auth.php`

| Método | Acción             | Descripción                              |
| ------ | ------------------ | ---------------------------------------- |
| `GET`  | `?action=me`       | Estado de la sesión actual               |
| `POST` | `action: register` | Crear cuenta (username, email, password) |
| `POST` | `action: login`    | Iniciar sesión (email, password)         |
| `POST` | `action: logout`   | Cerrar sesión                            |

### Conversaciones — `api/conversations.php`

| Método | Acción           | Descripción                       |
| ------ | ---------------- | --------------------------------- |
| `GET`  | —                | Listar conversaciones del usuario |
| `POST` | `action: create` | Crear nueva conversación          |
| `POST` | `action: rename` | Renombrar conversación            |
| `POST` | `action: delete` | Eliminar conversación             |

### Mensajes — `api/messages.php`

| Método | Parámetros                        | Descripción                           |
| ------ | --------------------------------- | ------------------------------------- |
| `GET`  | `conversation_id`                 | Obtener mensajes de una conversación  |
| `POST` | `conversation_id, message, model` | Enviar mensaje y recibir respuesta IA |

### Modelos — `api/models.php`

| Método | Descripción                          |
| ------ | ------------------------------------ |
| `GET`  | Listar modelos disponibles en Ollama |
| `POST` | Seleccionar modelo activo            |

---

## Estructura del proyecto

```
NousGPT/
├── index.php              # SPA entry point (HTML)
├── config.php             # Constantes centralizadas
├── db.php                 # Conexión PDO + auto-migración
├── api/
│   ├── common.php         # Utilidades compartidas
│   ├── auth.php           # Autenticación
│   ├── conversations.php  # CRUD conversaciones
│   ├── messages.php       # Mensajes + orquestación IA
│   └── models.php         # Modelos Ollama
├── lib/
│   └── assistant.php      # Proveedores IA + fallback
├── assets/
│   ├── app.js             # Cliente JavaScript (651 líneas)
│   └── styles.css         # Sistema de diseño CSS
└── db/
    └── schema.sql         # DDL de referencia
```

---

## Seguridad

- **Password hashing** con `PASSWORD_DEFAULT` (bcrypt)
- **Prepared statements** en todas las consultas SQL
- **Sesiones server-side** con limpieza de cookies en logout
- **Rate limiting** por usuario para prevenir abuso
- **Validación y saneamiento** de entrada con `clean_text()` y `filter_var()`
- **Aislamiento de datos**: cada usuario solo accede a sus conversaciones
- **Headers JSON-only**: `Content-Type: application/json` en todas las respuestas API
- **Errores ocultados** en producción (`display_errors = 0`)

---

## Autor

**Luis Rodriguez Cedeño**  
DAM2 — Acceso a datos  
📧 [luisrocedev](https://github.com/luisrocedev)

---

<p align="center">
  <sub>Desarrollado con 🧠 y mucho ☕ | NousGPT v2.0.0</sub>
</p>
