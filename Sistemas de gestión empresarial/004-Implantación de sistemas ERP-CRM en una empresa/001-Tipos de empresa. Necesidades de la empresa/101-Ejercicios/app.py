from flask import Flask, render_template, request
import mysql.connector
import requests

# -------------------------
# CONFIGURACIÓN
# -------------------------

DB_CONFIG = {
    "host": "localhost",
    "user": "empresaia",
    "password": "empresaia",
    "database": "empresaia",
}

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3"  # cambia al modelo que uses

TABLE_SCHEMA = r"""
You have access to a MySQL database called empresaia with this table:

CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    ciudad VARCHAR(50) NOT NULL,
    pais VARCHAR(50) DEFAULT 'España',
    fecha_registro DATE NOT NULL,
    estado_civil ENUM('Soltero', 'Soltera', 'Casado', 'Casada', 'Divorciado', 'Divorciada', 'Viudo', 'Viuda') DEFAULT 'Soltero',
    edad INT,
    INDEX idx_ciudad (ciudad)
);

Only generate SQL queries that are valid for this schema.
"""

SYSTEM_PROMPT = f"""
You are an assistant that converts NATURAL LANGUAGE QUESTIONS into SAFE MySQL SELECT queries.

Rules:
- ONLY return a single MySQL query, nothing else.
- Do NOT include explanations.
- Do NOT use backticks.
- You MUST only use the table 'clientes' described here.
- You MUST NOT modify data: NO INSERT, UPDATE, DELETE, DROP, ALTER, CREATE.
- Use only SELECT queries, possibly with WHERE, ORDER BY, LIMIT, etc.
- Use LIMIT 50 by default if the user does not specify a limit.
- Dates are stored in fecha_registro (DATE).
- Use Spanish values for estado_civil: 'Soltero', 'Soltera', 'Casado', 'Casada', 'Divorciado', 'Divorciada', 'Viudo', 'Viuda'.

Table schema:
{TABLE_SCHEMA}
"""

app = Flask(__name__)


# -------------------------
# HELPERS
# -------------------------

def call_ollama_to_sql(user_query: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query},
        ],
        "stream": False,
    }

    resp = requests.post(OLLAMA_URL, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    content = data.get("message", {}).get("content", "").strip()

    content = content.replace("```sql", "").replace("```", "").strip()
    if ";" in content:
        content = content.split(";")[0] + ";"

    return content


def is_query_safe(sql: str) -> bool:
    sql_lower = sql.strip().lower()
    if not sql_lower.startswith("select"):
        return False

    forbidden = ["insert", "update", "delete", "drop", "alter", "truncate"]
    if any(word in sql_lower for word in forbidden):
        return False

    if "clientes" not in sql_lower:
        return False

    return True


def execute_sql(sql: str):
    conn = mysql.connector.connect(**DB_CONFIG)
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        return columns, rows
    finally:
        conn.close()


def build_results_summary(sql_query, results, error):
    """
    Construye un resumen corto en castellano para que el navegador lo lea en voz alta.
    """
    if error:
        # mensaje corto, neutro
        return "Ha ocurrido un error al ejecutar la consulta."

    if sql_query and not results:
        return "La consulta no devolvió ningún resultado."

    if not results:
        return None

    count = len(results)
    parts = []

    # Parte 1: recuento
    if count == 1:
        parts.append("Se ha encontrado un cliente.")
    else:
        parts.append(f"Se han encontrado {count} clientes.")

    # Parte 2: ejemplos
    ejemplos = []
    for row in results[:3]:
        nombre = (row.get("nombre") or "").strip()
        apellidos = (row.get("apellidos") or "").strip()
        ciudad = row.get("ciudad")
        pieza = ""

        if nombre or apellidos:
            pieza = f"{nombre} {apellidos}".strip()
        else:
            pieza = f"identificador {row.get('id', '')}"

        if ciudad:
            pieza += f" de {ciudad}"

        ejemplos.append(pieza)

    if ejemplos:
        if len(ejemplos) == 1:
            parts.append(f"Por ejemplo: {ejemplos[0]}.")
        else:
            lista = "; ".join(ejemplos)
            parts.append(f"Por ejemplo: {lista}.")

    return " ".join(parts)


# -------------------------
# ROUTES
# -------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    sql_query = None
    results = None
    columns = []
    error = None
    results_summary = None

    if request.method == "POST":
        user_query = request.form.get("user_query", "").strip()
        if not user_query:
            error = "Por favor, escribe una pregunta."
        else:
            try:
                sql_query = call_ollama_to_sql(user_query)

                if not is_query_safe(sql_query):
                    error = "La consulta generada no es segura o no es un SELECT sobre 'clientes'."
                else:
                    columns, results = execute_sql(sql_query)
            except Exception as e:
                error = f"Error: {e}"

    # Resumen para síntesis de voz
    results_summary = build_results_summary(sql_query, results, error)

    # No devolvemos el texto del usuario => textarea vacío tras cada consulta
    return render_template(
        "index.html",
        sql_query=sql_query,
        results=results,
        columns=columns,
        error=error,
        results_summary=results_summary,
    )


if __name__ == "__main__":
    app.run(debug=True)

