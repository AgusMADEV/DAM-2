INSERT INTO `conversaciones`
(`Identificador`, `usuario_nombre`, `modelo_nombre`, `fecha`, `descripcion`)
VALUES
(2,  1, 1, '2026-01-02 09:15:00', 'Consulta sobre automatización de tareas en Python'),
(3,  1, 2, '2026-01-02 10:42:11', 'Generación de ideas para un SaaS educativo'),
(4,  1, 6, '2026-01-03 08:30:45', 'Corrección de errores en script Bash con ffmpeg'),
(5,  1, 3, '2026-01-03 12:05:33', 'Análisis técnico sobre modelos de lenguaje'),
(6,  1, 7, '2026-01-03 18:22:10', 'Redacción de textos comerciales para Jocarsa'),
(7,  1, 2, '2026-01-04 09:01:55', 'Explicación didáctica de SQL con ejemplos'),
(8,  1, 6, '2026-01-04 11:47:20', 'Optimización de código CUDA para simulación 3D'),
(9,  1, 1, '2026-01-04 16:10:02', 'Creación de ejercicios prácticos de Python'),
(10, 1, 4, '2026-01-05 08:55:40', 'Consulta rápida sobre sintaxis de JavaScript'),
(11, 1, 5, '2026-01-05 13:18:27', 'Ideas para monetizar contenido educativo'),
(12, 1, 6, '2026-01-05 19:44:09', 'Depuración de aplicación PHP con SQLite'),
(13, 1, 7, '2026-01-06 09:07:31', 'Generación de documentación técnica'),
(14, 1, 3, '2026-01-06 12:56:48', 'Evaluación de arquitectura IA local'),
(15, 1, 2, '2026-01-06 17:20:14', 'Creación de dataset JSONL para entrenamiento'),
(16, 1, 6, '2026-01-07 08:11:03', 'Script para backups automáticos de Moodle'),
(17, 1, 1, '2026-01-07 10:39:58', 'Redacción de introducción para libro técnico'),
(18, 1, 7, '2026-01-07 14:02:41', 'Revisión de UX para plataforma educativa');



CREATE TABLE IF NOT EXISTS `mensajes_conversacion` (
  `Identificador` INT NOT NULL AUTO_INCREMENT,
  `conversacion_id` INT NOT NULL,
  `datetime` DATETIME NOT NULL,
  `es_usuario` TINYINT(1) NOT NULL,
  `mensaje_md` LONGTEXT NOT NULL,
  PRIMARY KEY (`Identificador`),
  KEY `idx_conversacion_id` (`conversacion_id`),
  KEY `idx_datetime` (`datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `mensajes_conversacion`
(`conversacion_id`, `datetime`, `es_usuario`, `mensaje_md`)
VALUES
-- Conversación 2 (2026-01-02 09:15:00) - Automatización Python
(2, '2026-01-02 09:15:05', 1, 'Quiero automatizar tareas repetitivas en Python. ¿Qué estructura me recomiendas para scripts que se ejecutan por cron?'),
(2, '2026-01-02 09:15:40', 0, 'Una estructura simple y mantenible:\n\n- `config/` (YAML/JSON)\n- `src/` (lógica)\n- `bin/` (entrypoints)\n- `logs/`\n\nY en el entrypoint:\n\n1. Cargar config\n2. Validar argumentos\n3. Ejecutar tarea\n4. Log + códigos de salida\n\nSi quieres, te doy un esqueleto listo para producción.'),
(2, '2026-01-02 09:16:10', 1, 'Me interesa que haga logs rotativos y que si falla, salga con código distinto de 0.'),
(2, '2026-01-02 09:16:55', 0, 'Perfecto. Puedes usar `logging.handlers.RotatingFileHandler` y envolver el `main()` con `try/except` devolviendo `sys.exit(1)`.\n\nEjemplo conceptual:\n\n- `INFO`: ejecución normal\n- `WARNING`: recuperable\n- `ERROR`: fallo y `exit(1)`'),

-- Conversación 3 (2026-01-02 10:42:11) - Ideas SaaS educativo
(3, '2026-01-02 10:42:20', 1, 'Estoy pensando en un SaaS educativo. Dame ideas de módulos con enfoque práctico para centros.'),
(3, '2026-01-02 10:43:05', 0, 'Propuesta modular:\n\n1. **Matrícula y seguimiento** (asistencia, progreso, alertas)\n2. **Evaluación** (rúbricas + evidencias)\n3. **Informes** (PDF/Excel automáticos)\n4. **Comunicación** (mensajes y notificaciones)\n5. **Integración Moodle** (altas, matriculaciones, backups)\n\nSi me dices tu flujo real, lo aterrizo a pantallas y endpoints.'),
(3, '2026-01-02 10:43:40', 1, 'Me interesa especialmente integración con Moodle y reporting.'),
(3, '2026-01-02 10:44:15', 0, 'Entonces priorizaría:\n\n- Conector Moodle (API + scripts)\n- Motor de informes (plantillas + datos)\n- Programador de tareas (cron + colas)\n\nY lo dejaría listo para multi-centro (tenant).'),

-- Conversación 4 (2026-01-03 08:30:45) - ffmpeg bash
(4, '2026-01-03 08:30:55', 1, 'Tengo un script bash con ffmpeg y ffprobe. A veces no genera salida aunque no da error. ¿Cómo lo depuro bien?'),
(4, '2026-01-03 08:31:35', 0, 'Medidas prácticas:\n\n- `set -x` temporal\n- guardar `ffmpeg` con `-loglevel info` o `-report`\n- comprobar `return codes`\n- validar rutas (espacios) y existencia de salida\n\nTambién recomiendo escribir un “plan de ejecución” (lista de clips y duraciones) antes de lanzar ffmpeg.'),
(4, '2026-01-03 08:32:05', 1, 'Quiero que deje un log por cada vídeo procesado.'),
(4, '2026-01-03 08:32:40', 0, 'Puedes redirigir salida por archivo:\n\n- `ffmpeg ... >\"logs/$base.out\" 2>\"logs/$base.err\"`\n\nY registrar el resumen (duración, codec, tamaño) en un CSV o JSONL.'),

-- Conversación 5 (2026-01-03 12:05:33) - Modelos de lenguaje
(5, '2026-01-03 12:05:40', 1, 'Explícame diferencias prácticas entre un modelo generalista y uno ajustado con QLoRA.'),
(5, '2026-01-03 12:06:25', 0, 'En práctica:\n\n- **Generalista**: mejor cobertura, más “flexible”, pero menos consistente en tu dominio.\n- **QLoRA fine-tuned**: más consistencia en estilo/formatos y vocabulario, pero puede perder generalidad.\n\nPara un asistente educativo, suele valer la pena ajustar al formato de respuesta y a tus contenidos.'),
(5, '2026-01-03 12:06:55', 1, '¿Qué tamaño de dataset mínimo recomendarías para notar mejora?'),
(5, '2026-01-03 12:07:30', 0, 'Como orientación:\n\n- 500–2.000 ejemplos: mejoras en formato/tono.\n- 5.000–20.000: mejoras más robustas en dominio.\n\nLa clave es calidad + diversidad + evaluación automática.'),

-- Conversación 6 (2026-01-03 18:22:10) - Textos comerciales Jocarsa
(6, '2026-01-03 18:22:20', 1, 'Necesito un texto comercial breve para una solución SaaS de gestión educativa. Sin tecnicismos.'),
(6, '2026-01-03 18:23:00', 0, 'Propuesta:\n\n**Centraliza la gestión de tu centro**: matrícula, seguimiento y evaluación en un único lugar. Ahorra tiempo al equipo, mejora la coordinación y toma decisiones con información clara y actualizada.\n\nSi quieres, lo adapto a un producto concreto (asistencia, actas, integración Moodle…).'),
(6, '2026-01-03 18:23:35', 1, 'Dame también una versión para landing con CTA.'),
(6, '2026-01-03 18:24:10', 0, '**Simplifica la gestión del centro**\n\nAutomatiza tareas, reduce errores y obtén visión completa del alumnado.\n\n- Menos trabajo repetitivo\n- Más control y seguimiento\n- Informes listos en minutos\n\n**Solicita una demo**'),

-- Conversación 7 (2026-01-04 09:01:55) - SQL didáctico
(7, '2026-01-04 09:02:05', 1, 'Quiero una explicación didáctica de JOIN con un ejemplo realista.'),
(7, '2026-01-04 09:03:00', 0, 'Ejemplo típico:\n\n- `clientes(id, nombre)`\n- `pedidos(id, cliente_id, fecha)`\n\nUn `JOIN` une filas relacionadas:\n\n- `INNER JOIN`: solo coincidencias\n- `LEFT JOIN`: todos los clientes, tengan o no pedidos\n\nPuedo darte ejercicios incrementales si me dices tu estructura exacta.'),
(7, '2026-01-04 09:03:35', 1, 'Incluye un caso con clientes sin pedidos.'),
(7, '2026-01-04 09:04:10', 0, 'Ahí el `LEFT JOIN` es el correcto, y filtras con `WHERE pedidos.id IS NULL` para detectar “sin pedidos”.'),

-- Conversación 8 (2026-01-04 11:47:20) - CUDA optimización
(8, '2026-01-04 11:47:30', 1, 'En CUDA, ¿qué optimizaciones básicas aplicarías a un kernel de simulación 3D?'),
(8, '2026-01-04 11:48:20', 0, 'Básicas y efectivas:\n\n- Coalescing en accesos de memoria\n- Evitar ramas divergentes\n- Usar memoria compartida cuando haya reutilización\n- Unificar kernels para reducir overhead\n- Ajustar `blockDim`/`gridDim` con pruebas\n\nSi me dices el patrón de acceso, se puede orientar mejor.'),
(8, '2026-01-04 11:48:55', 1, 'Veo “grid” visual en el render. ¿Cómo lo suavizo?'),
(8, '2026-01-04 11:49:35', 0, 'Opciones:\n\n- Trilinear sampling en render\n- Añadir detalle en un “render-pass” (ruido advectado)\n- Dithering suave\n\nLa más limpia suele ser trilinear + un noise pass coherente.'),

-- Conversación 9 (2026-01-04 16:10:02) - Ejercicios Python
(9, '2026-01-04 16:10:10', 1, 'Necesito ideas de ejercicios prácticos de Python orientados a automatización.'),
(9, '2026-01-04 16:10:55', 0, 'Ideas útiles:\n\n1. Renombrador masivo de archivos con reglas\n2. Extractor de datos de CSV a SQLite\n3. Generador de informes en PDF\n4. Monitor de carpetas (watchdog)\n5. Backup incremental con hashing\n\nPuedo estructurarlos como “ejercicio continuo” si quieres.'),
(9, '2026-01-04 16:11:25', 1, 'Que sean proyectos cortos pero reales.'),
(9, '2026-01-04 16:12:05', 0, 'Perfecto: objetivos claros, input/output definidos y pruebas mínimas. También puedo incluir una plantilla de proyecto por ejercicio.'),

-- Conversación 10 (2026-01-05 08:55:40) - JS rápido
(10, '2026-01-05 08:55:50', 1, 'En JavaScript, ¿cómo recorro un array y construyo un objeto índice por id?'),
(10, '2026-01-05 08:56:20', 0, 'Patrón típico: `reduce()` para construir un diccionario por clave.\n\nSi me das ejemplo de entrada/salida, lo dejo exacto.'),

-- Conversación 11 (2026-01-05 13:18:27) - Monetización
(11, '2026-01-05 13:18:35', 1, 'Tengo contenidos educativos. ¿Qué vías de monetización encajan con un enfoque técnico?'),
(11, '2026-01-05 13:19:20', 0, 'Vías comunes:\n\n- Libros (KDP) por temáticas\n- Cursos (plataforma propia)\n- Suscripción (contenidos + soporte)\n- Licencias B2B para centros\n- Plantillas/recursos (datasets, proyectos base)\n\nLa combinación B2C + B2B suele estabilizar ingresos.'),
(11, '2026-01-05 13:20:00', 1, 'Me interesa un modelo recurrente.'),
(11, '2026-01-05 13:20:40', 0, 'Entonces:\n\n- Suscripción con entregas semanales\n- Roadmap público\n- Comunidad (soporte)\n- Herramientas (mini-SaaS) como parte del plan'),

-- Conversación 12 (2026-01-05 19:44:09) - PHP SQLite
(12, '2026-01-05 19:44:20', 1, 'Tengo una app PHP con SQLite. ¿Qué patrón recomiendas para evitar SQL injection y mantenerlo simple?'),
(12, '2026-01-05 19:45:05', 0, 'En SQLite con PHP:\n\n- `PDO` con `prepare()` y parámetros enlazados\n- Repositorios por entidad (métodos simples)\n- Validación de input antes de la capa de datos\n\nSi quieres, te propongo un mini-DAO por tabla.'),
(12, '2026-01-05 19:45:40', 1, 'También quiero paginación y búsqueda.'),
(12, '2026-01-05 19:46:20', 0, 'Paginación: `LIMIT :limit OFFSET :offset`.\n\nBúsqueda: construir `WHERE` con campos permitidos (whitelist), y parámetros para valores.'),

-- Conversación 13 (2026-01-06 09:07:31) - Documentación
(13, '2026-01-06 09:07:40', 1, 'Necesito un esquema de documentación técnica para un proyecto (README + docs).'),
(13, '2026-01-06 09:08:25', 0, 'Estructura mínima:\n\n- README: propósito, instalación, uso, ejemplos\n- `docs/`: arquitectura, API, despliegue, contribución\n- Changelog\n- Licencia\n\nSi el proyecto es SaaS, añadiría “Operación” (backups, logs, monitorización).'),
(13, '2026-01-06 09:09:00', 1, 'Incluye sección de despliegue con variables de entorno.'),
(13, '2026-01-06 09:09:35', 0, 'Correcto: tabla de variables (`NAME`, `required`, `default`, `description`) + ejemplo `.env.example`.'),

-- Conversación 14 (2026-01-06 12:56:48) - IA local arquitectura
(14, '2026-01-06 12:56:55', 1, 'Quiero una arquitectura de IA local para un asistente educativo, con evaluación automática de respuestas.'),
(14, '2026-01-06 12:57:40', 0, 'Arquitectura típica:\n\n- Ingesta → chunking → embeddings → índice\n- RAG: recuperación + prompt\n- Respuesta\n- Evaluación: corrector(es) + rúbrica + umbral\n- Reintentos controlados + logging\n\nSi me dices el formato de salida, lo dejo cerrado (JSON/Markdown).'),
(14, '2026-01-06 12:58:15', 1, 'Quiero que la evaluación genere nota sobre 10 y feedback.'),
(14, '2026-01-06 12:59:00', 0, 'Entonces define una rúbrica fija (criterios y pesos) y fuerza salida estructurada, por ejemplo:\n\n- `nota`\n- `fortalezas`\n- `mejoras`\n- `feedback`'),

-- Conversación 15 (2026-01-06 17:20:14) - Dataset JSONL
(15, '2026-01-06 17:20:25', 1, 'Estoy generando JSONL para entrenamiento. ¿Cómo aseguro diversidad sin perder calidad?'),
(15, '2026-01-06 17:21:10', 0, 'Prácticas:\n\n- Mezclar niveles (básico/intermedio/avanzado)\n- Variar formatos (Q/A, explicación, corrección)\n- Controlar duplicados (hash)\n- Validar estructura (schema)\n- Muestreo manual de calidad por lotes\n\nY tener un set de evaluación fijo para comparar versiones.'),
(15, '2026-01-06 17:21:55', 1, '¿Recomiendas “best-of-N” para generar respuestas?'),
(15, '2026-01-06 17:22:35', 0, 'Sí, si puedes costeártelo: genera N y elige por una métrica (longitud mínima, checklist, o un corrector).'),

-- Conversación 16 (2026-01-07 08:11:03) - Backups Moodle
(16, '2026-01-07 08:11:10', 1, 'Quiero automatizar backups de cursos Moodle y enviarlos por SSH a un servidor remoto.'),
(16, '2026-01-07 08:12:00', 0, 'Enfoque robusto:\n\n- Script que llame al backup (MBZ)\n- Verificación de tamaño/exit code\n- Transferencia con `scp`/`rsync`\n- Limpieza del temporal\n- Log en JSONL\n\nSi me dices IDs de curso y rutas, lo dejo parametrizable.'),
(16, '2026-01-07 08:12:35', 1, 'Quiero evitar llenar el disco con temporales.'),
(16, '2026-01-07 08:13:10', 0, 'Entonces:\n\n- Directorio temporal dedicado\n- Comprobación de espacio antes\n- Limpieza incluso en error (`trap` en bash o `finally` en Python)\n- Retención en remoto (rotación).'),

-- Conversación 17 (2026-01-07 10:39:58) - Intro libro técnico
(17, '2026-01-07 10:40:10', 1, 'Necesito una introducción para un libro técnico, estilo didáctico y directo.'),
(17, '2026-01-07 10:41:00', 0, 'Estructura recomendada:\n\n- Qué aprenderá el lector\n- A quién va dirigido\n- Cómo usar el libro (ejercicio continuo)\n- Requisitos mínimos\n- Qué no cubre\n\nSi me dices tema exacto, la redacto completa.'),
(17, '2026-01-07 10:41:35', 1, 'Tema: SQL práctico para FP.'),
(17, '2026-01-07 10:42:20', 0, 'Perfecto: orientaría el texto a aprendizaje por proyectos, con progresión y objetivos evaluables.'),

-- Conversación 18 (2026-01-07 14:02:41) - UX plataforma educativa
(18, '2026-01-07 14:02:50', 1, 'Quiero revisar UX de una plataforma educativa: pantallas esenciales y navegación.'),
(18, '2026-01-07 14:03:40', 0, 'Navegación mínima:\n\n- Dashboard (alertas y acciones)\n- Alumnos\n- Cursos / grupos\n- Evaluación / actas\n- Informes\n- Integraciones\n- Ajustes\n\nEn cada pantalla: búsqueda rápida + filtros + acciones primarias visibles.'),
(18, '2026-01-07 14:04:15', 1, 'Quiero que sea muy rápido para el profesor, con pocas pulsaciones.'),
(18, '2026-01-07 14:05:00', 0, 'Entonces:\n\n- Acciones frecuentes como botones directos\n- “Últimos usados”\n- Atajos de teclado\n- Formularios con autocompletado\n- Persistencia de filtros por usuario');

