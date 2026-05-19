# 📧 Guía: Envío Automático de Emails

## 🎯 Nueva Funcionalidad Añadida

El workflow **EMAIL_GENERATOR_DEMO.json** ahora puede **enviar automáticamente** los correos generados por Gmail para testing real.

---

## ⚙️ Configuración Rápida

### Paso 1: Configurar credenciales de Gmail

1. En n8n, ve a **Credentials**
2. Crea una nueva credencial de **Gmail OAuth2**
3. Sigue el proceso de autenticación con tu cuenta de Gmail
4. Guarda la credencial con el nombre: `Gmail account`

### Paso 2: Activar el envío

Edita el nodo **"⚙️ Config Email Sender"** y configura:

```javascript
SEND_EMAILS: "true"        // Cambiar de "false" a "true"
TARGET_EMAIL: "tu@email.com"  // Tu email de prueba
DELAY_SECONDS: "2"         // Segundos entre cada envío
```

### Paso 3: Ejecutar el workflow

1. Haz clic en **"Execute Workflow"**
2. Los emails se generarán y enviarán automáticamente
3. Verás el progreso en tiempo real
4. Al final, obtendrás un reporte detallado

---

## 📋 Opciones de Configuración

### SEND_EMAILS
- `"false"` → No envía, solo genera (por defecto)
- `"true"` → Genera Y envía los emails

### TARGET_EMAIL
- Email destino donde se enviarán TODOS los correos de prueba
- Recomendado: usa tu propio email para testing

### DELAY_SECONDS
- Segundos de espera entre cada envío
- Mínimo recomendado: `2` segundos
- Evita saturar el servidor de correo

---

## 🔄 Flujo del Workflow

```
1. Generate Demo Emails
   ↓
2. Clasificar por categorías
   ↓
3. Etiquetar y formatear
   ↓
4. ⚙️ Config Email Sender
   ↓
5. ¿Enviar emails? (IF)
   ↓
   ├─ NO → Merge Results (salta envío)
   └─ SÍ → Continuar
       ↓
6. Prepare Email Data
   ↓
7. Delay Between Sends (2s)
   ↓
8. 📧 Gmail Send (envío real)
   ↓
9. Track Sent Emails
   ↓
10. 📊 Final Send Report
```

---

## 📧 Formato del Email Enviado

Cada email se envía con este formato:

**Asunto:**
```
🧪 [DEMO] 🔵 CLIENTE - Cambio de cita para la próxima semana
```

**Cuerpo:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 EMAIL DE PRUEBA GENERADO AUTOMÁTICAMENTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏷️  CATEGORÍA: 🔵 CLIENTE
📤 Remitente original: maria.garcia@cliente.com
📋 Asunto: Cambio de cita para la próxima semana

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTENIDO DEL EMAIL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Buenos días,

Necesito cambiar mi cita del próximo martes a jueves...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️  Este es un email de prueba generado por:
    EMAIL_GENERATOR_DEMO workflow
    
🎯 Propósito: Testing del sistema de clasificación
📅 Generado: 2026-04-23 10:30:00

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📊 Reporte Final

Al terminar, el workflow genera un reporte:

```
╔══════════════════════════════════════════════════════╗
║       📧 REPORTE DE ENVÍO DE EMAILS DEMO           ║
╚══════════════════════════════════════════════════════╝

✅ EMAILS ENVIADOS: 19

  1. client - Cambio de cita para la próxima semana
     📤 Enviado a: tu@email.com
     🕐 2026-04-23T10:30:00.000Z

  2. client - Problema con mi pedido #12345
     📤 Enviado a: tu@email.com
     🕐 2026-04-23T10:30:02.000Z
  
  [... continúa con todos los emails ...]

════════════════════════════════════════════════════════
📊 Total emails generados: 19
📤 Enviados: 19
📥 No enviados: 0
════════════════════════════════════════════════════════
```

---

## ✅ Ventajas de Enviar vs Solo Generar

### Solo Generar (SEND_EMAILS: false)
- ⚡ Instantáneo
- 💾 Exporta JSON/TXT
- 🔍 Revisión manual
- 📋 Planificación

### Generar + Enviar (SEND_EMAILS: true)
- ✅ Testing real de clasificación
- 📧 Prueba del workflow completo
- 🔄 Integración end-to-end
- 🎯 Validación de bandeja de entrada

---

## 🎯 Casos de Uso

### 1. Testing Inicial
```javascript
SEND_EMAILS: "false"
```
→ Solo genera y revisa los emails

### 2. Testing de Clasificador
```javascript
SEND_EMAILS: "true"
TARGET_EMAIL: "tu-buzón-test@gmail.com"
```
→ Envía a un buzón de prueba y valida clasificación

### 3. Demo a Cliente
```javascript
SEND_EMAILS: "true"
TARGET_EMAIL: "cliente@empresa.com"
```
→ Muestra el sistema funcionando en vivo

---

## 🚨 Importante

### Límites de Gmail
- **Máximo 500 emails/día** (cuenta gratuita)
- **Máximo 100 emails/hora**
- Usa delay de 2-3 segundos entre envíos

### Buenas Prácticas
1. **Usa email de prueba** no tu email principal
2. **Verifica credenciales** antes de ejecutar
3. **Empieza con pocos emails** para probar
4. **Revisa spam** por si Gmail filtra los emails

---

## 🔧 Personalización

### Cambiar el asunto del email

Edita el nodo **"📧 Gmail Send"**, campo `subject`:

```javascript
// Actual
"🧪 [DEMO] {{ $json.category_label }} - {{ $json.email_subject }}"

// Personalizado
"[MI EMPRESA] {{ $json.category_label }} - {{ $json.email_subject }}"
```

### Cambiar el cuerpo del email

Edita el nodo **"📧 Gmail Send"**, campo `message`:

```javascript
// Puedes añadir tu logo, firma, etc.
```

### Cambiar el delay

Edita **"⚙️ Config Email Sender"**:

```javascript
DELAY_SECONDS: "5"  // Más lento y seguro
```

---

## 🐛 Solución de Problemas

### ❌ Error: "Credentials not found"

**Solución:**
1. Verifica que creaste la credencial de Gmail
2. El nodo "📧 Gmail Send" debe tener la credencial configurada
3. Reconecta la credencial si es necesario

### ❌ Error: "Rate limit exceeded"

**Solución:**
1. Aumenta `DELAY_SECONDS` a 5 o más
2. Espera 1 hora y vuelve a intentar
3. Verifica los límites de tu cuenta de Gmail

### ❌ Emails no llegan

**Solución:**
1. Revisa la carpeta de **Spam**
2. Verifica que `TARGET_EMAIL` sea correcto
3. Comprueba el reporte final para ver si se enviaron
4. Revisa los logs de n8n por errores

### ⚠️ "No se enviaron emails"

**Causa:** `SEND_EMAILS` está en `"false"`

**Solución:** Cámbialo a `"true"` en el nodo de configuración

---

## 📈 Estadísticas de Envío

| Emails | Tiempo Aprox | Delay |
|--------|--------------|-------|
| 19 | ~40 segundos | 2s |
| 19 | ~1 minuto | 3s |
| 50 | ~2 minutos | 2s |
| 100 | ~5 minutos | 3s |

---

## 🎯 Próximos Pasos

Una vez que tengas emails enviados:

1. **Conecta el MAIL_PROCESSOR** para clasificarlos
2. **Valida la precisión** del clasificador
3. **Ajusta las reglas** si es necesario
4. **Repite el proceso** con diferentes emails

---

## 📞 Resumen Rápido

```powershell
# 1. Configurar credencial Gmail en n8n
# 2. Editar nodo "⚙️ Config Email Sender":
SEND_EMAILS: "true"
TARGET_EMAIL: "tu@email.com"

# 3. Ejecutar workflow
# 4. Esperar ~40 segundos
# 5. Revisar tu bandeja de entrada
# 6. Validar clasificación
```

---

**✅ ¡Listo para enviar emails de prueba automáticamente!**

Recuerda siempre usar un email de prueba y verificar los límites de Gmail.
