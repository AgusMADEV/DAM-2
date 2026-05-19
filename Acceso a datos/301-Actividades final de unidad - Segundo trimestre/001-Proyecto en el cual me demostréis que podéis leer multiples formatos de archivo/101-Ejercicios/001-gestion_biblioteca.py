"""
RESTAURANTES DE ESPAÑA - Sistema de Gestión de Múltiples Formatos
Versión 1.0 - Estructura básica con archivos de texto

Este proyecto demuestra el manejo de diferentes formatos de persistencia:
- Archivos de texto plano (CSV, TXT)
- Sistema de hashes para búsqueda rápida
- Serialización con pickle
- Esteganografía en imágenes
- Navegación de árbol de directorios

Autor: Proyecto de Acceso a Datos
"""

import os
import csv
import json
from datetime import datetime

class SistemaRestaurantes:
    """Clase principal para gestionar restaurantes de España"""
    
    def __init__(self):
        self.ruta_base = "restaurantes_datos"
        self.crear_estructura_directorios()
        
    def crear_estructura_directorios(self):
        """Crea la estructura de carpetas necesaria para el proyecto"""
        directorios = [
            self.ruta_base,
            f"{self.ruta_base}/texto",
            f"{self.ruta_base}/hash",
            f"{self.ruta_base}/binario",
            f"{self.ruta_base}/imagenes",
            f"{self.ruta_base}/logs"
        ]
        
        for directorio in directorios:
            try:
                os.makedirs(directorio, exist_ok=True)
                print(f"✓ Directorio creado/verificado: {directorio}")
            except Exception as e:
                print(f"✗ Error al crear {directorio}: {e}")
    
    def guardar_en_csv(self, datos, nombre_archivo="restaurantes.csv"):
        """
        Guarda datos de restaurantes en formato CSV
        
        Args:
            datos: Lista de diccionarios con información de restaurantes
            nombre_archivo: Nombre del archivo CSV
        """
        ruta_completa = f"{self.ruta_base}/texto/{nombre_archivo}"
        
        try:
            with open(ruta_completa, 'w', newline='', encoding='utf-8') as archivo:
                if datos:
                    campos = datos[0].keys()
                    escritor = csv.DictWriter(archivo, fieldnames=campos)
                    escritor.writeheader()
                    escritor.writerows(datos)
                    print(f"✓ Datos guardados en CSV: {ruta_completa}")
                    return True
        except Exception as e:
            print(f"✗ Error al guardar CSV: {e}")
            return False
    
    def leer_desde_csv(self, nombre_archivo="restaurantes.csv"):
        """
        Lee datos desde un archivo CSV
        
        Args:
            nombre_archivo: Nombre del archivo CSV
            
        Returns:
            Lista de diccionarios con los datos leídos
        """
        ruta_completa = f"{self.ruta_base}/texto/{nombre_archivo}"
        
        try:
            with open(ruta_completa, 'r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                datos = list(lector)
                print(f"✓ Leídos {len(datos)} registros desde CSV")
                return datos
        except FileNotFoundError:
            print(f"✗ Archivo no encontrado: {ruta_completa}")
            return []
        except Exception as e:
            print(f"✗ Error al leer CSV: {e}")
            return []
    
    def guardar_en_texto(self, contenido, nombre_archivo="registro.txt"):
        """
        Guarda contenido en un archivo de texto plano
        
        Args:
            contenido: Texto a guardar
            nombre_archivo: Nombre del archivo
        """
        ruta_completa = f"{self.ruta_base}/texto/{nombre_archivo}"
        
        try:
            with open(ruta_completa, 'a', encoding='utf-8') as archivo:
                fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                archivo.write(f"[{fecha_hora}] {contenido}\n")
                print(f"✓ Registro guardado en: {ruta_completa}")
                return True
        except Exception as e:
            print(f"✗ Error al guardar texto: {e}")
            return False
    
    def leer_desde_texto(self, nombre_archivo="registro.txt"):
        """
        Lee contenido desde un archivo de texto
        
        Args:
            nombre_archivo: Nombre del archivo
            
        Returns:
            Contenido del archivo como string
        """
        ruta_completa = f"{self.ruta_base}/texto/{nombre_archivo}"
        
        try:
            with open(ruta_completa, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
                print(f"✓ Archivo leído correctamente")
                return contenido
        except FileNotFoundError:
            print(f"✗ Archivo no encontrado: {ruta_completa}")
            return ""
        except Exception as e:
            print(f"✗ Error al leer texto: {e}")
            return ""


def demo_archivos_texto():
    """Demostración de operaciones con archivos de texto"""
    print("\n" + "="*60)
    print("DEMOSTRACIÓN: Archivos de Texto Plano")
    print("="*60)
    
    sistema = SistemaRestaurantes()
    
    # Datos de ejemplo de restaurantes españoles
    restaurantes = [
        {
            "cif": "A28010000",
            "nombre": "DiverXO",
            "chef": "Dabiz Muñoz",
            "ciudad": "Madrid",
            "tipo_cocina": "Fusión vanguardista",
            "estrellas_michelin": "3",
            "precio_medio": "250€"
        },
        {
            "cif": "B08012345",
            "nombre": "Disfrutar",
            "chef": "Oriol Castro, Eduard Xatruch, Mateu Casañas",
            "ciudad": "Barcelona",
            "tipo_cocina": "Mediterránea creativa",
            "estrellas_michelin": "3",
            "precio_medio": "220€"
        },
        {
            "cif": "A20023456",
            "nombre": "Elkano",
            "chef": "Pedro Arregui",
            "ciudad": "Getaria",
            "tipo_cocina": "Asador vasco",
            "estrellas_michelin": "1",
            "precio_medio": "100€"
        },
        {
            "cif": "B41034567",
            "nombre": "Abantal",
            "chef": "Julio Fernández",
            "ciudad": "Sevilla",
            "tipo_cocina": "Andaluza moderna",
            "estrellas_michelin": "1",
            "precio_medio": "85€"
        }
    ]
    
    # Guardar en CSV
    print("\n1. Guardando restaurantes en formato CSV...")
    sistema.guardar_en_csv(restaurantes)
    
    # Leer desde CSV
    print("\n2. Leyendo restaurantes desde CSV...")
    restaurantes_leidos = sistema.leer_desde_csv()
    for restaurante in restaurantes_leidos:
        print(f"   - {restaurante['nombre']} ({restaurante['ciudad']}) - {restaurante['estrellas_michelin']}⭐ Michelin")
    
    # Guardar registro de operaciones en texto
    print("\n3. Guardando registros de actividad...")
    sistema.guardar_en_texto("Sistema iniciado")
    sistema.guardar_en_texto(f"Se guardaron {len(restaurantes)} restaurantes en la base de datos")
    sistema.guardar_en_texto("Operación de lectura completada exitosamente")
    
    # Leer registro
    print("\n4. Leyendo registro de actividad...")
    registro = sistema.leer_desde_texto()
    print(registro)


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║      RESTAURANTES DE ESPAÑA - Versión 1.0               ║
    ║      Sistema de Gestión de Múltiples Formatos           ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    demo_archivos_texto()
