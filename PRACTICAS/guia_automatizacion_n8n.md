# 📧 Sistema de Automatización de Correos con IA (n8n + Ollama)

## 🧠 Descripción general

Este sistema automatiza la gestión de correos electrónicos utilizando inteligencia artificial.

Su funcionamiento se basa en:
1. Recepción automática de emails
2. Análisis mediante IA
3. Generación de borradores de respuesta
4. Validación humana (aprobación o rechazo)
5. Envío automático al cliente

---

## ⚙️ Flujo del sistema

Gmail Trigger
↓
Preparación de datos (Set)
↓
Clasificación con IA (Ollama)
↓
Parseo del resultado (Code)
↓
Generación de borrador (IA)
↓
Preparar revisión (Set)
↓
Envío al responsable (Gmail)
↓
Wait (espera decisión)
↓
IF (aprobado / rechazado)
├─ aprobado → responder al cliente
└─ rechazado → revisión manual

---

## 🔧 Configuración paso a paso

### 1. Recepción del correo
Nodo: Gmail Trigger  
Detecta nuevos correos y extrae:
- remitente
- asunto
- contenido
- messageId

---

### 2. Preparación de datos
Nodo: Set  
Normaliza la información del email.

---

### 3. Clasificación con IA
Nodo: Basic LLM Chain + Ollama  
Modelo: llama3  
Clasifica el correo en categoría, prioridad, resumen e intención.

---

### 4. Parseo del resultado
Nodo: Code  
Convierte la salida de la IA en datos utilizables.

---

### 5. Generación del borrador
Nodo: Basic LLM Chain  
Genera una respuesta profesional basada en el análisis.

---

### 6. Preparación para revisión
Nodo: Set  
Se almacenan:
- borrador
- messageId
- datos del correo

Se generan enlaces de aprobación:
- approve
- reject

---

### 7. Envío al responsable
Nodo: Gmail (Send)  
Envía el correo con:
- resumen
- borrador
- enlaces de decisión

---

### 8. Espera de decisión
Nodo: Wait  
Pausa el flujo hasta que el responsable decide.

---

### 9. Evaluación
Nodo: IF  
Determina si se aprueba o rechaza.

---

### 10. Respuesta automática
Nodo: Gmail (Reply)  
Responde automáticamente al cliente si se aprueba.

---

### 11. Rechazo
Nodo: Gmail (Send)  
Notifica revisión manual.

---

## 🚀 Ventajas

- Ahorro de tiempo
- Automatización inteligente
- Control humano
- Escalable

---

## ✅ Estado

Sistema funcional con IA local, automatización y validación humana.
