# app.py
from flask import Flask, render_template, request, Response, jsonify
import mysql.connector, json
from JVDB import JVDB

# ---------- CONFIG ----------
MYSQL_HOST = "localhost"
MYSQL_USER = "tiendaonline"
MYSQL_PASS = "tiendaonline"
MYSQL_DB   = "tiendaonline"

app = Flask(__name__, template_folder="templates", static_folder="static")

# ---------- DB ----------
jvdb = JVDB(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB)

def json_resp(obj, status=200):
    body = json.dumps(obj, ensure_ascii=False, indent=2, default=jvdb._json_default)
    return Response(body, status=status, mimetype="application/json; charset=utf-8")

# ---------- FK UTILITIES ----------
def fk_metadata(tabla):
    sql = """
    SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
    FROM information_schema.KEY_COLUMN_USAGE
    WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND REFERENCED_TABLE_NAME IS NOT NULL
    """
    jvdb.cursor.execute(sql, (jvdb.basedatos, tabla))
    rows = jvdb.cursor.fetchall()
    fks = []
    for col, ref_table, ref_col in rows:
        jvdb.cursor.execute(f"DESCRIBE `{ref_table}`")
        desc = jvdb.cursor.fetchall()
        cols = [d[0] for d in desc]
        types = {d[0]: d[1].lower() for d in desc}
        label = next((c for c in ("nombre","name","titulo","title","descripcion","description") if c in cols), None)
        if not label:
            label = next((c for c in cols if "char" in types.get(c,"") or "text" in types.get(c,"")), ref_col)
        fks.append({"col": col, "ref_table": ref_table, "ref_column": ref_col, "label_column": label})
    return fks

def fk_maps_for_table(tabla, rows, fks):
    maps = {}
    for fk in fks:
        col = fk["col"]
        ids = sorted({r.get(col) for r in rows if r.get(col) is not None})
        if not ids:
            maps[col] = {}
            continue
        ref_table, ref_col, lab = fk["ref_table"], fk["ref_column"], fk["label_column"]
        placeholders = ", ".join(["%s"] * len(ids))
        sql = f"SELECT `{ref_col}`, `{lab}` FROM `{ref_table}` WHERE `{ref_col}` IN ({placeholders})"
        jvdb.cursor.execute(sql, tuple(ids))
        maps[col] = {rid: lbl for (rid, lbl) in jvdb.cursor.fetchall()}
    return maps

def fk_options_for_table(tabla, fks):
    out = {}
    for fk in fks:
        ref_table, ref_col, lab = fk["ref_table"], fk["ref_column"], fk["label_column"]
        jvdb.cursor.execute(f"SELECT `{ref_col}`, `{lab}` FROM `{ref_table}` ORDER BY `{lab}` ASC")
        out[fk["col"]] = [{"value": rid, "label": lbl} for (rid, lbl) in jvdb.cursor.fetchall()]
    return out

# ---------- FRONTEND ----------
@app.route("/")
def index():
    # Render templates/index.html
    return render_template("index.html")

@app.route("/favicon.ico")
def favicon():
    return ("", 204)

@app.route("/health")
def health():
    return Response("OK", mimetype="text/plain")

# ---------- API ----------
@app.route("/tablas")
def tablas():
    try:
        jvdb.cursor.execute("SHOW TABLES")
        data = [{"tabla": r[0]} for r in jvdb.cursor.fetchall()]
        return json_resp(data)
    except mysql.connector.Error as e:
        return json_resp({"error": True, "mensaje": str(e)}, status=500)

@app.route("/seleccionar/<tabla>")
def seleccionar(tabla):
    try:
        jvdb.cursor.execute(f"SELECT * FROM `{tabla}`")
        cols = jvdb.cursor.column_names
        filas = jvdb.cursor.fetchall()
        data = [dict(zip(cols, fila)) for fila in filas]
        return json_resp(data)
    except mysql.connector.Error as e:
        return json_resp({"error": True, "mensaje": str(e)}, status=500)

@app.route("/seleccionar_humano/<tabla>")
def seleccionar_humano(tabla):
    try:
        jvdb.cursor.execute(f"SELECT * FROM `{tabla}`")
        cols = jvdb.cursor.column_names
        filas = jvdb.cursor.fetchall()
        rows = [dict(zip(cols, fila)) for fila in filas]
        pk = jvdb._pk_column(tabla) or ("id" if "id" in cols else cols[0])
        fks = fk_metadata(tabla)
        maps = fk_maps_for_table(tabla, rows, fks)
        for r in rows:
            for fk in fks:
                c = fk["col"]
                if c in r and r[c] is not None:
                    r[c + "__label"] = maps.get(c, {}).get(r[c])
        return json_resp({"rows": rows, "meta": {"pk": pk, "fks": fks}})
    except mysql.connector.Error as e:
        return json_resp({"error": True, "mensaje": str(e)}, status=500)

@app.route("/fk_options/<tabla>")
def fk_options(tabla):
    try:
        fks = fk_metadata(tabla)
        opts = fk_options_for_table(tabla, fks)
        return json_resp(opts)
    except mysql.connector.Error as e:
        return json_resp({"error": True, "mensaje": str(e)}, status=500)

@app.post("/insertar/<tabla>")
def insertar(tabla):
    try:
        payload = request.get_json(force=True)
        res_json = jvdb.insertar(tabla, payload)
        return Response(res_json, mimetype="application/json; charset=utf-8")
    except Exception as e:
        return json_resp({"error": True, "mensaje": str(e)}, status=500)

@app.put("/actualizar/<tabla>/<pk>")
def actualizar(tabla, pk):
    try:
        cambios = request.get_json(force=True)
        cambios = {k: (None if (isinstance(v, str) and v.strip() == "") else v) for k, v in cambios.items()}
        res_json = jvdb.actualizar(tabla, pk, cambios)
        return Response(res_json, mimetype="application/json; charset=utf-8")
    except Exception as e:
        return json_resp({"error": True, "mensaje": str(e)}, status=500)

@app.delete("/eliminar/<tabla>/<pk>")
def eliminar(tabla, pk):
    try:
        res_json = jvdb.eliminar(tabla, pk)
        return Response(res_json, mimetype="application/json; charset=utf-8")
    except Exception as e:
        return json_resp({"error": True, "mensaje": str(e)}, status=500)

# ---------- ERROR HANDLERS ----------
@app.errorhandler(Exception)
def handle_any(e):
    return json_resp({"error": True, "mensaje": str(e)}, status=500)

# ---------- MAIN ----------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

