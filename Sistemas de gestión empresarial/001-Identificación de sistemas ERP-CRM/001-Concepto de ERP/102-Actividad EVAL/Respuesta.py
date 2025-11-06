# ============================================
# MÓDULO DE RECURSOS HUMANOS - SISTEMA ERP
# ============================================

# 1. DEFINICIÓN DEL MÓDULO
nombre_modulo = "Gestión de Recursos Humanos"

print("=" * 50)
print(f"MÓDULO: {nombre_modulo}")
print("=" * 50)
print()

# 2. FUNCIONALIDADES DEL MÓDULO RH
funciones_rh = {
    "Gestión de empleados": "Administración completa de la información de los empleados",
    "Contrataciones": "Proceso de reclutamiento y selección de nuevo personal",
    "Evaluaciones": "Sistema de evaluación del desempeño de los empleados",
    "Capacitaciones": "Gestión de cursos y formación del personal"
}

print("FUNCIONALIDADES DEL MÓDULO:")
print("-" * 50)
for funcion, descripcion in funciones_rh.items():
    print(f"• {funcion}: {descripcion}")
print()

# 3. INTERFAZ DE USUARIO
interfaz_usuario = [
    "Vistas",
    "Pantallas",
    "Formularios",
    "Etapas",
    "Campos"
]

print("ELEMENTOS DE LA INTERFAZ:")
print("-" * 50)
for i, elemento in enumerate(interfaz_usuario, 1):
    print(f"{i}. {elemento}")
print()

# 4. SEGURIDAD Y ACCESO
seguridad_acceso = [
    "Admin",
    "Gerente de Recursos Humanos",
    "Supervisor"
]

print("ROLES Y PERMISOS:")
print("-" * 50)
for rol in seguridad_acceso:
    print(f"✓ {rol}")
print()
