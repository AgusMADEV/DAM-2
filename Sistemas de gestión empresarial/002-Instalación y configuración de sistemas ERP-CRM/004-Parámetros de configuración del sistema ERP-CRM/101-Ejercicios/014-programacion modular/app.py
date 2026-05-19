from flask import Flask, request, jsonify, render_template
import os, webbrowser
from threading import Timer

# === Carga dinámica de módulos backend ===
from modules import load_backend_modules  # nuestra factoría

app = Flask(__name__, static_folder="static", template_folder="templates")

BASE_DIR = os.path.abspath(os.getenv("BASE_DIR", os.getcwd()))
BACKEND_MODULES = load_backend_modules()  # dict: type -> {TOOL, execute}

def static_front_module_exists(tool_type: str) -> bool:
    path = os.path.join(app.static_folder, "modules", f"{tool_type}.js")
    return os.path.isfile(path)

@app.route("/")
def index():
    return render_template("index.html", base_dir=BASE_DIR)

@app.route("/api/tools", methods=["GET"])
def api_tools():
    """
    Devuelve la lista de tools detectados con su schema y, si existe,
    la ruta del front-module JS correspondiente.
    """
    tools = []
    for t, mod in BACKEND_MODULES.items():
        tool = dict(mod["TOOL"])  # copia
        # Añadir ruta del front-module si existe
        if static_front_module_exists(t):
            tool["front_module"] = f"/static/modules/{t}.js"
        tools.append(tool)

    return jsonify({"tools": tools, "base_dir": BASE_DIR})

def safe_join(base, target):
    final_path = os.path.abspath(os.path.join(base, target))
    if not final_path.startswith(base):
        raise ValueError("Path escapes BASE_DIR")
    return final_path

@app.route("/api/execute", methods=["POST"])
def api_execute():
    """
    Ejecuta cada nodo por su 'type' despachando al módulo backend correspondiente.
    Payload:
      { nodes:[{id,type,config}], edges:[...] }
    """
    payload = request.get_json(silent=True) or {}
    nodes = payload.get("nodes", [])
    results = {}

    for node in nodes:
        nid = node.get("id")
        ntype = node.get("type")
        config = node.get("config", {})

        try:
            mod = BACKEND_MODULES.get(ntype)
            if not mod:
                raise RuntimeError(f"Unknown node type: {ntype}")

            # Algunas utilidades comunes que los módulos pueden querer (p.ej. BASE_DIR)
            context = {
                "BASE_DIR": BASE_DIR,
                "safe_join": safe_join,
            }
            out = mod["execute"](config, context)
            results[nid] = {"ok": True, "data": out, "error": None}
        except Exception as e:
            results[nid] = {"ok": False, "data": None, "error": str(e)}

    return jsonify({"results": results})

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    Timer(0.75, open_browser).start()
    app.run(debug=True)

