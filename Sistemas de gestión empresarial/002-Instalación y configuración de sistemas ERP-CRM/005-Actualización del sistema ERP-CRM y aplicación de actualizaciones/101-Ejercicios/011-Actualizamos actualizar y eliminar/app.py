from flask import Flask, render_template, request, jsonify
from JVDB import JVDB

aplicacion = Flask(__name__)

# Conexión con la base de datos
conexion = JVDB("localhost", "crimson", "crimson", "crimson")

@aplicacion.route("/")
def raiz():
    return render_template("index.html")

# Ruta dinámica: permite seleccionar cualquier tabla
@aplicacion.route("/seleccionar/<tabla>")
def seleccionar(tabla):
    return conexion.seleccionar(tabla)

@aplicacion.route("/tablas")
def tablas():
    return conexion.tablas()

@aplicacion.post("/insertar/<tabla>")
def insertar(tabla):
    try:
        payload = request.get_json(force=True, silent=False)
    except Exception:
        return jsonify({"error": True, "mensaje": "JSON inválido"}), 400

    def _clean_row(d):
        # Convierte '' -> None para que MySQL trate como NULL
        return {k: (None if isinstance(v, str) and v.strip() == "" else v) for k, v in d.items()}

    if isinstance(payload, list):
        datos = [_clean_row(d) for d in payload if isinstance(d, dict)]
    elif isinstance(payload, dict):
        datos = _clean_row(payload)
    else:
        return jsonify({"error": True, "mensaje": "El cuerpo debe ser un objeto o lista de objetos"}), 400

    # `insertar` ya devuelve un JSON (string). Lo devolvemos con el mimetype adecuado.
    res = conexion.insertar(tabla, datos)
    return aplicacion.response_class(res, mimetype="application/json")
# --- add below your existing routes in app.py ---

@aplicacion.put("/actualizar/<tabla>/<pk>")
def actualizar(tabla, pk):
    # Cuerpo: { "col1": "nuevo", "col2": 123, ... }
    try:
        cambios = request.get_json(force=True, silent=False)
    except Exception:
        return jsonify({"error": True, "mensaje": "JSON inválido"}), 400

    if not isinstance(cambios, dict) or not cambios:
        return jsonify({"error": True, "mensaje": "El cuerpo debe ser un objeto con cambios"}), 400

    # '' -> None para NULL en MySQL
    for k, v in list(cambios.items()):
        if isinstance(v, str) and v.strip() == "":
            cambios[k] = None

    res = conexion.actualizar(tabla, pk, cambios)
    return aplicacion.response_class(res, mimetype="application/json")

@aplicacion.delete("/eliminar/<tabla>/<pk>")
def eliminar(tabla, pk):
    res = conexion.eliminar(tabla, pk)
    return aplicacion.response_class(res, mimetype="application/json")

if __name__ == "__main__":
    aplicacion.run(debug=True)

