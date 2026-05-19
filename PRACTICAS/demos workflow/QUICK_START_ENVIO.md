# 🚀 Quick Start - Envío de Emails

## ⚡ Configuración en 3 Pasos

### 1️⃣ Configurar Gmail (Primera vez)

```
n8n → Credentials → + New Credential
→ Gmail OAuth2
→ Autorizar cuenta
→ Guardar como "Gmail account"
```

### 2️⃣ Activar Envío

Edita nodo: **⚙️ Config Email Sender**

```diff
- SEND_EMAILS: "false"
+ SEND_EMAILS: "true"

- TARGET_EMAIL: "test@example.com"
+ TARGET_EMAIL: "tuemail@gmail.com"
```

### 3️⃣ Ejecutar

```
Workflow → Execute ▶️
Esperar ~40 segundos
✅ ¡Revisa tu inbox!
```

---

## 📊 Modos de Operación

### 🔵 Modo: Solo Generar (por defecto)

```
SEND_EMAILS: "false"
```

**Resultado:**
- ✅ Genera 19 emails
- ✅ Exporta JSON
- ✅ Crea reporte
- ❌ NO envía

**Tiempo:** <1 segundo

---

### 📧 Modo: Generar + Enviar

```
SEND_EMAILS: "true"
TARGET_EMAIL: "tu@email.com"
```

**Resultado:**
- ✅ Genera 19 emails
- ✅ Exporta JSON
- ✅ Crea reporte
- ✅ ENVÍA por Gmail

**Tiempo:** ~40 segundos

---

## 🎯 Estructura de Nodos

```
┌─────────────────────────────────────────┐
│  Manual Trigger                         │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Generate Demo Emails                   │
│  (19 emails en 5 categorías)            │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Clasificar por Categoría               │
│  (If CLIENT, BILLING, LEAD...)          │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Etiquetar (CLIENTE 🔵, etc)           │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Merge All Categories                   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Format Date + Create Summary           │
└──────────────┬──────────────────────────┘
               │
               ├──────────────┐
               │              │
               ▼              ▼
     ┌─────────────┐  ┌─────────────┐
     │ Export JSON │  │ Generate    │
     └─────────────┘  │ Report      │
                      └─────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  ⚙️ Config Email Sender                │
│  SEND_EMAILS: true/false                │
│  TARGET_EMAIL: tu@email.com             │
│  DELAY_SECONDS: 2                       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  ¿Enviar emails? (IF)                   │
└──────┬───────────────────────┬──────────┘
       │ SÍ                    │ NO
       │                       │
       ▼                       ▼
┌──────────────┐      ┌────────────────┐
│ Prepare Data │      │ Skip to Merge  │
└──────┬───────┘      └────────┬───────┘
       │                       │
       ▼                       │
┌──────────────┐              │
│ Delay 2s     │              │
└──────┬───────┘              │
       │                       │
       ▼                       │
┌──────────────┐              │
│ 📧 Gmail     │              │
│    Send      │              │
└──────┬───────┘              │
       │                       │
       ▼                       │
┌──────────────┐              │
│ Track Sent   │              │
└──────┬───────┘              │
       │                       │
       └───────┬───────────────┘
               ▼
       ┌───────────────┐
       │ Merge Results │
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │ 📊 Final      │
       │    Report     │
       └───────────────┘
```

---

## 📧 Ejemplo de Email Enviado

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
De: tu-cuenta-gmail@gmail.com
Para: tu@email.com
Asunto: 🧪 [DEMO] 🔵 CLIENTE - Cambio de cita
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📧 EMAIL DE PRUEBA GENERADO AUTOMÁTICAMENTE

🏷️  CATEGORÍA: 🔵 CLIENTE
📤 Remitente original: maria.garcia@cliente.com
📋 Asunto: Cambio de cita para la próxima semana

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTENIDO DEL EMAIL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Buenos días,

Necesito cambiar mi cita del próximo martes...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️  Generado por: EMAIL_GENERATOR_DEMO
🎯 Propósito: Testing clasificación
📅 Generado: 2026-04-23 10:30:00

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🎯 Categorías de Emails

| Emoji | Categoría | Cantidad |
|-------|-----------|----------|
| 🔵 | CLIENTE | 4 emails |
| 💰 | FACTURAS | 4 emails |
| 🟢 | LEAD | 4 emails |
| 🟡 | INTERNO | 3 emails |
| 🔴 | SPAM | 4 emails |

**Total:** 19 emails

---

## ⚙️ Configuración Recomendada

### Testing Local
```
SEND_EMAILS: "false"
```
→ Solo genera, no envía

### Testing Real
```
SEND_EMAILS: "true"
TARGET_EMAIL: "tu-test@gmail.com"
DELAY_SECONDS: "2"
```
→ Envía a buzón de prueba

### Demo Cliente
```
SEND_EMAILS: "true"
TARGET_EMAIL: "cliente@empresa.com"
DELAY_SECONDS: "3"
```
→ Demo en vivo

---

## 🔒 Seguridad

✅ **Usa cuenta de prueba de Gmail**
✅ **Nunca uses email personal principal**
✅ **Verifica límites diarios de Gmail**
✅ **Revisa carpeta Spam periódicamente**

---

## 📈 Tiempos de Ejecución

```
Solo Generar:    <1 segundo
Generar + Enviar: ~40 segundos

Breakdown:
  - Generación:    <1s
  - Clasificación: <1s
  - Envío 19 x 2s: 38s
  - Reporte:       <1s
  ────────────────────
  Total:           ~40s
```

---

## 🐛 Troubleshooting Rápido

### ❌ "Credentials not found"
→ Configura Gmail OAuth2 en Credentials

### ❌ "Rate limit exceeded"
→ Aumenta DELAY_SECONDS a 5

### ❌ Emails no llegan
→ Revisa Spam en tu bandeja

### ⚠️ "No se enviaron emails"
→ SEND_EMAILS debe ser "true"

---

## ✅ Checklist Pre-Ejecución

- [ ] Credencial Gmail configurada
- [ ] SEND_EMAILS: "true"
- [ ] TARGET_EMAIL: correcto
- [ ] Gmail conectado en nodo 📧
- [ ] Buzón de destino vacío (recomendado)

---

## 📚 Documentación Completa

→ **GUIA_ENVIO_EMAILS.md** - Guía detallada
→ **EMAIL_GENERATOR_DEMO.json** - Workflow

---

**🚀 ¡Listo para enviar emails de prueba!**
