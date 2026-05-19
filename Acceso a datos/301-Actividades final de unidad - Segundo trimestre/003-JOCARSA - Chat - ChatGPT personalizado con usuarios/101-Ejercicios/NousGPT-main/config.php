<?php

declare(strict_types=1);

/* ───────────────────────────── Base de datos ───────────────────────────── */
const DB_HOST   = 'localhost';
const DB_PORT   = '3306';
const DB_SOCKET = '/Applications/MAMP/tmp/mysql/mysql.sock';
const DB_NAME   = 'dragonball_chat';
const DB_USER   = 'dragonball_chat';
const DB_PASS   = 'dragonball_chat';

/* ───────────────────────────── Aplicación ──────────────────────────────── */
const APP_NAME              = 'Oráculo Namek';
const APP_VERSION           = '2.0.0';
const ASSISTANT_NAME        = 'ShenronIA';
const DEFAULT_SYSTEM_PROMPT = 'Eres un experto supremo en el universo Dragon Ball (DB, DBZ, DBGT, DBS, Dragon Ball Super: Super Hero). Conoces absolutamente todo sobre personajes, sagas, transformaciones, técnicas de combate, niveles de poder, planetas, razas, historia y cronología. Responde con entusiasmo, detalle y precisión usando formato Markdown. Incluye datos curiosos y detalles que solo un verdadero fan conocería.';

/* ───────────────────────────── Ollama (IA local) ──────────────────────── */
const OLLAMA_ENABLED         = true;
const OLLAMA_BASE_URL        = 'http://127.0.0.1:11434';
const OLLAMA_MODEL           = 'qwen2.5-coder:7b';
const OLLAMA_TIMEOUT_SECONDS = 90;

/* ───────────────────────────── OpenAI (fallback) ──────────────────────── */
const OPENAI_MODEL          = 'gpt-4o-mini';
const OPENAI_TIMEOUT        = 30;

/* ───────────────────────────── Rate limiting ──────────────────────────── */
const RATE_LIMIT_MESSAGES_PER_MINUTE = 12;
const RATE_LIMIT_WINDOW_SECONDS      = 60;

/* ───────────────────────────── Límites ─────────────────────────────────── */
const MAX_MESSAGE_LENGTH     = 5000;
const MAX_HISTORY_MESSAGES   = 30;
const MAX_CONVERSATION_TITLE = 120;
