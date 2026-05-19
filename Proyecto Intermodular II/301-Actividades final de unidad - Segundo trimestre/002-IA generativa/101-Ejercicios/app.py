from flask import Flask, render_template, request, jsonify, send_file
import requests
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__)

# Configuración
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:7b-instruct-q4_0"
DB_NAME = "inmoweb.db"

# Inicializar base de datos
def init_db():
    """Inicializa la base de datos con las tablas necesarias"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo_propiedad TEXT,
            descripcion TEXT,
            precio TEXT,
            ubicacion TEXT,
            caracteristicas TEXT,
            html_generado TEXT NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Inicializar BD al arrancar
init_db()


def call_ollama(prompt: str, system_instruction: str = None) -> str:
    """
    Llama a Ollama local y retorna HTML+CSS generado
    """
    if system_instruction is None:
        system_instruction = """Eres un diseñador web especializado en sitios inmobiliarios.
Crea páginas HTML+CSS profesionales y modernas para el sector inmobiliario.
- Responde SOLO con HTML válido y completo
- Incluye CSS en <style> dentro de <head>
- NO incluyas JavaScript
- Usa colores corporativos: azul (#003d82), dorado (#d4af37), blanco
- Diseño elegante, profesional y confiable
- Incluye secciones típicas: hero, propiedades destacadas, servicios, contacto
- Imágenes placeholder con URLs de unsplash relacionadas con inmuebles"""

    full_prompt = f"""{system_instruction}

Crea: {prompt}"""

    payload = {
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "num_predict": 2048,  # Más tokens para páginas más completas
            "temperature": 0.7,
            "top_p": 0.9
        }
    }

    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=300)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "").strip()
    except Exception as e:
        print(f"Error llamando a Ollama: {e}")
        return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Error - InmoWeb AI</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', sans-serif; 
            background: linear-gradient(135deg, #003d82 0%, #005bb5 100%);
            color: #fff; 
            padding: 3rem; 
            text-align: center;
        }}
        .error {{ 
            background: rgba(255,255,255,0.1); 
            padding: 2rem; 
            border-radius: 1rem;
            backdrop-filter: blur(10px);
        }}
        h1 {{ color: #d4af37; }}
    </style>
</head>
<body>
    <div class="error">
        <h1>⚠️ Error al generar la página</h1>
        <p>No se pudo conectar con la IA generativa.</p>
        <p><small>Detalles técnicos: {e}</small></p>
    </div>
</body>
</html>
        """


@app.route("/")
def index():
    """Página principal"""
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    """Genera una página web usando IA"""
    data = request.get_json(force=True)
    prompt = data.get("prompt", "").strip()
    
    # Parámetros adicionales específicos de inmobiliaria
    tipo_propiedad = data.get("tipo_propiedad", "")
    precio = data.get("precio", "")
    ubicacion = data.get("ubicacion", "")
    caracteristicas = data.get("caracteristicas", "")
    
    if not prompt:
        return jsonify({"error": "El prompt no puede estar vacío"}), 400
    
    # Enriquecer el prompt con los datos adicionales
    prompt_enriquecido = prompt
    if tipo_propiedad:
        prompt_enriquecido += f" Tipo de propiedad: {tipo_propiedad}."
    if precio:
        prompt_enriquecido += f" Rango de precio: {precio}."
    if ubicacion:
        prompt_enriquecido += f" Ubicación: {ubicacion}."
    if caracteristicas:
        prompt_enriquecido += f" Características destacadas: {caracteristicas}."
    
    html = call_ollama(prompt_enriquecido)
    return jsonify({"html": html})


@app.route("/save", methods=["POST"])
def save_proyecto():
    """Guarda un proyecto en la base de datos"""
    data = request.get_json(force=True)
    
    nombre = data.get("nombre", "").strip()
    tipo_propiedad = data.get("tipo_propiedad", "")
    descripcion = data.get("descripcion", "")
    precio = data.get("precio", "")
    ubicacion = data.get("ubicacion", "")
    caracteristicas = data.get("caracteristicas", "")
    html_generado = data.get("html", "")
    
    if not nombre or not html_generado:
        return jsonify({"error": "Nombre y HTML son obligatorios"}), 400
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO proyectos 
            (nombre, tipo_propiedad, descripcion, precio, ubicacion, caracteristicas, html_generado)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, tipo_propiedad, descripcion, precio, ubicacion, caracteristicas, html_generado))
        
        conn.commit()
        proyecto_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            "success": True,
            "message": "Proyecto guardado correctamente",
            "id": proyecto_id
        })
    except Exception as e:
        print(f"Error guardando proyecto: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/proyectos", methods=["GET"])
def listar_proyectos():
    """Lista todos los proyectos guardados"""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, nombre, tipo_propiedad, descripcion, precio, ubicacion, 
                   fecha_creacion
            FROM proyectos
            ORDER BY fecha_creacion DESC
        ''')
        
        proyectos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({"proyectos": proyectos})
    except Exception as e:
        print(f"Error listando proyectos: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/proyecto/<int:proyecto_id>", methods=["GET"])
def obtener_proyecto(proyecto_id):
    """Obtiene un proyecto específico por ID"""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM proyectos WHERE id = ?', (proyecto_id,))
        proyecto = cursor.fetchone()
        conn.close()
        
        if proyecto is None:
            return jsonify({"error": "Proyecto no encontrado"}), 404
        
        return jsonify({"proyecto": dict(proyecto)})
    except Exception as e:
        print(f"Error obteniendo proyecto: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/proyecto/<int:proyecto_id>", methods=["DELETE"])
def eliminar_proyecto(proyecto_id):
    """Elimina un proyecto"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM proyectos WHERE id = ?', (proyecto_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "Proyecto no encontrado"}), 404
        
        conn.close()
        return jsonify({"success": True, "message": "Proyecto eliminado"})
    except Exception as e:
        print(f"Error eliminando proyecto: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/exportar/<int:proyecto_id>")
def exportar_proyecto(proyecto_id):
    """Exporta un proyecto como archivo HTML"""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM proyectos WHERE id = ?', (proyecto_id,))
        proyecto = cursor.fetchone()
        conn.close()
        
        if proyecto is None:
            return jsonify({"error": "Proyecto no encontrado"}), 404
        
        # Crear archivo temporal
        filename = f"{proyecto['nombre'].replace(' ', '_')}.html"
        filepath = os.path.join("/tmp", filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(proyecto['html_generado'])
        
        return send_file(filepath, as_attachment=True, download_name=filename)
    except Exception as e:
        print(f"Error exportando proyecto: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
