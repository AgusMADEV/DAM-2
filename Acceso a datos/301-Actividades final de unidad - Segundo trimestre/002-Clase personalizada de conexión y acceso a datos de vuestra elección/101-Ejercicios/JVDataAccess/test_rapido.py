"""
Script de prueba rápida para JVDataAccess
"""

import sys
import os

# Añadir el directorio src al path para importar los módulos
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'src', 'python'))

from jvdb import JVDB

# Importar configuración
sys.path.insert(0, project_root)
from config import DB_CONFIG

print("=" * 80)
print("🧪 Prueba Rápida de JVDataAccess v1.0")
print("=" * 80)

try:
    # Crear instancia de JVDB
    print("\n1. Conectando a la base de datos...")
    db = JVDB(
        host=DB_CONFIG['host'],
        usuario=DB_CONFIG['user'],
        contrasena=DB_CONFIG['password'],
        basedatos=DB_CONFIG['database']
    )
    
    # Prueba 1: Listar tablas
    print("\n2. Listando tablas...")
    tablas = db.tablas(formato='list')
    print(f"   ✅ Se encontraron {len(tablas)} tablas:")
    for tabla in tablas:
        print(f"      📋 {tabla}")
    
    # Prueba 2: Consultar productos
    print("\n3. Consultando productos...")
    productos = db.seleccionar('productos', formato='list')
    print(f"   ✅ Se encontraron {len(productos)} productos:")
    for producto in productos[:3]:
        print(f"      🛍️  {producto['nombre']} - ${producto['precio']}")
    
    # Prueba 3: Buscar por categoría
    print("\n4. Buscando productos de 'Audio'...")
    resultados = db.buscar('productos', 'categoria', 'Audio', formato='list')
    print(f"   ✅ Se encontraron {len(resultados)} productos de Audio:")
    for producto in resultados:
        print(f"      🎧 {producto['nombre']}")
    
    # Prueba 4: Consultar un cliente
    print("\n5. Consultando cliente con ID 1...")
    cliente = db.seleccionar_uno('clientes', 1)
    if cliente:
        print(f"   ✅ Cliente encontrado:")
        print(f"      👤 {cliente['nombre']} {cliente['apellidos']}")
        print(f"      📧 {cliente['email']}")
    
    # Cerrar conexión
    print("\n6. Cerrando conexión...")
    db.desconectar()
    
    print("\n" + "=" * 80)
    print("✅ ¡TODAS LAS PRUEBAS PASARON CORRECTAMENTE!")
    print("=" * 80)
    print("\nJVDataAccess está funcionando perfectamente. 🎉")
    print("Puedes ejecutar 'python ejemplo_basico.py' para ver más ejemplos.\n")

except Exception as e:
    print(f"\n❌ Error durante la prueba: {e}")
    import traceback
    traceback.print_exc()
    print("\n⚠️  Verifica que:")
    print("   - MySQL esté ejecutándose")
    print("   - Hayas ejecutado database/init.sql")
    print("   - Las credenciales en config.py sean correctas")
