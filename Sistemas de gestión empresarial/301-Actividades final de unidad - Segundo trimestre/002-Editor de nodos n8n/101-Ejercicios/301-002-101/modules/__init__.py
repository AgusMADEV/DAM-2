"""
Cargador de módulos backend para el sistema de nodos
"""

import os
import importlib


def load_backend_modules():
    """
    Carga dinámicamente todos los módulos Python de la carpeta modules/
    que tengan definida la estructura TOOL y la función execute().
    
    Returns:
        dict: {type: {TOOL: {...}, execute: function}}
    """
    modules = {}
    modules_dir = os.path.dirname(__file__)
    
    for filename in os.listdir(modules_dir):
        # Solo archivos .py que no sean __init__
        if not filename.endswith(".py") or filename.startswith("__"):
            continue
        
        module_name = filename[:-3]  # quitar .py
        
        try:
            # Importar módulo dinámicamente
            mod = importlib.import_module(f"modules.{module_name}")
            
            # Verificar que tenga TOOL y execute
            if hasattr(mod, "TOOL") and hasattr(mod, "execute"):
                tool_type = mod.TOOL.get("type", module_name)
                modules[tool_type] = {
                    "TOOL": mod.TOOL,
                    "execute": mod.execute
                }
                print(f"✅ Módulo cargado: {tool_type}")
            else:
                print(f"⚠️ Módulo {module_name} no tiene TOOL o execute")
                
        except Exception as e:
            print(f"❌ Error cargando módulo {module_name}: {e}")
    
    print(f"\n📦 Total de módulos cargados: {len(modules)}\n")
    return modules
