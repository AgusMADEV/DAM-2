En este trabajo he realizado un **análisis comparativo de varios motores LLM (Large Language Models)** usando **Ollama**, con el objetivo de elegir el más adecuado para mi **Proyecto Intermodular**.  
Mi proyecto busca desarrollar una solución empresarial que integre un **widget web** con conexión a la **API de WhatsApp**, por lo que necesito un modelo que sea rápido, preciso y que maneje bien el idioma español.  

He querido enfocar el análisis desde un punto de vista práctico, tal como lo haría en un entorno de desarrollo real. Cada fase del proceso (descarga, pruebas, evaluación y conclusiones) está pensada para obtener resultados claros y medibles que me ayuden a tomar una decisión técnica fundamentada.

---

He seguido un proceso organizado en varias fases, desde la **instalación de modelos** hasta la **recogida de resultados**.  

### Pasos principales:
1. **Descarga e instalación de modelos** con `ollama pull`. Probé los siguientes:
   ```bash
   ollama pull llama2:7b
   ollama pull mistral:7b
   ollama pull codellama:7b
   ollama pull vicuna:7b
   ollama pull orca-mini:3b
   ```
   Elegí estos modelos porque cubren distintos enfoques: generalistas, especializados en código, conversacionales y ligeros.

2. **Preparación de la batería de tests**, con 50 preguntas distribuidas en 4 áreas empresariales:
   - Atención al cliente  
   - Ventas y marketing  
   - Soporte técnico  
   - Gestión empresarial  
   Además, las clasifiqué en tres niveles de dificultad: básico, intermedio y avanzado.

3. **Automatización de las pruebas** con un script en Python que ejecuta cada modelo y guarda las respuestas:
   ```python
   result = subprocess.run(['ollama', 'run', model_name, question], capture_output=True, text=True)
   ```
   Esto me permitió medir los tiempos y resultados de forma uniforme para todos los modelos.

4. **Evaluación de resultados** mediante una tabla de criterios donde valoré:
   - Precisión  
   - Relevancia  
   - Claridad  
   - Tiempo de respuesta  
   - Capacidad de uso en español  

Este proceso me ayudó a aplicar los conocimientos de **evaluación técnica y automatización de procesos** que vimos en clase.

---

Para aplicar todo de forma realista, diseñé una **batería de pruebas empresariales** centrada en una **empresa tecnológica ficticia (Empresa X)**, especializada en desarrollo web y apps móviles.  

### Ejemplos de preguntas:
- **Básico:** “¿Qué servicios ofrece la empresa?”  
- **Intermedio:** “¿Qué tecnologías utilizan para el desarrollo backend?”  
- **Avanzado:** “¿Cómo manejan la escalabilidad en aplicaciones con alta concurrencia?”

Cada modelo respondió a las mismas preguntas y analicé los resultados generando una estructura de datos como esta:
```python
resultados = {
    'modelo': 'nombre_modelo',
    'categoria': 'categoria_pregunta',
    'pregunta': 'texto_pregunta',
    'respuesta': 'texto_respuesta',
    'tiempo_respuesta': 0.0,
    'puntuacion_precision': 0,
    'puntuacion_relevancia': 0,
    'puntuacion_claridad': 0
}
```

Esto me permitió medir de forma objetiva las diferencias entre los modelos y obtener conclusiones basadas en datos.  
Un error común que evité fue depender solo de la percepción subjetiva; en su lugar, usé puntuaciones y métricas claras.  
También aprendí a **balancear recursos**: por ejemplo, modelos más ligeros como *Orca Mini* eran más rápidos, pero menos precisos en español.

---

Este análisis me ayudó a entender mejor cómo **evaluar modelos de lenguaje desde una perspectiva técnica y práctica**.  
Pude comprobar que cada modelo tiene sus fortalezas y debilidades, y que la elección final debe depender del **contexto del proyecto**.

Gracias a esta práctica:
- Mejoré mis habilidades de **automatización con Python**.  
- Apliqué **conceptos de benchmarking y evaluación técnica**.  
- Entendí cómo integrar herramientas de IA en proyectos empresariales reales.

En resumen, este trabajo me permitió **conectar la teoría con la práctica**, y los resultados que obtuve me servirán para tomar una decisión sólida al integrar el motor LLM más adecuado en el **Proyecto Intermodular**.