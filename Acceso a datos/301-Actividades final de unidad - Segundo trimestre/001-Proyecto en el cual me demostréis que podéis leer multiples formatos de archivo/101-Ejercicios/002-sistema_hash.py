"""
RESTAURANTES DE ESPAÑA - Versión 2.0
Sistema de Hashes para Búsqueda Rápida

Implementa el uso de hashes MD5 para indexación y búsqueda eficiente de restaurantes.
En lugar de buscar secuencialmente, usamos el hash del CIF como clave de acceso directa.
"""

import hashlib
import json
import os
import time


class SistemaRestaurantesHash:
    """Gestión de restaurantes usando sistema de hashes para búsqueda rápida"""
    
    def __init__(self, ruta_base="restaurantes_datos"):
        self.ruta_base = ruta_base
        self.ruta_hash = f"{ruta_base}/hash"
        self._asegurar_directorio()
    
    def _asegurar_directorio(self):
        """Asegura que exista el directorio de hashes"""
        try:
            os.makedirs(self.ruta_hash, exist_ok=True)
        except Exception as e:
            print(f"Error al crear directorio: {e}")
    
    def generar_hash(self, clave):
        """
        Genera un hash MD5 a partir de una clave
        
        Args:
            clave: String que se usará para generar el hash
            
        Returns:
            String con el hash MD5 en hexadecimal
        """
        return hashlib.md5(clave.encode()).hexdigest()
    
    def guardar_restaurante_hash(self, restaurante):
        """
        Guarda un restaurante usando su CIF como clave de hash
        
        Args:
            restaurante: Diccionario con información del restaurante (debe incluir 'cif')
        
        Returns:
            Tuple (éxito, hash_generado)
        """
        if 'cif' not in restaurante:
            print("✗ Error: El restaurante debe tener un CIF")
            return False, None
        
        try:
            # Generar hash del CIF
            hash_cif = self.generar_hash(restaurante['cif'])
            
            # Guardar en archivo JSON nombrado con el hash
            ruta_archivo = f"{self.ruta_hash}/{hash_cif}.json"
            
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                json.dump(restaurante, archivo, indent=4, ensure_ascii=False)
            
            print(f"✓ Restaurante guardado con hash: {hash_cif}")
            print(f"  CIF: {restaurante['cif']} → Hash: {hash_cif}")
            return True, hash_cif
            
        except Exception as e:
            print(f"✗ Error al guardar restaurante: {e}")
            return False, None
    
    def buscar_restaurante_por_cif(self, cif):
        """
        Busca un restaurante por su CIF de forma directa usando hash
        
        Args:
            cif: CIF del restaurante a buscar
            
        Returns:
            Diccionario con los datos del restaurante o None si no se encuentra
        """
        try:
            # Generar hash del CIF
            hash_cif = self.generar_hash(cif)
            ruta_archivo = f"{self.ruta_hash}/{hash_cif}.json"
            
            # Acceso directo al archivo (O(1) - constante)
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                restaurante = json.load(archivo)
                print(f"✓ Restaurante encontrado usando hash: {hash_cif}")
                return restaurante
                
        except FileNotFoundError:
            print(f"✗ Restaurante no encontrado con CIF: {cif}")
            return None
        except Exception as e:
            print(f"✗ Error al buscar restaurante: {e}")
            return None
    
    def listar_todos_los_restaurantes(self):
        """
        Lista todos los restaurantes almacenados en el sistema de hashes
        
        Returns:
            Lista de diccionarios con todos los restaurantes
        """
        restaurantes = []
        
        try:
            archivos = os.listdir(self.ruta_hash)
            archivos_json = [f for f in archivos if f.endswith('.json')]
            
            for archivo in archivos_json:
                ruta_completa = f"{self.ruta_hash}/{archivo}"
                with open(ruta_completa, 'r', encoding='utf-8') as f:
                    restaurante = json.load(f)
                    restaurantes.append(restaurante)
            
            print(f"✓ {len(restaurantes)} restaurantes encontrados en el sistema")
            return restaurantes
            
        except Exception as e:
            print(f"✗ Error al listar restaurantes: {e}")
            return []
    
    def actualizar_restaurante(self, cif, datos_nuevos):
        """
        Actualiza la información de un restaurante existente
        
        Args:
            cif: CIF del restaurante a actualizar
            datos_nuevos: Diccionario con los campos a actualizar
            
        Returns:
            Boolean indicando éxito
        """
        # Primero buscamos el restaurante
        restaurante = self.buscar_restaurante_por_cif(cif)
        
        if restaurante:
            # Actualizamos los campos
            restaurante.update(datos_nuevos)
            # Guardamos de nuevo (mantiene el mismo hash porque el CIF no cambia)
            exito, _ = self.guardar_restaurante_hash(restaurante)
            if exito:
                print(f"✓ Restaurante actualizado correctamente")
            return exito
        else:
            print(f"✗ No se puede actualizar: restaurante no encontrado")
            return False
    
    def eliminar_restaurante(self, cif):
        """
        Elimina un restaurante del sistema
        
        Args:
            cif: CIF del restaurante a eliminar
            
        Returns:
            Boolean indicando éxito
        """
        try:
            hash_cif = self.generar_hash(cif)
            ruta_archivo = f"{self.ruta_hash}/{hash_cif}.json"
            
            if os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)
                print(f"✓ Restaurante eliminado correctamente")
                return True
            else:
                print(f"✗ Restaurante no encontrado")
                return False
                
        except Exception as e:
            print(f"✗ Error al eliminar restaurante: {e}")
            return False
    
    def generar_estadisticas(self):
        """
        Genera estadísticas sobre los restaurantes
        
        Returns:
            Diccionario con estadísticas
        """
        restaurantes = self.listar_todos_los_restaurantes()
        
        if not restaurantes:
            return {"total": 0}
        
        tipo_cocinas = {}
        ciudades = {}
        estrellas = {}
        
        for rest in restaurantes:
            # Contar tipos de cocina
            tipo = rest.get('tipo_cocina', 'Sin clasificar')
            tipo_cocinas[tipo] = tipo_cocinas.get(tipo, 0) + 1
            
            # Contar ciudades
            ciudad = rest.get('ciudad', 'Desconocida')
            ciudades[ciudad] = ciudades.get(ciudad, 0) + 1
            
            # Contar estrellas Michelin
            estrella = rest.get('estrellas_michelin', '0')
            est_key = f"{estrella} estrellas"
            estrellas[est_key] = estrellas.get(est_key, 0) + 1
        
        estadisticas = {
            "total": len(restaurantes),
            "tipo_cocinas": tipo_cocinas,
            "ciudades": ciudades,
            "estrellas_michelin": estrellas
        }
        
        return estadisticas


def demo_sistema_hash():
    """Demostración del sistema de hashes"""
    print("\n" + "="*60)
    print("DEMOSTRACIÓN: Sistema de Hashes para Búsqueda Rápida")
    print("="*60)
    
    sistema = SistemaRestaurantesHash()
    
    # Leer restaurantes desde el CSV
    print("\n📖 Leyendo datos desde el archivo CSV...")
    print("-" * 60)
    import csv
    restaurantes = []
    try:
        with open("restaurantes_datos/texto/restaurantes.csv", 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            restaurantes = list(lector)
        print(f"✓ {len(restaurantes)} restaurantes leídos desde CSV")
    except FileNotFoundError:
        print("✗ Archivo CSV no encontrado")
        return
    except Exception as e:
        print(f"✗ Error al leer CSV: {e}")
        return
    
    # 0. Limpiar archivos hash antiguos
    print("\n🧹 Limpiando archivos hash antiguos...")
    print("-" * 60)
    try:
        archivos_eliminados = 0
        # Listar todos los archivos en el directorio hash
        if os.path.exists(sistema.ruta_hash):
            for archivo in os.listdir(sistema.ruta_hash):
                if archivo.endswith('.json'):
                    ruta_archivo = os.path.join(sistema.ruta_hash, archivo)
                    os.remove(ruta_archivo)
                    print(f"  ✓ Eliminado: {archivo}")
                    archivos_eliminados += 1
        print(f"✓ Total: {archivos_eliminados} archivos antiguos eliminados")
    except Exception as e:
        print(f"⚠ Error al limpiar archivos: {e}")
    
    # 1. Guardar restaurantes usando hash
    print("\n1. Guardando restaurantes con sistema de hash...")
    print("-" * 60)
    for rest in restaurantes:
        sistema.guardar_restaurante_hash(rest)
    
    # 2. Búsqueda directa por CIF (muy rápida - O(1))
    print("\n2. Búsqueda directa por CIF...")
    print("-" * 60)
    # Usar el primer CIF del CSV si existe
    cif_buscar = restaurantes[0]['cif'] if restaurantes else "A28010000"
    print(f"Buscando CIF: {cif_buscar}")
    resto_encontrado = sistema.buscar_restaurante_por_cif(cif_buscar)
    if resto_encontrado:
        print(f"Nombre: {resto_encontrado['nombre']}")
        print(f"Chef: {resto_encontrado['chef']}")
        print(f"Ciudad: {resto_encontrado['ciudad']}")
        print(f"Estrellas: {resto_encontrado['estrellas_michelin']}⭐")
    
    # 3. Listar todos los restaurantes
    print("\n3. Listando todos los restaurantes...")
    print("-" * 60)
    todos = sistema.listar_todos_los_restaurantes()
    for resto in sorted(todos, key=lambda x: int(x.get('estrellas_michelin', '0')), reverse=True):
        estrellas = "⭐"*int(resto.get('estrellas_michelin', '0'))
        print(f"{estrellas} {resto['nombre']} - {resto['ciudad']}")
    
    # 4. Actualizar información de un restaurante
    print("\n4. Actualizando información...")
    print("-" * 60)
    sistema.actualizar_restaurante("A20023456", {"precio_medio": "110€"})
    
    # 5. Generar estadísticas
    print("\n5. Estadísticas del sistema...")
    print("-" * 60)
    stats = sistema.generar_estadisticas()
    print(f"Total de restaurantes: {stats['total']}")
    print(f"\nRestaurantes por ciudad:")
    for ciudad, cantidad in stats['ciudades'].items():
        print(f"  - {ciudad}: {cantidad}")
    print(f"\nDistribución de estrellas Michelin:")
    for est, cantidad in stats['estrellas_michelin'].items():
        print(f"  - {est}: {cantidad}")
    
    # 6. Comparación de rendimiento
    print("\n6. Comparando Hash O(1) vs Secuencial O(n)...")
    print("-" * 60)
    inicio = time.perf_counter()
    sistema.buscar_restaurante_por_cif(cif_buscar)
    tiempo_hash = time.perf_counter() - inicio
    
    print(f"\n⏱️  Tiempo con hash: {tiempo_hash*1000:.6f} ms")
    print("🚀 Búsqueda con hash: O(1) - acceso directo")
    print("   Búsqueda secuencial: O(n) - revisa todos los archivos")
    print("   Con 1000 restaurantes, el hash es 1000x más rápido!")


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║      RESTAURANTES DE ESPAÑA - Versión 2.0               ║
    ║      Sistema de Indexación con Hash                     ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    demo_sistema_hash()
