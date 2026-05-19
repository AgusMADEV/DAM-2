# GastroBotChef — Entrenamiento de IA personalizada

**Proyecto:** GastroBotChef  
**Temática:** Gastronomía española (recetas, técnicas, denominaciones de origen)  
**Modelo base:** Qwen2.5-0.5B-Instruct  
**Técnica de entrenamiento:** Fine-tuning con LoRA / QLoRA  

---

## Descripción

GastroBotChef es un asistente de inteligencia artificial entrenado para responder preguntas sobre gastronomía española. Partiendo del modelo `Qwen2.5-0.5B-Instruct` (el mismo utilizado en clase), se ha realizado un *fine-tuning* con LoRA usando un dataset personalizado de 23 pares pregunta-respuesta sobre cocina española.

La actividad demuestra el diferencial **antes/después** del entrenamiento: el modelo base responde de forma genérica, mientras que el modelo fine-tuned responde con precisión y detalle sobre temas específicos como el pil-pil, el sofrito, las D.O.P., etc.

---

## Estructura de ficheros

| Fichero | Descripción |
|---|---|
| `training_data.jsonl` | Dataset personalizado: 23 Q&A sobre gastronomía española |
| `entrenar.py` | Script de fine-tuning con LoRA/QLoRA + guardado de métricas en JSON |
| `probar.py` | Comparativa **antes/después**: mismo prompt en modelo base y fine-tuned |
| `interfaz.py` | Chat interactivo con historial, comandos especiales y exportación |
| `gastrobot-chef-model/` | Carpeta generada al entrenar (adaptadores LoRA) |
| `gastrobot_metricas.json` | Métricas de entrenamiento (loss por paso) — generado al entrenar |
| `comparativa_antes_despues.json` | Resultados exportados por `probar.py` |

---

## Pasos para ejecutar el proyecto

### 1. Instalar dependencias

```bash
pip install torch transformers datasets peft bitsandbytes accelerate
```

### 2. Entrenar el modelo

```bash
python entrenar.py
```

Genera el adaptador LoRA en `./gastrobot-chef-model/` y las métricas en `gastrobot_metricas.json`.

### 3. Comparativa antes/después

```bash
python probar.py
```

Lanza las mismas preguntas contra el modelo base y el fine-tuned. Exporta los resultados a `comparativa_antes_despues.json`.

### 4. Interfaz conversacional

```bash
python interfaz.py
```

Comandos disponibles dentro del chat:

| Comando | Acción |
|---|---|
| `/ayuda` | Muestra la lista de comandos |
| `/historial` | Imprime el historial de la sesión |
| `/limpiar` | Reinicia el historial |
| `/exportar` | Guarda el historial en JSON |
| `/salir` | Cierra la interfaz |

---

## Modificaciones respecto al ejercicio de clase

### Modificaciones estéticas y visuales
- **Colores ANSI** en todos los scripts: verde para respuestas del chef, azul para el usuario, magenta para banners, amarillo para advertencias.
- **Banners ASCII** al inicio de cada script.
- **Tiempo de respuesta** y número de tokens mostrados tras cada generación.

### Modificaciones funcionales
- **Dataset propio** sobre gastronomía española (23 ejemplos) en lugar del dataset sobre Jose Vicente.
- **`GuardarMetricasCallback`**: callback personalizado del Trainer que registra la pérdida (loss), el learning rate y el tiempo de cada paso y los guarda automáticamente en `gastrobot_metricas.json`.
- **Modo comparativa** (`probar.py`): carga los dos modelos simultáneamente y ejecuta las mismas preguntas en ambos, exportando los resultados comparativos a JSON para documentación.
- **Historial de conversación** (`interfaz.py`): la interfaz mantiene el contexto de la conversación en memoria, pasando el historial completo al modelo en cada turno (multi-turn).
- **Exportación del historial** a JSON con marca de tiempo desde dentro del chat con `/exportar`.
- **Comandos especiales** dentro del chat interactivo.

---

## Dataset: temática de gastronomía española

El fichero `training_data.jsonl` contiene 23 pares Q&A sobre:

- Platos icónicos: paella valenciana, tortilla española, gazpacho, salmorejo, cocido madrileño, pulpo a la gallega
- Técnicas culinarias: sofrito, pil-pil, escabeche, confitado
- Productos con D.O.P./I.G.P.: jamón ibérico, pimentón de La Vera, queso Manchego, Cabrales, turrón de Jijona
- Bebidas y repostería: vinos (Rioja, Ribera del Duero, Rías Baixas), sangría, crema catalana, arroz con leche
- Cultura gastronómica: dieta mediterránea, nueva cocina vasca, tapas, pintxos

---

## Relación con los conceptos vistos en clase

| Concepto (clase) | Aplicación en GastroBotChef |
|---|---|
| Carga de modelos pre-entrenados desde Hugging Face | `AutoModelForCausalLM.from_pretrained(MODEL_NAME)` |
| Tokenización y preparación de datos | `tokenize_fn` + `apply_chat_template` |
| Fine-tuning con LoRA | `LoraConfig` + `get_peft_model` + `Trainer` |
| QLoRA 4-bit en GPU | `load_in_4bit=True` + `bnb_4bit_*` |
| Generación de texto controlada | `temperature`, `top_p`, `max_new_tokens` |
| Gestión de dispositivos (GPU/CPU) | `detectar_dispositivo()` en todos los scripts |
| Plantilla de chat de Qwen | `apply_chat_template` con mensajes system/user/assistant |
