import os
import re
import json
import requests
import mysql.connector
from functools import lru_cache
from flask import Flask, request, render_template_string, session, redirect, url_for, flash, jsonify
from markdown import markdown  # server-side Markdown → HTML

# ===================== CONFIG =====================
MYSQL_CONFIG = {
    "host": os.environ.get("MYSQL_HOST", "127.0.0.1"),
    "port": int(os.environ.get("MYSQL_PORT", "3306")),
    "user": os.environ.get("MYSQL_USER", "sisi"),
    "password": os.environ.get("MYSQL_PASSWORD", "sisi"),
    "database": os.environ.get("MYSQL_DATABASE", "sisi"),
    "connection_timeout": 5,
}

OLLAMA_BASE = os.environ.get("OLLAMA_BASE", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1:8b-instruct-q4_0")

SCHEMA_PATH = os.environ.get("SCHEMA_PATH", "aplicacion.sql")
MAX_SCHEMA_CHARS = 80_000
DEFAULT_LIMIT = int(os.environ.get("DEFAULT_LIMIT", "200"))
MAX_EXEC_MS = int(os.environ.get("MAX_EXEC_MS", "1500"))
MAX_ANALYSIS_ROWS = int(os.environ.get("MAX_ANALYSIS_ROWS", "50"))
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-secret")

# Behavior
CLEAR_ON_NEW_QUERY = True
ALLOW_DML = os.environ.get("ALLOW_DML", "true").lower() in ("1", "true", "yes", "y")

# Schema strategy: "full" (no trimming) or "compact"
SCHEMA_STRATEGY = os.environ.get("SCHEMA_STRATEGY", "full").lower()  # "full" | "compact"

app = Flask(__name__)
app.secret_key = SECRET_KEY

# ===================== ESQUEMA & CATÁLOGO =====================
CREATE_TBL_RE = re.compile(
    r"CREATE\s+TABLE\s+`?([A-Za-z0-9_]+)`?\s*\((.*?)\)\s*(?:ENGINE|;)",
    re.IGNORECASE | re.DOTALL
)
CREATE_VIEW_RE = re.compile(
    r"CREATE\s+.*?\sVIEW\s+`?([A-Za-z0-9_]+)`?\s+AS\s+(.*?);",
    re.IGNORECASE | re.DOTALL
)

NON_COLUMN_PREFIXES = (
    "PRIMARY KEY", "KEY ", "UNIQUE KEY", "CONSTRAINT", "FOREIGN KEY",
    "INDEX ", "FULLTEXT ", "SPATIAL "
)

def read_schema_raw(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def _clean_cols_block(block: str) -> list[str]:
    cols = []
    for line in block.splitlines():
        line = line.strip().rstrip(",")
        if not line:
            continue
        up = line.upper()
        if up.startswith(NON_COLUMN_PREFIXES):
            continue
        m = re.match(r"`([A-Za-z0-9_]+)`\s+", line)
        if m:
            cols.append(m.group(1))
    return cols

def compact_schema(sql_text: str) -> str:
    """
    Optional compact representation. No column cap anymore.
    """
    out = []
    for m in CREATE_TBL_RE.finditer(sql_text):
        tname = m.group(1)
        cols = _clean_cols_block(m.group(2))
        cols_txt = ", ".join([f"`{c}`" for c in cols])
        out.append(f"TABLE `{tname}` ( {cols_txt} )")
    for m in CREATE_VIEW_RE.finditer(sql_text):
        vname = m.group(1)
        sel = " ".join(m.group(2).split())
        out.append(f"VIEW `{vname}` AS {sel}")
    txt = "\n".join(out)
    if SCHEMA_STRATEGY == "compact" and len(txt) > MAX_SCHEMA_CHARS:
        txt = txt[:MAX_SCHEMA_CHARS] + "\n-- [Truncado]\n"
    return txt

@lru_cache(maxsize=1)
def load_schema_text(path: str) -> str:
    raw = read_schema_raw(path)
    if SCHEMA_STRATEGY == "full":
        return raw
    return compact_schema(raw)

@lru_cache(maxsize=1)
def build_catalog_from_raw(path: str) -> dict:
    """
    Build {table: [col, ...]} from RAW CREATE TABLE blocks. No trimming.
    """
    raw = read_schema_raw(path)
    catalog: dict[str, list[str]] = {}
    for m in CREATE_TBL_RE.finditer(raw):
        tname = m.group(1)
        block = m.group(2)
        cols = _clean_cols_block(block)
        if cols:
            catalog[tname] = cols
    return catalog

# ===================== LLM helpers =====================
SQL_BLOCK_RE = re.compile(r"```sql\s*(.*?)\s*```", re.I | re.S)

def build_prompt(schema_text: str, user_question: str, catalog: dict) -> str:
    catalog_json = json.dumps(catalog, ensure_ascii=False, indent=2)

    guidelines = (
        "Eres un asistente SQL **ESTRICTO** para MySQL.\n"
        "Debes usar ÚNICAMENTE tablas y columnas que aparecen en el **CATÁLOGO**.\n"
        "Reglas OBLIGATORIAS:\n"
        "1) Si una columna o tabla NO está en el catálogo, **no la uses**. No inventes nombres.\n"
        "2) Si hay 2+ tablas en la consulta, cualifica columnas con alias (`t`.`col`). Con 1 tabla, se admite sin alias.\n"
        "3) Evita `SELECT *`. Enumera columnas.\n"
        "4) Usa `LIMIT` en SELECT (salvo COUNT global sin GROUP BY).\n"
        "5) Solo SELECT o DML básicos (INSERT/UPDATE/DELETE). Prohibido DDL, OUTFILE/INFILE y multi-sentencias.\n"
        "6) Si el usuario pide una columna inexistente, **usa solo columnas existentes** del catálogo y explícalo brevemente.\n"
    )

    format_block = (
        "### Formato estricto de respuesta\n"
        "Responde **solo** con:\n"
        "1) 1–2 frases de explicación (máx. 30 palabras)\n"
        "2) Un ÚNICO bloque de SQL dentro de ```sql```\n"
        "Luego escribe ENDSQL en una nueva línea.\n\n"
        "### Ejemplo\n"
        "Explicación: Muestra 10 alumnos por id.\n"
        "```sql\nSELECT `id`, `nombre` FROM `alumnos` ORDER BY `id` DESC LIMIT 10\n```\nENDSQL\n"
    )

    return (
        f"{guidelines}\n\n"
        f"=== CATÁLOGO (tablas → columnas) ===\n{catalog_json}\n=== FIN CATÁLOGO ===\n\n"
        f"=== ESQUEMA SQL (texto completo) ===\n{schema_text}\n=== FIN ESQUEMA ===\n\n"
        f"{format_block}\n"
        f"Instrucción del usuario:\n{user_question}\n"
        "Recuerda: solo columnas/tablas del **CATÁLOGO**."
    )

def build_results_comment_prompt(question: str, sql: str, sql_type: str,
                                 cols: list, rows: list, rowcount: int, limit_rows: int) -> str:
    preview = []
    if rows and cols and sql_type == "select":
        for r in rows[:limit_rows]:
            preview.append([("" if v is None else str(v)) for v in r])

    payload = {
        "question": question,
        "sql": sql,
        "sql_type": sql_type,
        "columns": cols or [],
        "preview_rows": preview,
        "row_count_total": len(rows) if rows else 0,
        "affected": rowcount or 0
    }

    if sql_type == "select":
        task = "Redacta 2–5 viñetas en **Markdown** con observaciones útiles sobre los resultados. Máx. 80 palabras."
    else:
        task = "Redacta 2–4 viñetas en **Markdown** resumiendo la operación DML (alcance, filas afectadas, riesgos). Máx. 60 palabras."

    return f"{task}\n\nContexto:\n{json.dumps(payload, ensure_ascii=False)}"

def call_ollama(prompt: str, temperature=0.1, num_predict=220) -> str:
    r = requests.post(
        f"{OLLAMA_BASE}/api/chat",
        json={
            "model": OLLAMA_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": temperature, "num_predict": num_predict},
        },
        timeout=300,
    )
    if r.status_code != 200:
        try:
            payload = r.json()
        except Exception:
            payload = {"error": r.text}
        raise RuntimeError(
            f"Ollama chat error {r.status_code} — {payload.get('error') or payload} "
            f"(base={OLLAMA_BASE} model={OLLAMA_MODEL})"
        )
    data = r.json()
    return (data.get("message", {}).get("content") or data.get("response") or "").strip()

def extract_sql_from_llm(text: str) -> str:
    m = SQL_BLOCK_RE.search(text)
    if m:
        return m.group(1).strip().rstrip(";")
    for ln in text.splitlines():
        if ln.lower().startswith(("select", "insert", "update", "delete")):
            return ln.strip().rstrip(";")
    return ""

# ===================== SQL helpers & validation =====================
def classify_sql_type(sql: str) -> str:
    s = sql.lower().strip()
    if s.startswith("select"): return "select"
    if s.startswith("insert"): return "insert"
    if s.startswith("update"): return "update"
    if s.startswith("delete"): return "delete"
    return "other"

def is_safe_query(sql: str) -> (bool, str):
    s = f" {sql.lower()} "
    if any(tok in s for tok in (" drop ", " alter ", " truncate ", " outfile ", " infile ")):
        return False, "Operación bloqueada (DDL/OUTFILE/INFILE no permitidos)."
    if ";" in s.strip()[1:-1]:
        return False, "Operación bloqueada (multi-sentencia no permitida)."

    typ = classify_sql_type(sql)
    if typ == "select":
        return True, ""
    if typ in ("insert", "update", "delete"):
        if not ALLOW_DML:
            return False, "DML deshabilitado. Habilítalo con ALLOW_DML=true."
        return True, ""
    return False, "Solo se permiten SELECT o DML básicos (INSERT/UPDATE/DELETE)."

def ensure_limit(sql: str) -> str:
    low = sql.lower()
    if not low.startswith("select"):
        return sql
    if " limit " in low:
        return sql
    if " count(" in low and " group by " not in low:
        return sql
    return f"{sql} LIMIT {DEFAULT_LIMIT}"

def add_max_exec_hint(sql: str) -> str:
    if not sql.lower().startswith("select"):
        return sql
    return re.sub(r"(?is)\A(select\s+)", rf"\1/*+ MAX_EXECUTION_TIME({MAX_EXEC_MS}) */ ", sql, count=1)

def run_query(sql: str):
    typ = classify_sql_type(sql)
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    try:
        cur = conn.cursor()
        if typ == "select":
            cur.execute(f"SET SESSION max_execution_time={MAX_EXEC_MS}")
            final_sql = add_max_exec_hint(ensure_limit(sql))
            cur.execute(final_sql)
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description] if cur.description else []
            return typ, cols, rows, len(rows)
        else:
            cur.execute(sql)
            conn.commit()
            return typ, None, None, cur.rowcount
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()

def validate_sql_against_catalog(sql: str, catalog: dict) -> (bool, str):
    """
    - Ensures referenced tables/columns exist in catalog
    - Bare column ambiguity only when 2+ tables are used
    - Disallows SELECT *
    """
    s = sql.strip().lower()
    if not s.startswith(("select", "insert", "update", "delete")):
        return False, "Solo se permiten SELECT o DML básicos."

    table_pattern = r"(?:from|join|update|into|delete\s+from)\s+`([A-Za-z0-9_]+)`"
    tables = set(re.findall(table_pattern, sql, flags=re.I))
    for t in tables:
        if t not in catalog:
            return False, f"La tabla `{t}` no existe en el catálogo."

    qual_cols = re.findall(r"`([A-Za-z0-9_]+)`\s*\.\s*`([A-Za-z0-9_]+)`", sql)
    for t, c in qual_cols:
        if t not in catalog or c not in catalog[t]:
            return False, f"La columna `{t}`.`{c}` no existe en el catálogo."

    segments = re.findall(r"(?:select|where|group by|order by|set)\s+([^;]+)", sql, flags=re.I)
    bare_cols = []
    for seg in segments:
        bare_cols += re.findall(r"(?:^|[\s,(])`([A-Za-z0-9_]+)`(?:[\s),]|$)", seg)

    multi_table = len(tables) >= 2
    if s.startswith("select") and re.search(r"select\s+\*", sql, flags=re.I):
        return False, "Prohibido `SELECT *`. Enumera columnas."

    qual_only = {c for _, c in qual_cols}
    for c in bare_cols:
        if c in qual_only:
            continue
        owners = [t for t, cols in catalog.items() if c in cols]
        if not owners:
            return False, f"La columna `{c}` no existe en el catálogo."
        if multi_table:
            owners_in_query = set(owners).intersection(tables)
            if len(owners_in_query) >= 2:
                return False, f"Ambigüedad con columna `{c}`. Debe estar cualificada con alias."
    return True, ""

# ===================== UI (claro/profesional) =====================
PAGE = """
<!doctype html><html lang="es"><head>
<meta charset="utf-8"><title>jocarsa | neurocontrolador</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{margin:0;background:#f7f8fb;font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;color:#1f2937}
.wrap{max-width:1100px;margin:0 auto;padding:24px 24px 120px}
header{background:#fff;border:1px solid #e6e8f0;border-radius:14px;padding:16px 18px;box-shadow:0 6px 20px rgba(16,24,40,.08)}
h1{margin:0 0 6px;font-size:20px}
.sub{color:#5b6472;font-size:14px}
.pill{padding:6px 10px;font-size:12px;border:1px solid #e6e8f0;border-radius:999px;background:#fafbff;margin-right:6px}
.pane{margin-top:16px;background:#fff;border:1px solid #e6e8f0;border-radius:14px;box-shadow:0 6px 20px rgba(16,24,40,.08);padding:14px}
.insights{background:#f8fafc;border:1px solid #e6e8f0;padding:12px;border-radius:10px}
.insights h3{margin:0 0 8px;font-size:14px;color:#0f3f9c}
table{width:100%;border-collapse:collapse;font-size:14px;margin-top:10px}
th,td{border:1px solid #e6e8f0;padding:8px 10px;text-align:left;background:#fff}
tbody tr:nth-child(odd) td{background:#fcfcfe}
.flash{background:#fff7ed;border:1px solid #fed7aa;color:#9a3412;padding:10px 12px;border-radius:10px;margin:8px 0}
.error{background:#fef2f2;border-color:#fecaca;color:#b91c1c}
.dock{position:fixed;bottom:0;left:0;right:0;background:rgba(255,255,255,.9);backdrop-filter:blur(6px);border-top:1px solid #e6e8f0}
.dock-inner{max-width:1100px;margin:0 auto;padding:12px 24px;display:flex;gap:10px}
input[type=text]{flex:1;padding:12px 14px;background:#fff;border:1px solid #e6e8f0;border-radius:10px}
button{padding:12px 14px;border-radius:10px;border:1px solid #1f6feb26;color:#fff;background:linear-gradient(180deg,#1f6feb,#1a61d0);cursor:pointer;font-weight:600}
a{color:#1f6feb;text-decoration:none}
a:hover{text-decoration:underline}
.meta{color:#5b6472;font-size:12px;margin-top:6px}
</style>
</head><body>
<div class="wrap">
  <header>
    <h1>jocarsa | neurocontrolador</h1>
    <div class="sub">Comentario en Markdown (server-side) · Resultados arriba · Consulta abajo</div>
    <div>
      <span class="pill">BD: {{db}}</span>
      <span class="pill">Modelo: {{model}}</span>
      <span class="pill">Límite SELECT: {{dlimit}}</span>
      <span class="pill">Max {{ms}} ms</span>
      <span class="pill"><a href="{{url_for('health')}}">/health</a></span>
    </div>
  </header>

  {% with messages = get_flashed_messages() %}
    {% if messages %}
      {% for m in messages %}
        <div class="pane flash">{{ m }}</div>
      {% endfor %}
    {% endif %}
  {% endwith %}

  {% if history %}
    {% for t in history %}
      <div class="pane">
        <div><strong>{{ t.title }}</strong></div>
        <div class="meta" style="margin-bottom:8px">{{ t.subtitle }}</div>

        {% if t.commentary_html %}
          <div class="insights">
            <h3>Comentario</h3>
            {{ t.commentary_html|safe }}
          </div>
        {% endif %}

        {% if t.show_table %}
          <div style="max-height:520px;overflow:auto;border-radius:10px;margin-top:10px">
            <table>
              <thead>
                <tr>{% for c in t.cols %}<th>{{ c }}</th>{% endfor %}</tr>
              </thead>
              <tbody>
                {% for r in t.rows %}
                  <tr>{% for cell in r %}<td>{{ cell }}</td>{% endfor %}</tr>
                {% endfor %}
                {% if not t.rows %}
                  <tr><td colspan="{{ t.cols|length }}">(Sin filas)</td></tr>
                {% endif %}
              </tbody>
            </table>
          </div>
        {% endif %}

        {% if t.error %}
          <div class="flash error" style="margin-top:10px">{{ t.error }}</div>
        {% endif %}
      </div>
    {% endfor %}
  {% endif %}
</div>

<div class="dock">
  <form class="dock-inner" method="post" action="{{ url_for('chat') }}">
    <input type="text" name="q" placeholder="Escribe tu consulta o instrucción SQL (SELECT, INSERT, UPDATE, DELETE)…" required>
    <button type="submit">Ejecutar</button>
  </form>
</div>
</body></html>
"""

# ===================== Routes =====================
@app.route("/", methods=["GET"])
def index():
    session.setdefault("history", [])
    return render_template_string(
        PAGE,
        history=session["history"],
        model=OLLAMA_MODEL,
        dlimit=DEFAULT_LIMIT,
        ms=MAX_EXEC_MS,
        db=MYSQL_CONFIG["database"],
    )

@app.route("/", methods=["POST"])
def chat():
    q = request.form.get("q", "").strip()
    if not q:
        flash("Escribe una consulta o instrucción SQL.")
        return redirect(url_for("index"))

    # Mostrar solo el resultado actual
    if CLEAR_ON_NEW_QUERY:
        session["history"] = []
    else:
        session.setdefault("history", [])

    # Cargar esquema (full o compacto) y catálogo desde RAW
    schema_text = load_schema_text(SCHEMA_PATH)
    catalog = build_catalog_from_raw(SCHEMA_PATH)

    # 1) Generar SQL (único bloque) con prompt estricto
    try:
        llm_text = call_ollama(build_prompt(schema_text, q, catalog), temperature=0.05, num_predict=200)
    except Exception as e:
        session["history"].append({
            "title": "Error al generar SQL",
            "subtitle": q,
            "commentary_html": None,
            "show_table": False,
            "cols": None,
            "rows": None,
            "error": str(e),
        })
        session.modified = True
        return redirect(url_for("index"))

    sql = extract_sql_from_llm(llm_text)
    if not sql:
        session["history"].append({
            "title": "No se pudo extraer SQL",
            "subtitle": q,
            "commentary_html": None,
            "show_table": False,
            "cols": None,
            "rows": None,
            "error": "La respuesta del modelo no contenía un bloque SQL válido.",
        })
        session.modified = True
        return redirect(url_for("index"))

    # 1.b) Validación contra catálogo (con regla de ambigüedad multi-tabla)
    ok_catalog, why_catalog = validate_sql_against_catalog(sql, catalog)
    if not ok_catalog:
        session["history"].append({
            "title": "Consulta bloqueada por catálogo",
            "subtitle": sql,
            "commentary_html": None,
            "show_table": False,
            "cols": None,
            "rows": None,
            "error": why_catalog,
        })
        session.modified = True
        return redirect(url_for("index"))

    # 2) Reglas de seguridad generales
    ok, why = is_safe_query(sql)
    if not ok:
        session["history"].append({
            "title": "Consulta bloqueada por seguridad",
            "subtitle": sql,
            "commentary_html": None,
            "show_table": False,
            "cols": None,
            "rows": None,
            "error": why,
        })
        session.modified = True
        return redirect(url_for("index"))

    # 3) Ejecutar SQL
    try:
        typ, cols, rows, rowcount = run_query(sql)
        final_sql = add_max_exec_hint(ensure_limit(sql)) if typ == "select" else sql

        # 4) Generar comentario (Markdown → HTML)
        try:
            comment_prompt = build_results_comment_prompt(q, final_sql, typ, cols, rows, rowcount, MAX_ANALYSIS_ROWS)
            comment_md = call_ollama(comment_prompt, temperature=0.2, num_predict=220)
            comment_html = markdown(comment_md, extensions=["fenced_code", "tables"])
        except Exception as e2:
            comment_html = f"<p><em>No se pudo generar el comentario: {str(e2)}</em></p>"

        # 5) Preparar tarjeta
        if typ == "select":
            title = "Resultados de la consulta"
            subtitle = f"{len(rows)} fila{'s' if len(rows)!=1 else ''} · SELECT con límite y tiempo máximo aplicados"
            show_table = True
        elif typ == "insert":
            title = "Inserción realizada"
            subtitle = f"{rowcount} fila{'s' if rowcount!=1 else ''} insertada(s)"
            show_table = False
        elif typ == "update":
            title = "Actualización realizada"
            subtitle = f"{rowcount} fila{'s' if rowcount!=1 else ''} actualizada(s)"
            show_table = False
        elif typ == "delete":
            title = "Borrado realizado"
            subtitle = f"{rowcount} fila{'s' if rowcount!=1 else ''} borrada(s)"
            show_table = False
        else:
            title = "Operación completada"
            subtitle = q
            show_table = bool(cols)

        session["history"].append({
            "title": title,
            "subtitle": subtitle,
            "commentary_html": comment_html,
            "show_table": show_table,
            "cols": cols if show_table else None,
            "rows": rows if show_table else None,
            "error": None,
        })

    except Exception as e:
        session["history"].append({
            "title": "Error al ejecutar SQL",
            "subtitle": sql,
            "commentary_html": None,
            "show_table": False,
            "cols": None,
            "rows": None,
            "error": str(e),
        })

    session.modified = True
    return redirect(url_for("index"))

@app.route("/health")
def health():
    info = {"ollama_base": OLLAMA_BASE, "model": OLLAMA_MODEL, "schema_path": SCHEMA_PATH, "allow_dml": ALLOW_DML, "strategy": SCHEMA_STRATEGY}
    try:
        v = requests.get(f"{OLLAMA_BASE}/api/version", timeout=3).json()
        info["ollama_version"] = v.get("version")
    except Exception as e:
        info["ollama_version_error"] = str(e)
    try:
        tags = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=5).json()
        info["available_models"] = [m.get("model") for m in tags.get("models", [])]
    except Exception as e:
        info["available_models_error"] = str(e)
    return jsonify(info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

