En esta actividad he trabajado con un **sistema de gestión de consultas para un blog** que combina bases de datos relacionales y un modelo de lenguaje. El objetivo del ejercicio es automatizar la generación de consultas SQL a partir de preguntas en lenguaje natural, utilizando como base el esquema definido en `blog.sql` y el programa `consulta_blog.py`.

Este trabajo encaja dentro del módulo de **Programación de Servicios y Procesos**, porque pone en práctica:
- la integración con servicios externos (Ollama mediante una llamada HTTP con `curl`),
- el uso de ficheros como fuente de configuración (el esquema SQL),
- y el diseño de un flujo que procesa peticiones del usuario y devuelve una respuesta estructurada.

En un entorno real, este enfoque se puede aplicar para consultar grandes volúmenes de datos sin que el usuario tenga que conocer SQL, algo muy útil en empresas donde distintos departamentos necesitan información rápida sobre contenidos, clientes o métricas internas.

---

El programa `consulta_blog.py` sigue de forma correcta los pasos marcados en el enunciado:

### 🔹 Carga del esquema

Se utiliza la función `cargar_schema_sql(SCHEMA_PATH)`:

- Comprueba si existe el archivo `blog.sql`.
- Lo lee con codificación UTF-8.
- Si el tamaño supera `MAX_SCHEMA_CHARS`, recorta el contenido para no sobrepasar el contexto del modelo.
- Devuelve el texto del esquema para integrarlo en el prompt.

El esquema define dos tablas principales:

```sql
CREATE TABLE `entradas` (
  `Identificador` int NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `fecha` date NOT NULL,
  `contenido` text NOT NULL
);

CREATE TABLE `usuarios` (
  `Identificador` int NOT NULL,
  `usuario` varchar(255) NOT NULL,
  `contrasena` varchar(255) NOT NULL
);
```

Con sus claves primarias y `AUTO_INCREMENT`, lo que proporciona una estructura clara para las consultas.

### 🔹 Construcción del prompt

La función `construir_prompt_completo(schema_sql, pregunta_usuario)`:

- Genera un contexto donde el modelo actúa como **experto en SQL y bases de datos**.
- Incluye:
  - instrucciones concretas (analizar el esquema, responder al usuario, generar SQL dentro de ```sql```, explicar la consulta),
  - el contenido real de `blog.sql`,
  - la pregunta escrita por el usuario.

Si no se carga el esquema, el prompt se ajusta indicando que responda de forma más general.  
Con esto se cumple el requisito de construcción de un **prompt completo, preciso y dependiente del esquema real**.

### 🔹 Ejecución del modelo

La función `ejecutar_modelo_ollama(prompt)`:

- Construye el JSON con:
  - `"model": "qwen2.5:7b-instruct-q4_0"`,
  - `"prompt": prompt`,
  - `"stream": True`.
- Llama a la API de Ollama usando `subprocess.run` con `curl`.
- Lee la salida línea a línea, interpreta cada JSON y concatena los fragmentos `"response"` para formar la respuesta final.
- Maneja posibles errores (timeout, problemas de parseo, excepciones generales).

Este comportamiento demuestra un desarrollo técnico correcto dentro del contexto de **programación de servicios**, utilizando un modelo de lenguaje como backend inteligente.

### 🔹 Procesamiento y presentación

En la función `main()` se organiza todo el flujo:

1. `mostrar_banner()` presenta el título del sistema.
2. Se carga el esquema (`cargar_schema_sql`).
3. Se pide al usuario que introduzca su pregunta sobre el blog.
4. Se construye el prompt (`construir_prompt_completo`).
5. Se envía al modelo (`ejecutar_modelo_ollama`).
6. Se muestra la respuesta final con `mostrar_respuesta(respuesta)`.

Todo está dividido en funciones claras, con mensajes informativos y control de errores básicos, cumpliendo los requisitos del enunciado.

---

```py
"""
import subprocess
import json
import os

# Configuración
SCHEMA_PATH = "blog.sql"
MAX_SCHEMA_CHARS = 200_000
MODELO_OLLAMA = "qwen2.5:7b-instruct-q4_0"
OLLAMA_URL = "http://localhost:11434/api/generate"


def cargar_schema_sql(path):
    """
    Carga el esquema de la base de datos desde el archivo SQL.
    
    Args:
        path (str): Ruta al archivo SQL
        
    Returns:
        str: Contenido del archivo SQL o cadena vacía si no existe
    """
    if not os.path.exists(path):
        print(f"[ERROR] No se encontró el archivo: {path}")
        return ""
    
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            schema = f.read()
        
        # Truncar si es muy largo para evitar exceder el contexto del modelo
        if len(schema) > MAX_SCHEMA_CHARS:
            schema = schema[:MAX_SCHEMA_CHARS] + "\n-- [Truncado para no exceder el contexto]\n"
        
        return schema
    except Exception as e:
        print(f"[ERROR] No se pudo leer el archivo: {e}")
        return ""


def construir_prompt_completo(schema_sql, pregunta_usuario):
    """
    Construye el prompt completo que se enviará al modelo de lenguaje.
    
    Args:
        schema_sql (str): Esquema de la base de datos
        pregunta_usuario (str): Pregunta del usuario
        
    Returns:
        str: Prompt completo con instrucciones, esquema y pregunta
    """
    if schema_sql:
        contexto_sql = (
            "Eres un asistente experto en SQL y bases de datos. "
            "A continuación tienes el esquema completo de una base de datos de blog "
            "extraído del archivo 'blog.sql'.\n\n"
            "Tu tarea es:\n"
            "1. Analizar el esquema proporcionado\n"
            "2. Responder a la pregunta del usuario de forma clara y precisa\n"
            "3. Si la pregunta requiere una consulta SQL, proporcionarla dentro de un bloque ```sql```\n"
            "4. Explicar brevemente qué hace la consulta\n\n"
            "=== ESQUEMA DE LA BASE DE DATOS (blog.sql) ===\n"
            f"{schema_sql}\n"
            "=== FIN DEL ESQUEMA ===\n\n"
        )
    else:
        contexto_sql = (
            "Eres un asistente experto en SQL. "
            "(Advertencia: no se pudo cargar el esquema 'blog.sql', "
            "responde de forma general.)\n\n"
        )
    
    prompt_final = (
        f"{contexto_sql}"
        f"Pregunta del usuario:\n{pregunta_usuario}\n\n"
        f"Por favor, proporciona una respuesta estructurada y profesional."
    )
    
    return prompt_final


def ejecutar_modelo_ollama(prompt):
    """
    Ejecuta una llamada al modelo de lenguaje Ollama.
    
    Args:
        prompt (str): Prompt completo a enviar al modelo
        
    Returns:
        str: Respuesta generada por el modelo
    """
    # Construir el payload JSON para la API de Ollama
    payload = {
        "model": MODELO_OLLAMA,
        "prompt": prompt,
        "stream": True  # Ollama devuelve respuesta en formato JSONL (línea por línea)
    }
    
    try:
        # Ejecutar curl con subprocess
        result = subprocess.run(
            [
                "curl", "-s", OLLAMA_URL,
                "-d", json.dumps(payload)
            ],
            capture_output=True,
            text=True,
            timeout=120  # Timeout de 2 minutos
        )
        
        # Procesar la respuesta JSONL
        response = ""
        lines = result.stdout.splitlines()
        
        for line in lines:
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
                if "response" in obj and obj["response"] is not None:
                    response += obj["response"]
            except json.JSONDecodeError:
                continue
        
        return response.strip()
    
    except subprocess.TimeoutExpired:
        return "[ERROR] Timeout: El modelo tardó demasiado en responder."
    except Exception as e:
        return f"[ERROR] No se pudo ejecutar la consulta: {e}"


def mostrar_banner():
    """Muestra el banner de inicio del programa."""
    print("=" * 70)
    print(" " * 15 + "SISTEMA DE CONSULTAS SQL PARA BLOG")
    print(" " * 20 + "Powered by Ollama + Python")
    print("=" * 70)
    print()


def mostrar_respuesta(respuesta):
    """
    Muestra la respuesta del modelo de forma estructurada.
    
    Args:
        respuesta (str): Respuesta generada por el modelo
    """
    print("\n" + "=" * 70)
    print("RESPUESTA DEL SISTEMA:")
    print("=" * 70)
    print()
    print(respuesta)
    print()
    print("=" * 70)


def main():
    """Función principal del programa."""
    
    # Mostrar banner de inicio
    mostrar_banner()
    
    # Paso 1: Carga del esquema SQL
    print("[1/5] Cargando esquema de la base de datos...")
    schema_sql = cargar_schema_sql(SCHEMA_PATH)
    
    if schema_sql:
        print(f"      ✓ Esquema cargado correctamente ({len(schema_sql)} caracteres)")
    else:
        print("      ✗ No se pudo cargar el esquema")
    print()
    
    # Paso 2: Interacción con el usuario
    print("[2/5] Esperando pregunta del usuario...")
    pregunta_usuario = input("      Introduce tu pregunta sobre el blog: ").strip()
    
    if not pregunta_usuario:
        print("[ERROR] No se proporcionó ninguna pregunta. Saliendo...")
        return
    
    print(f"      ✓ Pregunta recibida: \"{pregunta_usuario}\"")
    print()
    
    # Paso 3: Construcción del prompt
    print("[3/5] Construyendo el prompt para el modelo de lenguaje...")
    prompt_completo = construir_prompt_completo(schema_sql, pregunta_usuario)
    print(f"      ✓ Prompt construido ({len(prompt_completo)} caracteres)")
    print()
    
    # Paso 4: Ejecución del modelo
    print("[4/5] Enviando consulta al modelo Ollama...")
    print(f"      Modelo: {MODELO_OLLAMA}")
    print(f"      URL: {OLLAMA_URL}")
    print("      Esperando respuesta... (esto puede tardar unos segundos)")
    print()
    
    respuesta = ejecutar_modelo_ollama(prompt_completo)
    
    if respuesta.startswith("[ERROR]"):
        print(f"      ✗ {respuesta}")
        return
    else:
        print("      ✓ Respuesta recibida del modelo")
    print()
    
    # Paso 5: Presentación de la respuesta
    print("[5/5] Procesando y presentando la respuesta...")
    mostrar_respuesta(respuesta)
    
    print("\n[✓] Proceso completado exitosamente.")


# Punto de entrada del programa
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Programa interrumpido por el usuario.")
    except Exception as e:
        print(f"\n[ERROR CRÍTICO] {e}")
```

Un ejemplo práctico del funcionamiento sería:

- El programa muestra:
  ```text
  [2/5] Esperando pregunta del usuario...
        Introduce tu pregunta sobre el blog:
  ```
- El usuario escribe, por ejemplo:
  `¿Cuáles son las últimas 5 entradas publicadas en el blog?`

A partir de ahí, el sistema:

1. Usa `blog.sql` para que el modelo sepa que existe la tabla `entradas` con campos `titulo`, `fecha` y `contenido`.
2. Construye un prompt donde se incluye el esquema y la pregunta del usuario.
3. Envía ese prompt a Ollama.
4. Recoge la respuesta del modelo, que puede contener:
   - una propuesta de consulta SQL basada en la tabla `entradas`,
   - una explicación breve de lo que hace esa consulta,
   - y, si procede, una descripción del resultado esperado.

Gracias a este flujo, el usuario puede obtener respuestas avanzadas sobre el contenido del blog **sin escribir manualmente SQL**, lo que demuestra claramente la utilidad práctica del programa en escenarios reales de análisis de datos.

---

Este ejercicio me ha permitido ver cómo se conecta todo lo trabajado en **Programación de Servicios y Procesos**:

- Lectura y uso de ficheros de configuración (`blog.sql`).
- Construcción dinámica de prompts.
- Consumo de un servicio externo (modelo Ollama) desde Python.
- Presentación final de la información de forma legible para el usuario.

En un entorno empresarial, este tipo de solución puede ahorrar mucho tiempo a los equipos que necesitan consultar información constantemente, ya que:
- reduce la dependencia de perfiles técnicos para escribir consultas SQL,
- centraliza el acceso a los datos,
- y permite interactuar con el sistema usando lenguaje natural.

En resumen, este proyecto demuestra cómo la combinación de **bases de datos + modelos de lenguaje + automatización** puede mejorar de forma directa la **eficiencia en la gestión y análisis de datos**, que es uno de los objetivos clave de la unidad y de los sistemas de información modernos.