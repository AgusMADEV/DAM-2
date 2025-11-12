"""
Sistema de Gestión de Consultas SQL para Blog
==============================================

Este programa permite realizar consultas sobre una base de datos de blog
utilizando un modelo de lenguaje (Ollama) para generar SQL dinámicamente.
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
