"""
Módulo de Gestión de Proyectos
Originalmente un programa independiente para gestionar tareas y proyectos
"""

import os
import json
from datetime import datetime

MODULE_INFO = {
    "name": "Gestión de Proyectos",
    "description": "Organiza proyectos, tareas y asignaciones de equipo",
    "icon": "📋",
    "category": "proyectos"
}

def _get_data_file(context):
    """Ruta del archivo de datos"""
    return os.path.join(context["DATA_DIR"], "proyectos.json")

def _load_data(context):
    """Carga los datos del archivo JSON"""
    file_path = _get_data_file(context)
    
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    return {
        "proyectos": [],
        "tareas": []
    }

def _save_data(context, data):
    """Guarda los datos en el archivo JSON"""
    file_path = _get_data_file(context)
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_data(context):
    """Obtiene todos los datos del módulo de proyectos"""
    return _load_data(context)

def execute(context):
    """Ejecuta acciones en el módulo de proyectos"""
    action = context.get("action", "")
    params = context.get("params", {})
    
    data = _load_data(context)
    
    if action == "add_proyecto":
        # Añadir un nuevo proyecto
        proyecto = {
            "id": len(data["proyectos"]) + 1,
            "nombre": params.get("nombre", ""),
            "descripcion": params.get("descripcion", ""),
            "cliente_id": params.get("cliente_id"),  # Vinculación con CRM
            "estado": "planificacion",  # planificacion, en_proceso, completado
            "fecha_inicio": params.get("fecha_inicio", datetime.now().isoformat()),
            "fecha_fin": params.get("fecha_fin"),
            "presupuesto": params.get("presupuesto", 0),
            "responsable": params.get("responsable", "")
        }
        data["proyectos"].append(proyecto)
        _save_data(context, data)
        return {"proyecto": proyecto, "message": "Proyecto creado"}
    
    elif action == "add_tarea":
        # Añadir una nueva tarea a un proyecto
        tarea = {
            "id": len(data["tareas"]) + 1,
            "proyecto_id": params.get("proyecto_id"),
            "titulo": params.get("titulo", ""),
            "descripcion": params.get("descripcion", ""),
            "estado": "pendiente",  # pendiente, en_proceso, completada
            "prioridad": params.get("prioridad", "media"),  # baja, media, alta
            "asignado_a": params.get("asignado_a", ""),
            "fecha_creacion": datetime.now().isoformat(),
            "fecha_vencimiento": params.get("fecha_vencimiento"),
            "tiempo_estimado": params.get("tiempo_estimado", 0),  # en horas
            "tiempo_real": 0
        }
        data["tareas"].append(tarea)
        _save_data(context, data)
        return {"tarea": tarea, "message": "Tarea creada"}
    
    elif action == "update_tarea_estado":
        # Actualizar estado de una tarea
        tarea_id = params.get("id")
        nuevo_estado = params.get("estado")
        
        for tarea in data["tareas"]:
            if tarea["id"] == tarea_id:
                tarea["estado"] = nuevo_estado
                if nuevo_estado == "completada":
                    tarea["fecha_completada"] = datetime.now().isoformat()
                _save_data(context, data)
                return {"tarea": tarea, "message": "Estado actualizado"}
        
        return {"error": "Tarea no encontrada"}
    
    elif action == "registrar_tiempo":
        # Registrar tiempo trabajado en una tarea
        tarea_id = params.get("id")
        horas = params.get("horas", 0)
        
        for tarea in data["tareas"]:
            if tarea["id"] == tarea_id:
                tarea["tiempo_real"] = tarea.get("tiempo_real", 0) + horas
                _save_data(context, data)
                return {"tarea": tarea, "message": f"Registradas {horas} horas"}
        
        return {"error": "Tarea no encontrada"}
    
    elif action == "update_proyecto":
        # Actualizar proyecto
        proyecto_id = params.get("id")
        
        for proyecto in data["proyectos"]:
            if proyecto["id"] == proyecto_id:
                if "nombre" in params:
                    proyecto["nombre"] = params["nombre"]
                if "descripcion" in params:
                    proyecto["descripcion"] = params["descripcion"]
                if "estado" in params:
                    proyecto["estado"] = params["estado"]
                if "presupuesto" in params:
                    proyecto["presupuesto"] = params["presupuesto"]
                if "responsable" in params:
                    proyecto["responsable"] = params["responsable"]
                
                _save_data(context, data)
                return {"proyecto": proyecto, "message": "Proyecto actualizado"}
        
        return {"error": "Proyecto no encontrado"}
    
    elif action == "delete_proyecto":
        # Eliminar proyecto y sus tareas
        proyecto_id = params.get("id")
        
        for i, proyecto in enumerate(data["proyectos"]):
            if proyecto["id"] == proyecto_id:
                # Eliminar tareas relacionadas
                data["tareas"] = [t for t in data["tareas"] if t.get("proyecto_id") != proyecto_id]
                
                # Eliminar proyecto
                deleted = data["proyectos"].pop(i)
                _save_data(context, data)
                return {"proyecto": deleted, "message": "Proyecto y sus tareas eliminados"}
        
        return {"error": "Proyecto no encontrado"}
    
    elif action == "update_tarea":
        # Actualizar tarea completa
        tarea_id = params.get("id")
        
        for tarea in data["tareas"]:
            if tarea["id"] == tarea_id:
                if "titulo" in params:
                    tarea["titulo"] = params["titulo"]
                if "descripcion" in params:
                    tarea["descripcion"] = params["descripcion"]
                if "estado" in params:
                    tarea["estado"] = params["estado"]
                if "prioridad" in params:
                    tarea["prioridad"] = params["prioridad"]
                if "asignado_a" in params:
                    tarea["asignado_a"] = params["asignado_a"]
                
                _save_data(context, data)
                return {"tarea": tarea, "message": "Tarea actualizada"}
        
        return {"error": "Tarea no encontrada"}
    
    elif action == "delete_tarea":
        # Eliminar tarea
        tarea_id = params.get("id")
        
        for i, tarea in enumerate(data["tareas"]):
            if tarea["id"] == tarea_id:
                deleted = data["tareas"].pop(i)
                _save_data(context, data)
                return {"tarea": deleted, "message": "Tarea eliminada"}
        
        return {"error": "Tarea no encontrada"}
    
    else:
        return {"error": f"Acción desconocida: {action}"}

def get_summary(context):
    """Obtiene un resumen para el dashboard"""
    data = _load_data(context)
    
    total_proyectos = len(data["proyectos"])
    proyectos_activos = len([p for p in data["proyectos"] if p.get("estado") in ["planificacion", "en_proceso"]])
    
    total_tareas = len(data["tareas"])
    tareas_pendientes = len([t for t in data["tareas"] if t.get("estado") == "pendiente"])
    tareas_en_proceso = len([t for t in data["tareas"] if t.get("estado") == "en_proceso"])
    tareas_completadas = len([t for t in data["tareas"] if t.get("estado") == "completada"])
    
    # Calcular progreso general
    progreso = 0
    if total_tareas > 0:
        progreso = int((tareas_completadas / total_tareas) * 100)
    
    return {
        "total_proyectos": total_proyectos,
        "proyectos_activos": proyectos_activos,
        "total_tareas": total_tareas,
        "tareas_pendientes": tareas_pendientes,
        "tareas_en_proceso": tareas_en_proceso,
        "tareas_completadas": tareas_completadas,
        "progreso_general": progreso
    }
