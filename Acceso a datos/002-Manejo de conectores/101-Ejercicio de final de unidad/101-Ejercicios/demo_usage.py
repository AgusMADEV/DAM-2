from AMA import AMA


def main():
    """Demostración principal del componente AMA"""
    
    print("🎯 DEMOSTRACIÓN COMPONENTE AMA")
    print("=" * 40)
    print("Basado en el patrón visto en clase\n")
    
    # PASO 1: Crear conexión (cambia estos datos por los tuyos)
    print("📡 Conectando a la base de datos...")
    try:
        conexion = AMA(
            host="localhost",
            usuario="futbol_amadev",      # Cambia por tu usuario
            contrasena="futbol_amadev",  # Cambia por tu contraseña
            basedatos="futbol_amadev"     # Cambia por tu base de datos
        )
        print("✅ Conexión establecida correctamente\n")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("Verifica tus credenciales de base de datos")
        return
    
    try:
        # PASO 2: Ver tablas disponibles
        print("📋 Tablas disponibles en la base de datos:")
        tablas_json = conexion.tablas()
        print(tablas_json)
        print()
        
        # PASO 3: Crear tabla de ejemplo si no existe
        print("🏗️  Creando tabla de ejemplo...")
        sql_crear_tabla = """
        CREATE TABLE IF NOT EXISTS usuarios_ama (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            edad INT,
            activo BOOLEAN DEFAULT TRUE
        )
        """
        conexion.ejecutar_sql(sql_crear_tabla)
        print("✅ Tabla 'usuarios_ama' lista\n")
        
        # PASO 4: Insertar datos de ejemplo
        print("➕ Insertando usuarios de ejemplo...")
        
        # Usuario 1
        usuario1_id = conexion.insertar("usuarios_ama", {
            "nombre": "Ana García",
            "email": "ana@example.com",
            "edad": 28,
            "activo": True
        })
        print(f"   Usuario Ana insertado con ID: {usuario1_id}")
        
        # Usuario 2
        usuario2_id = conexion.insertar("usuarios_ama", {
            "nombre": "Carlos López",
            "email": "carlos@example.com",
            "edad": 35,
            "activo": True
        })
        print(f"   Usuario Carlos insertado con ID: {usuario2_id}")
        
        # Usuario 3
        usuario3_id = conexion.insertar("usuarios_ama", {
            "nombre": "Elena Botezatu",
            "email": "elena@example.com", 
            "edad": 29,
            "activo": False
        })
        print(f"   Usuario Elena insertado con ID: {usuario3_id}\n")
        
        # PASO 5: Seleccionar todos los usuarios
        print("👥 Todos los usuarios en la tabla:")
        usuarios = conexion.seleccionar("usuarios_ama")
        print(usuarios)
        print()
        
        # PASO 6: Buscar usuarios por criterio
        print("🔍 Buscando usuarios por email que contenga 'ana':")
        busqueda = conexion.buscar("usuarios_ama", "email", "ana")
        print(busqueda)
        print()
        
        # PASO 7: Actualizar un usuario
        print("✏️  Actualizando edad de Ana...")
        filas_actualizadas = conexion.actualizar(
            "usuarios_ama",
            {"edad": 29, "email": "ana.garcia@example.com"},
            {"id": usuario1_id}
        )
        print(f"   {filas_actualizadas} fila(s) actualizada(s)\n")
        
        # PASO 8: Ver usuarios después de la actualización
        print("👥 Usuarios después de la actualización:")
        usuarios_actualizados = conexion.seleccionar("usuarios_ama")
        print(usuarios_actualizados)
        print()
        
        # PASO 9: Consulta personalizada
        print("📊 Consulta personalizada - Usuarios activos:")
        usuarios_activos = conexion.ejecutar_sql(
            "SELECT nombre, email, edad FROM usuarios_ama WHERE activo = %s ORDER BY edad",
            (True,)
        )
        print(usuarios_activos)
        print()
        
        # PASO 10: Describir estructura de tabla
        print("🔍 Estructura de la tabla usuarios_ama:")
        estructura = conexion.describir("usuarios_ama")
        print(estructura)
        print()
        
        # PASO 11: Estadísticas con consulta personalizada
        print("📈 Estadísticas de usuarios:")
        stats = conexion.ejecutar_sql("""
            SELECT 
                COUNT(*) as total_usuarios,
                AVG(edad) as edad_promedio,
                MIN(edad) as edad_minima,
                MAX(edad) as edad_maxima,
                SUM(CASE WHEN activo = 1 THEN 1 ELSE 0 END) as usuarios_activos
            FROM usuarios_ama
        """)
        print(stats)
        print()
        
        # PASO 12: Opcional - Limpiar datos de demostración
        respuesta = input("¿Quieres eliminar los datos de demostración? (s/n): ")
        if respuesta.lower() == 's':
            print("🗑️  Limpiando datos de demostración...")
            eliminados = conexion.eliminar("usuarios_ama", {"nombre": "Ana García"})
            eliminados += conexion.eliminar("usuarios_ama", {"nombre": "Carlos López"})
            eliminados += conexion.eliminar("usuarios_ama", {"nombre": "Elena Botezatu"})
            print(f"   {eliminados} registro(s) eliminado(s)")
            
            # Eliminar tabla si está vacía
            confirmar = input("¿Eliminar también la tabla usuarios_ama? (s/n): ")
            if confirmar.lower() == 's':
                conexion.ejecutar_sql("DROP TABLE usuarios_ama")
                print("   Tabla eliminada")
        
        print("\n🎉 ¡Demostración completada exitosamente!")
        print("\nEl componente JVDB está listo para usar en tus proyectos:")
        print("- ✅ Conexión simple a MySQL")
        print("- ✅ Operaciones CRUD básicas")
        print("- ✅ Consultas personalizadas") 
        print("- ✅ Resultados en formato JSON")
        print("- ✅ Validación de identificadores")
        
    except Exception as e:
        print(f"❌ Error durante la demostración: {e}")
    
    finally:
        # PASO 13: Cerrar conexión
        print("\n🔌 Cerrando conexión...")
        conexion.cerrar()
        print("✅ Conexión cerrada")


def ejemplo_integracion():
    """Ejemplo de cómo integrar AMA en un proyecto"""
    
    print("\n" + "=" * 50)
    print("📝 EJEMPLO DE INTEGRACIÓN EN PROYECTO")
    print("=" * 50)
    
    print("""
# En tu proyecto, podrías usarlo así:

from data_access_component import AMA

# 1. Crear conexión
db = AMA("localhost", "tu_usuario", "tu_password", "tu_database")

# 2. Usar en funciones de tu aplicación
def obtener_usuarios():
    return db.seleccionar("usuarios")

def crear_usuario(nombre, email, edad):
    return db.insertar("usuarios", {
        "nombre": nombre,
        "email": email,
        "edad": edad
    })

def buscar_usuario_por_email(email):
    return db.buscar("usuarios", "email", email)

# 3. Para APIs web (Flask, etc.)
@app.route('/api/usuarios')
def api_usuarios():
    usuarios_json = db.seleccionar("usuarios")
    return usuarios_json  # Ya está en formato JSON

# 4. No olvides cerrar al terminar
db.cerrar()
    """)


if __name__ == "__main__":
    main()
    ejemplo_integracion()