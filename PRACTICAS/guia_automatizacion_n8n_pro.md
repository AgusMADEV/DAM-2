# 📧 Sistema de Automatización Inteligente de Correos  
## n8n + IA local (Ollama)

---

## 🧠 Resumen ejecutivo

Este sistema automatiza la gestión de correos electrónicos mediante inteligencia artificial, manteniendo control humano antes de enviar cualquier respuesta.

Permite:
- Analizar automáticamente emails entrantes
- Clasificarlos por tipo y prioridad
- Generar respuestas profesionales
- Validar mediante aprobación humana
- Responder automáticamente al cliente

---

## 🔁 Flujo general del sistema

```text
Cliente envía email
        ↓
Gmail Trigger (entrada)
        ↓
Normalización de datos (Set)
        ↓
Clasificación IA (Ollama)
        ↓
Parseo de resultado (Code)
        ↓
Generación de respuesta IA
        ↓
Preparación de revisión
        ↓
Envío al responsable
        ↓
⏸ Espera decisión (Wait)
        ↓
Decisión (IF)
   ├── ✔ Aprobado → Respuesta automática
   └── ❌ Rechazado → Revisión manual
```

---

## ⚙️ Arquitectura del sistema

### 🔹 Entrada
- Gmail Trigger
- Captura emails en tiempo real

### 🔹 Procesamiento IA
- Ollama (IA local)
- Clasificación + generación de texto

### 🔹 Control de flujo
- n8n (orquestación completa)

### 🔹 Validación humana
- Enlace de aprobación/rechazo

---

## 🧩 Componentes clave

### 1. 📥 Recepción del correo
Nodo: Gmail Trigger  
Captura:
- Remitente
- Asunto
- Contenido
- ID del mensaje

---

### 2. 🧹 Preparación de datos
Nodo: Set  
Estandariza la información para la IA

---

### 3. 🤖 Clasificación con IA
Nodo: Basic LLM Chain  
Modelo: Ollama (llama3)

Salida:
- Categoría
- Prioridad
- Resumen
- Intención

---

### 4. 🔧 Transformación de datos
Nodo: Code  
Convierte la salida en formato estructurado

---

### 5. ✉️ Generación de borrador
Nodo: Basic LLM Chain  
Crea respuesta profesional automática

---

### 6. 📊 Preparación para revisión
Nodo: Set  

Incluye:
- Borrador generado
- Datos del correo
- Enlaces de aprobación/rechazo

---

### 7. 📤 Envío al responsable
Nodo: Gmail (Send)  

El responsable recibe:
- Contexto del correo
- Respuesta propuesta
- Botones de decisión

---

### 8. ⏸ Espera de decisión
Nodo: Wait  

El flujo se pausa hasta recibir:
- Aprobación
- Rechazo

---

### 9. 🔀 Evaluación de decisión
Nodo: IF  

- Aprobado → continúa
- Rechazado → flujo alternativo

---

### 10. 📬 Respuesta automática
Nodo: Gmail (Reply)  

- Responde en el mismo hilo
- Usa el borrador generado

---

### 11. 🚨 Rechazo
Nodo: Gmail (Send)  

- Notifica revisión manual

---

## 🧠 Buenas prácticas aplicadas

- Uso de IA local (privacidad total)
- Validación humana obligatoria
- Separación por fases del flujo
- Minimización de dependencias entre nodos
- Manejo robusto de errores

---

## 🚀 Beneficios para la empresa

- ⏱️ Reducción del tiempo de respuesta
- 📈 Mejora de productividad
- 🤖 Automatización inteligente
- 👤 Control humano garantizado
- 🔒 Datos privados (sin APIs externas)

---

## 🔮 Mejoras futuras

- Integración con CRM
- Panel interno de aprobación
- Priorización automática avanzada
- Memoria de conversaciones
- Integración con Slack / Teams

---

## ✅ Estado actual

✔ Sistema completamente funcional  
✔ IA local integrada  
✔ Flujo automatizado con aprobación  
✔ Preparado para entorno empresarial  

---

