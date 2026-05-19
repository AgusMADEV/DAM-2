"""
RESTAURANTES DE ESPAÑA - Sistema Completo Integrado
Versión Final 1.0

Este programa integra todos los métodos de persistencia de datos:
1. Archivos de texto plano (CSV, TXT)
2. Sistema de hashes para búsqueda rápida
3. Serialización binaria con pickle
4. Esteganografía en imágenes
5. Exploración de árbol de directorios

Autor: Proyecto de Acceso a Datos
Fecha: 2026
"""

import os
import sys


def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter"""
    input("\nPresiona Enter para continuar...")


def mostrar_banner():
    """Muestra el banner principal del programa"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║         �  RESTAURANTES DE ESPAÑA 🇪🇸                       ║
    ║                                                          ║
    ║      Sistema Integral de Gestión de Datos                ║
    ║           Versión 1.0 - 2026                            ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)


def menu_principal():
    """Muestra el menú principal y retorna la opción seleccionada"""
    print("\n" + "="*60)
    print("MENÚ PRINCIPAL")
    print("="*60)
    print("""
    1. 📝 Gestión de Archivos de Texto (CSV/TXT)
    2. 🔍 Sistema de Búsqueda con Hashes
    3. 🔒 Serialización Binaria (Pickle)
    4. 🖼️  Esteganografía en Imágenes
    5. 📂 Explorador de Directorios
    6. 🎯 Demostración Completa
    7. ℹ️  Información del Proyecto
    0. ❌ Salir
    """)
    
    try:
        opcion = input("Selecciona una opción: ").strip()
        return opcion
    except:
        return ""


def opcion_archivos_texto():
    """Menú y ejecución para archivos de texto"""
    limpiar_pantalla()
    mostrar_banner()
    print("\n📝 GESTIÓN DE ARCHIVOS DE TEXTO")
    print("="*60)
    
    try:
        from importlib import import_module
        modulo = import_module('001-gestion_biblioteca')
        modulo.demo_archivos_texto()
    except Exception as e:
        print(f"✗ Error al ejecutar módulo: {e}")
        print("\nAsegúrate de que el archivo '001-gestion_biblioteca.py' existe.")
    
    pausar()


def opcion_sistema_hash():
    """Menú y ejecución para sistema de hashes"""
    limpiar_pantalla()
    mostrar_banner()
    print("\n🔍 SISTEMA DE BÚSQUEDA CON HASHES")
    print("="*60)
    
    try:
        from importlib import import_module
        modulo = import_module('002-sistema_hash')
        modulo.demo_sistema_hash()
    except Exception as e:
        print(f"✗ Error al ejecutar módulo: {e}")
        print("\nAsegúrate de que el archivo '002-sistema_hash.py' existe.")
    
    pausar()


def opcion_pickle():
    """Menú y ejecución para serialización pickle"""
    limpiar_pantalla()
    mostrar_banner()
    print("\n🔒 SERIALIZACIÓN BINARIA CON PICKLE")
    print("="*60)
    
    try:
        from importlib import import_module
        modulo = import_module('003-serializacion_pickle')
        modulo.demo_serializacion_pickle()
    except Exception as e:
        print(f"✗ Error al ejecutar módulo: {e}")
        print("\nAsegúrate de que el archivo '003-serializacion_pickle.py' existe.")
    
    pausar()


def opcion_esteganografia():
    """Menú y ejecución para esteganografía"""
    limpiar_pantalla()
    mostrar_banner()
    print("\n🖼️  ESTEGANOGRAFÍA EN IMÁGENES")
    print("="*60)
    
    try:
        from importlib import import_module
        modulo = import_module('004-esteganografia')
        modulo.demo_esteganografia()
    except Exception as e:
        print(f"✗ Error al ejecutar módulo: {e}")
        print("\nAsegúrate de que el archivo '004-esteganografia.py' existe.")
        print("Nota: Requiere la librería Pillow (pip install Pillow)")
    
    pausar()


def opcion_explorador():
    """Menú y ejecución para explorador de directorios"""
    limpiar_pantalla()
    mostrar_banner()
    print("\n📂 EXPLORADOR DE DIRECTORIOS")
    print("="*60)
    
    try:
        from importlib import import_module
        modulo = import_module('005-explorador_directorios')
        modulo.demo_explorador()
    except Exception as e:
        print(f"✗ Error al ejecutar módulo: {e}")
        print("\nAsegúrate de que el archivo '005-explorador_directorios.py' existe.")
    
    pausar()


def opcion_demo_completa():
    """Ejecuta una demostración completa de todos los módulos"""
    limpiar_pantalla()
    mostrar_banner()
    print("\n🎯 DEMOSTRACIÓN COMPLETA DEL SISTEMA")
    print("="*60)
    print("\nEste proceso ejecutará todas las demostraciones en secuencia.")
    print("Puede tomar unos minutos completar todas las operaciones.")
    
    confirmar = input("\n¿Deseas continuar? (s/n): ").strip().lower()
    
    if confirmar != 's':
        print("Demostración cancelada.")
        pausar()
        return
    
    modulos = [
        ('001-gestion_biblioteca', '📝 Archivos de Texto'),
        ('002-sistema_hash', '🔍 Sistema de Hashes'),
        ('003-serializacion_pickle', '🔒 Serialización Pickle'),
        ('004-esteganografia', '🖼️  Esteganografía'),
        ('005-explorador_directorios', '📂 Explorador')
    ]
    
    for i, (nombre_modulo, descripcion) in enumerate(modulos, 1):
        print(f"\n{'='*60}")
        print(f"[{i}/{len(modulos)}] Ejecutando: {descripcion}")
        print('='*60)
        
        try:
            from importlib import import_module
            modulo = import_module(nombre_modulo)
            
            # Ejecutar la demo correspondiente
            if nombre_modulo == '001-gestion_biblioteca':
                modulo.demo_archivos_texto()
            elif nombre_modulo == '002-sistema_hash':
                modulo.demo_sistema_hash()
            elif nombre_modulo == '003-serializacion_pickle':
                modulo.demo_serializacion_pickle()
            elif nombre_modulo == '004-esteganografia':
                modulo.demo_esteganografia()
            elif nombre_modulo == '005-explorador_directorios':
                modulo.demo_explorador()
            
            print(f"\n✓ {descripcion} completado exitosamente")
            
        except Exception as e:
            print(f"\n✗ Error al ejecutar {descripcion}: {e}")
        
        if i < len(modulos):
            input("\nPresiona Enter para continuar con el siguiente módulo...")
    
    print("\n" + "="*60)
    print("✓ DEMOSTRACIÓN COMPLETA FINALIZADA")
    print("="*60)
    print("""
    Se ha completado la ejecución de todos los módulos.
    
    Revisa el directorio 'biblioteca_datos' para ver:
    - Archivos CSV y TXT en /texto
    - Archivos JSON con hash en /hash
    - Objetos serializados en /binario
    - Imágenes con datos ocultos en /imagenes
    - Informes del sistema en /logs
    """)
    
    pausar()


def opcion_informacion():
    """Muestra información detallada del proyecto"""
    limpiar_pantalla()
    mostrar_banner()
    print("\nℹ️  INFORMACIÓN DEL PROYECTO")
    print("="*60)
    print("""
    BIBLIOTECA DIGITAL - Sistema Integral de Gestión de Datos
    
    📋 DESCRIPCIÓN:
    Este proyecto demuestra el dominio de múltiples formatos de 
    persistencia de datos en Python, cumpliendo con los requisitos
    de la asignatura de Acceso a Datos.
    
    🎯 OBJETIVOS CUMPLIDOS:
    
    1. ✓ Escritura y lectura de archivos en modo texto
       - Archivos CSV para datos tabulares
       - Archivos TXT para logs y registros
       - Manejo de codificación UTF-8
    
    2. ✓ Sistema de hashes para indexación
       - Uso de MD5 para generar identificadores únicos
       - Acceso directo O(1) a archivos
       - Comparación: secuencial O(n) vs hash O(1)
    
    3. ✓ Serialización binaria con pickle
       - Objetos Python completos con métodos
       - Preservación de tipos de datos complejos
       - Ventajas sobre JSON para objetos complejos
    
    4. ✓ Esteganografía en imágenes
       - Técnica LSB (Least Significant Bit)
       - Ocultación invisible de datos
       - Aplicaciones de seguridad
    
    5. ✓ Exploración de árbol de directorios
       - Navegación recursiva del sistema
       - Generación de informes
       - Búsqueda y análisis de archivos
    
    💡 CASOS DE USO REALES:
    
    • Gestión de bibliotecas y archivos
    • Sistemas de backup inteligentes
    • Protección de datos sensibles
    • Marcas de agua digitales
    • Sistemas de auditoría
    • Bases de datos ligeras
    
    🔧 TECNOLOGÍAS UTILIZADAS:
    
    • Python 3.x
    • Módulos estándar: os, json, pickle, hashlib, csv
    • Pillow (PIL) para procesamiento de imágenes
    • Estructura orientada a objetos
    • Patrones de diseño (Singleton, Factory)
    
    📚 CONCEPTOS DEMOSTRADOS:
    
    • Programación orientada a objetos
    • Manejo de excepciones
    • Entrada/Salida de archivos
    • Algoritmos de hash
    • Manipulación de bits
    • Recursividad
    • Serialización/Deserialización
    • Estructuras de datos complejas
    
    👨‍💻 DESARROLLO:
    
    Este proyecto fue desarrollado de manera incremental,
    añadiendo funcionalidad en cada versión:
    
    v1.0 - Archivos de texto básicos
    v2.0 - Sistema de hashes
    v3.0 - Serialización con pickle
    v4.0 - Esteganografía
    v5.0 - Explorador de directorios
    vFinal - Integración completa
    
    📖 ESTRUCTURA DEL CÓDIGO:
    
    001-gestion_biblioteca.py    - Archivos texto
    002-sistema_hash.py           - Sistema de hashes
    003-serializacion_pickle.py   - Pickle binario
    004-esteganografia.py         - Imágenes
    005-explorador_directorios.py - Explorador
    006-programa_principal.py     - Menú integrado
    
    🎓 APLICACIÓN ACADÉMICA:
    
    Este proyecto cumple con los criterios de evaluación de la
    asignatura "Acceso a Datos" demostrando:
    
    • Comprensión de diferentes formatos de persistencia
    • Capacidad de implementar soluciones complejas
    • Conocimiento de estructuras de datos
    • Buenas prácticas de programación
    • Documentación clara y completa
    
    ═══════════════════════════════════════════════════════════
    Proyecto desarrollado para DAM - 2º Curso
    Asignatura: Acceso a Datos
    Año: 2026
    ═══════════════════════════════════════════════════════════
    """)
    
    pausar()


def main():
    """Función principal del programa"""
    while True:
        limpiar_pantalla()
        mostrar_banner()
        
        opcion = menu_principal()
        
        if opcion == '1':
            opcion_archivos_texto()
        elif opcion == '2':
            opcion_sistema_hash()
        elif opcion == '3':
            opcion_pickle()
        elif opcion == '4':
            opcion_esteganografia()
        elif opcion == '5':
            opcion_explorador()
        elif opcion == '6':
            opcion_demo_completa()
        elif opcion == '7':
            opcion_informacion()
        elif opcion == '0':
            limpiar_pantalla()
            print("\n" + "="*60)
            print("Gracias por usar la Biblioteca Digital")
            print("="*60)
            print("""
            🏛️  Sistema cerrado correctamente
            
            Recuerda revisar el directorio 'biblioteca_datos'
            para ver todos los archivos generados.
            
            ¡Hasta pronto! 👋
            """)
            sys.exit(0)
        else:
            print("\n⚠️  Opción no válida. Por favor, selecciona una opción del menú.")
            pausar()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario.")
        print("Saliendo...")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error inesperado: {e}")
        print("El programa se cerrará.")
        sys.exit(1)
