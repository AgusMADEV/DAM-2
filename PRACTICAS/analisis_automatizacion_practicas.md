# Automatización de procesos — Resumen + análisis inicial (n8n / Make / Zapier)

> Documento de trabajo para prácticas (DAM) — **Agustín Morcillo**  
> Objetivo: sintetizar necesidades, requisitos y una primera comparación de herramientas de automatización **en base a costes y funcionalidades**.

---

## 1) Resumen del audio (necesidades por áreas)

### 1.1 Área técnica — incidencias / tickets
- **Centralizar incidencias** cuando llegan (principalmente por **correo**).
- **Crear ticket automáticamente**.
- **Notificar** el ticket a los **técnicos disponibles**.
- Registrar y guardar **trazabilidad** (historial y seguimiento).
- **Envíos diferenciados** en función del tipo de incidencia (routing).

### 1.2 Área comercial — leads / CRM
- Cuando entra un cliente:
  - por **llamada** (se registra en CRM) o por **web**,
  - **asignarlo automáticamente** a una persona (por reglas o reparto).
  - enviar **emails de bienvenida** / secuencia inicial (automatizada).

### 1.3 Área administrativa — facturación
- Tener referencia de los **productos/servicios a facturar**.
- Recibir “órdenes” por canales como:
  - **correo**, **WhatsApp**, **Slack** (u otros),
- y que el sistema de facturación genere la **factura automáticamente** (o al menos un borrador), evitando elaborar manualmente.

### 1.4 Extra — clasificación y prioridad de correos (Gmail / Google)
- Clasificar correos por tipo y **prioridad**.
- Implementar **etiquetado automático** dentro de Gmail / Google Workspace.

### 1.5 IA (ChatGPT u otras)
- Posibilidad de usar IA para clasificación, extracción de campos, resúmenes y priorización.
- Se debe evaluar si conviene ChatGPT u otra alternativa “mejor” para el caso.

---

## 2) Requisitos técnicos mínimos (lo que la herramienta debe cubrir)

### 2.1 Integraciones clave
- **Gmail / Google Workspace**: leer, etiquetar, mover, responder, disparar flujos.
- **CRM** (según herramienta concreta usada en la empresa): crear/actualizar lead, asignar responsable, seguimiento.
- **Slack**: notificaciones, creación de tareas/tickets, mensajes automáticos.
- **WhatsApp**: integración normalmente vía API oficial (Meta) o proveedores (Twilio / 360dialog / etc.).

### 2.2 Capacidades funcionales necesarias
- **Triggers**: correo entrante, formularios web, cambios en CRM, webhooks, etc.
- **Reglas + condiciones**: if/else, rutas, filtros, prioridades.
- **Plantillas de email** y secuencias (bienvenida, respuesta de incidencia, etc.).
- **Trazabilidad**: logs de ejecución y evidencias (qué pasó, cuándo, con qué datos).
- **Manejo de errores**: reintentos, control de fallos, alertas.

### 2.3 Requisitos si se usa IA
- Enviar texto (email/incidencia) a un modelo para:
  - **clasificación** (tipo/tema),
  - **prioridad**,
  - **extracción de campos** (cliente, producto, urgencia),
  - **resumen** para notificación a técnicos.
- Recomendable:
  - si IA “duda” → **revisión humana** o ruta alternativa,
  - guardar “razón/resultado” para auditoría,
  - cuidado con **datos sensibles** y cumplimiento (política interna).

---

## 3) Comparativa inicial (n8n vs Make vs Zapier)

> Enfoque: encaje con los procesos descritos + visión general de costes (sin precios cerrados).

### 3.1 n8n
**Encaje**
- Muy bueno para flujos con lógica compleja: routing de incidencias, asignaciones, reglas por prioridad.
- Muy adecuado si se busca **control de datos** y **flexibilidad** (webhooks, APIs, JSON, ramas).
- Posible **auto-hosting** (VPS), útil para optimizar costes a medio plazo.

**Coste (visión práctica)**
- **Auto-host**: coste de servidor + mantenimiento (updates, backups, seguridad).
- **Cloud**: cuota, con potencia y flexibilidad.

**Puntos a vigilar**
- Requiere perfil técnico mínimo para administrar.
- WhatsApp suele depender de proveedores/API oficial.

**Ideal si…**
- Se quiere una solución robusta, escalable y con control (y hay soporte técnico básico).

---

### 3.2 Make (Integromat)
**Encaje**
- Equilibrio muy bueno: **cloud** + potencia + visual.
- Flujos con condiciones, routers, transformaciones suelen ser más cómodos que en Zapier.
- Buena opción si no quieren auto-alojar nada.

**Coste (visión práctica)**
- Suele ser competitivo, pero el coste crece con el **volumen de operaciones**.

**Puntos a vigilar**
- Si hay mucho tráfico (muchos correos, muchos tickets), revisar escalabilidad del coste.

**Ideal si…**
- Se busca potencia en la nube y rapidez sin administrar servidores.

---

### 3.3 Zapier
**Encaje**
- El más rápido de arrancar para automatizaciones simples (Gmail → Slack → CRM → email).
- Muy accesible para perfiles no técnicos.

**Coste (visión práctica)**
- A menudo el coste escala peor cuando aumentan tareas/volumen o flujos complejos.

**Puntos a vigilar**
- Flujos complejos pueden volverse limitados o caros.
- Menos “control fino” que n8n/Make.

**Ideal si…**
- Se busca prototipar muy rápido y el volumen inicial es bajo/moderado.

---

## 3.4 Comparación de precios (referencia rápida — marzo 2026)

> **Nota:** los precios cambian con frecuencia. Además, cada herramienta cobra por “unidad de uso” distinta:  
> - **n8n Cloud**: por *workflow executions/mes* (ejecuciones de workflow).  
> - **Make**: por *credits/mes* (cada acción/módulo suele contar como 1 crédito).  
> - **Zapier**: por *tasks/mes* (cada acción “exitosa” suele contar como 1 task).

### 3.4.1 Tabla orientativa (planes de entrada)
| Herramienta | Plan | Precio (aprox.) | Incluye / límite principal |
|---|---|---:|---|
| **n8n** | Starter (Cloud) | **20€ / mes** (facturado anual) | ~**2.5K ejecuciones/mes** |
| **n8n** | Pro (Cloud) | **50€ / mes** (facturado anual) | ~**10K ejecuciones/mes** |
| **n8n** | Business | **667€ / mes** (facturado anual) | ~**40K ejecuciones/mes**, SSO y features enterprise |
| **Make** | Free | **$0 / mes** | Hasta **1,000 credits/mes** |
| **Make** | Core | **$9 / mes** | Precio base para **10K credits/mes** |
| **Make** | Pro | **$16 / mes** | Precio base para **10K credits/mes** |
| **Make** | Teams | **$29 / mes** | Precio base para **10K credits/mes** |
| **Zapier** | Professional | **$19.99 / mes** (facturado anual) | “Starting from” (el precio sube según el tier de tasks) |
| **Zapier** | Team | **$69 / mes** (facturado anual) | “Starting from”, orientado a equipos |
| **Zapier** | Free | **$0 / mes** | Muy limitado (principalmente pruebas/uso básico) |

### 3.4.2 Lectura rápida de costes para vuestro caso (incidencias + CRM + facturación + Gmail)
- Si el volumen de automatizaciones crece (muchos correos/tickets/leads), **Make y Zapier** pueden subir rápido porque el coste va ligado a *credits/tasks*.  
- **n8n auto-hosted** puede ser más estable en coste (pagas servidor + mantenimiento), y suele interesar si:
  - hay muchas ejecuciones,
  - queréis control de datos,
  - o necesitáis flujos complejos con menos límites.

### 3.4.3 Coste “real” de auto-host (referencia)
Si se auto-hospeda n8n (o una herramienta propia), el coste típico se compone de:
- VPS/servidor (según recursos y SLA),
- backups,
- tiempo de mantenimiento (actualizaciones, seguridad, monitorización).

---

## 4) Recomendación inicial (sin casarse aún con una sola herramienta)

### 4.1 Para piloto “serio”
- **n8n** si se prioriza: control, flexibilidad, escalabilidad y coste medio plazo (auto-host).
- **Make** si se prioriza: cloud + potencia + rapidez sin infra.

### 4.2 Zapier como alternativa
- Para un piloto muy rápido y sencillo (quick wins) o si el equipo es muy no-técnico.

---

## 5) IA en el flujo (propuesta práctica)

### 5.1 Casos de uso directos
- Clasificar correos: **incidencia / comercial / facturación / otros**.
- Calcular **prioridad** y etiquetar (Gmail).
- Resumir incidencias para técnicos y canal Slack.
- Extraer campos útiles (cliente, producto, urgencia, id interno).

### 5.2 Buenas prácticas
- “Human-in-the-loop” cuando el score sea bajo o haya riesgo.
- Guardar logs de decisión.
- Sanitizar/filtrar datos sensibles si procede.

---

## 6) Propuesta de plan de trabajo (para presentar al responsable)

### 6.1 Paso 1 — inventario de procesos
- Listar 10–20 procesos candidatos con:
  - canal de entrada (Gmail/web/CRM/Slack/WhatsApp),
  - frecuencia/volumen,
  - criticidad,
  - datos sensibles,
  - salida deseada (ticket, email, factura, tarea, etc.).

### 6.2 Paso 2 — seleccionar 3 pilotos
- **Piloto 1 (correo → clasificación → etiqueta → Slack)**  
  Gmail → IA/Reglas → etiquetas → notificación a técnicos/ops en Slack.
- **Piloto 2 (lead → CRM → asignación → bienvenida)**  
  Form web/CRM → asignación responsable → email bienvenida/seguimiento.
- **Piloto 3 (orden → facturación)**  
  Email/Slack/WhatsApp → extracción de datos → creación factura (o borrador) en sistema de facturación.

### 6.3 Paso 3 — comparar en ejecución
Para cada herramienta (n8n/Make/Zapier):
- tiempo de implementación del piloto,
- coste estimado mensual según volumen,
- mantenimiento requerido,
- trazabilidad (logs),
- gestión de errores y alertas,
- facilidad de evolución (añadir nuevas reglas/casos).

---

## 7) Nota sobre “automatizador propio” / NodeFlow (prototipo)

- **Puede servir** como PoC interna o para automatizaciones muy específicas (datos/archivos/pipelines).
- Para reemplazar n8n/Make/Zapier “en empresa real” faltan piezas típicas:
  - conectores SaaS (Gmail/CRM/Slack/WhatsApp/facturación) listos,
  - autenticación/roles,
  - gestión de credenciales/secretos,
  - triggers robustos (cron/webhooks),
  - historial de ejecuciones y auditoría,
  - reintentos/colas/concurrencia.

**Propuesta realista**
- Usar **n8n o Make** como orquestador principal.
- Si hace falta lógica custom, construir módulos/servicios propios (y NodeFlow podría ser un apoyo técnico, no el core).

---

## 8) Próximos datos a pedir al responsable (para cerrar decisión)
- ¿Qué **CRM** exacto usan?
- ¿Qué **sistema de facturación** usan?
- ¿Google Workspace sí/no? (Gmail corporativo)
- Canales reales para “órdenes”: ¿WhatsApp es imprescindible o es “nice to have”?
- Volumen estimado:
  - correos/día,
  - incidencias/semana,
  - leads/día,
  - facturas/mes.
- Restricciones de seguridad/compliance (datos sensibles, dónde se puede alojar).
- Saber si ya tienen un sistema de automatización, con n8n, que me haga una lista de TODO lo que usan.

---

**Fin del documento.**
