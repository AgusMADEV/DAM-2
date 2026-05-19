"""
Sistema de Gestión de Procesos Empresariales - Editor de Nodos
Aplicación Flask para gestión visual de flujos empresariales
"""

from flask import Flask, request, jsonify, render_template
import os
import webbrowser
from threading import Timer
from collections import defaultdict, deque
from typing import Dict, Any, List

from modules import load_backend_modules

app = Flask(__name__, static_folder="static", template_folder="templates")

# Cargar módulos de backend (nodos disponibles)
BACKEND_MODULES = load_backend_modules()


def module_exists(tool_type: str) -> bool:
    """Verifica si existe un módulo frontend para este tipo de nodo"""
    path = os.path.join(app.static_folder, "modules", f"{tool_type}.js")
    return os.path.isfile(path)


@app.route("/")
def index():
    """Página principal del editor"""
    return render_template("index.html")


@app.route("/api/tools", methods=["GET"])
def api_tools():
    """Devuelve la lista de herramientas (nodos) disponibles"""
    tools = []
    for tool_type, mod in BACKEND_MODULES.items():
        tool = dict(mod["TOOL"])
        # Si existe módulo frontend específico, lo enlazamos
        if module_exists(tool_type):
            tool["front_module"] = f"/static/modules/{tool_type}.js"
        tools.append(tool)
    
    # Ordenar herramientas alfabéticamente
    tools.sort(key=lambda x: str(x.get("label", "")).lower())
    
    return jsonify({"tools": tools})


@app.route("/api/execute", methods=["POST"])
def api_execute():
    """
    Ejecuta un grafo de nodos siguiendo las conexiones.
    Recibe: {nodes: [...], edges: [...]}
    Devuelve: {success: bool, logs: [...], error: str}
    """
    try:
        data = request.get_json()
        nodes = data.get("nodes", [])
        edges = data.get("edges", [])
        
        # Logs de ejecución
        logs = []
        
        # Validar que tenemos nodos
        if not nodes:
            return jsonify({
                "success": False,
                "error": "No hay nodos para ejecutar",
                "logs": []
            })
        
        # Construir mapa de nodos por ID
        node_map = {n["id"]: n for n in nodes}
        
        # Construir grafo de adyacencia (de qué nodo sale a qué nodo llega)
        graph = defaultdict(list)
        for edge in edges:
            from_id = edge["from"]
            to_id = edge["to"]
            from_port = edge.get("fromPort", "default")
            graph[from_id].append({"to": to_id, "port": from_port})
        
        # Encontrar nodos de inicio (sin entradas)
        incoming = {n["id"]: 0 for n in nodes}
        for edge in edges:
            incoming[edge["to"]] = incoming.get(edge["to"], 0) + 1
        
        start_nodes = [nid for nid, count in incoming.items() if count == 0]
        
        if not start_nodes:
            return jsonify({
                "success": False,
                "error": "No hay nodos de inicio (todos tienen entradas). Posible ciclo.",
                "logs": logs
            })
        
        # BFS para ejecutar los nodos
        queue = deque(start_nodes)
        visited = set()
        results = {}  # almacena resultados de cada nodo
        
        logs.append(f"🚀 Iniciando ejecución del flujo con {len(nodes)} nodos")
        logs.append(f"📍 Nodos de inicio: {', '.join(start_nodes)}")
        
        while queue:
            node_id = queue.popleft()
            
            if node_id in visited:
                continue
            
            visited.add(node_id)
            node = node_map.get(node_id)
            
            if not node:
                logs.append(f"⚠️ Nodo {node_id} no encontrado")
                continue
            
            node_type = node.get("type")
            config = node.get("config", {})
            
            logs.append(f"\n🔵 Ejecutando: {node_id} ({node_type})")
            
            # Obtener módulo backend
            backend = BACKEND_MODULES.get(node_type)
            if not backend:
                logs.append(f"⚠️ Módulo '{node_type}' no encontrado")
                results[node_id] = {"error": f"Módulo no encontrado: {node_type}"}
                continue
            
            # Preparar contexto de ejecución
            # Los inputs son los resultados de los nodos que llegan a este
            inputs = []
            for edge in edges:
                if edge["to"] == node_id:
                    from_result = results.get(edge["from"], {})
                    value = from_result.get("value")
                    if value is not None:
                        inputs.append(value)
            
            context = {
                "inputs": inputs,
                "node_id": node_id
            }
            
            # Ejecutar el nodo
            try:
                result = backend["execute"](config, context)
                results[node_id] = result
                
                # Mostrar resultado en logs
                if "message" in result:
                    logs.append(f"   💬 {result['message']}")
                if "value" in result:
                    logs.append(f"   ✅ Valor: {result['value']}")
                
            except Exception as e:
                error_msg = f"Error en {node_id}: {str(e)}"
                logs.append(f"   ❌ {error_msg}")
                results[node_id] = {"error": str(e)}
                continue
            
            # Agregar nodos siguientes a la cola
            for next_info in graph.get(node_id, []):
                next_id = next_info["to"]
                if next_id not in visited:
                    queue.append(next_id)
        
        logs.append(f"\n✨ Ejecución completada. {len(visited)} nodos procesados.")
        
        return jsonify({
            "success": True,
            "logs": logs,
            "results": results
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "logs": [f"❌ Error general: {str(e)}"]
        }), 500


def open_browser():
    """Abre el navegador automáticamente"""
    webbrowser.open("http://localhost:5000")


if __name__ == "__main__":
    print("=" * 60)
    print("🏢 Sistema de Gestión de Procesos Empresariales")
    print("=" * 60)
    print("📡 Servidor Flask iniciando...")
    print("🌐 URL: http://localhost:5000")
    print("💡 Presiona Ctrl+C para detener el servidor")
    print("=" * 60)
    
    # Abrir navegador después de 1.5 segundos
    Timer(1.5, open_browser).start()
    
    # Iniciar servidor
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)
