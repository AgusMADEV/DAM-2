"""
RESTAURANTES DE ESPAÑA - Versión 5.0
Sistema de Exploración y Árbol de Directorios

Implementa navegación recursiva del sistema de archivos de restaurantes.
Permite visualizar la estructura completa, buscar archivos y generar informes.
"""

import os
from datetime import datetime
import json


class ExploradorRestaurantes:
    """Clase para explorar y analizar el árbol de directorios de restaurantes"""
    
    def __init__(self, ruta_base="restaurantes_datos"):
        self.ruta_base = ruta_base
        self.estadisticas = {
            "total_archivos": 0,
            "total_directorios": 0,
            "tamaño_total": 0,
            "tipos_archivo": {},
            "archivos_mas_grandes": []
        }
    
    def obtener_tamaño_archivo(self, ruta):
        """
        Obtiene el tamaño de un archivo en bytes
        
        Args:
            ruta: Ruta del archivo
            
        Returns:
            Tamaño en bytes
        """
        try:
            return os.path.getsize(ruta)
        except:
            return 0
    
    def formatear_tamaño(self, bytes):
        """
        Formatea bytes a una representación legible
        
        Args:
            bytes: Tamaño en bytes
            
        Returns:
            String formateado (ej: "1.5 MB")
        """
        for unidad in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unidad}"
            bytes /= 1024.0
        return f"{bytes:.2f} TB"
    
    def recorrer_directorio_recursivo(self, ruta=None, nivel=0, mostrar=True):
        """
        Recorre recursivamente un directorio y muestra su estructura
        
        Args:
            ruta: Ruta del directorio a recorrer
            nivel: Nivel de profundidad (para indentación)
            mostrar: Si se debe imprimir la estructura
            
        Returns:
            Diccionario con la estructura del directorio
        """
        if ruta is None:
            ruta = self.ruta_base
        
        estructura = {
            "nombre": os.path.basename(ruta) or ruta,
            "tipo": "directorio",
            "ruta": ruta,
            "hijos": []
        }
        
        try:
            elementos = sorted(os.listdir(ruta))
            
            # Separar directorios y archivos
            directorios = []
            archivos = []
            
            for elemento in elementos:
                ruta_completa = os.path.join(ruta, elemento)
                if os.path.isdir(ruta_completa):
                    directorios.append(elemento)
                else:
                    archivos.append(elemento)
            
            # Procesar directorios primero
            for i, directorio in enumerate(directorios):
                ruta_completa = os.path.join(ruta, directorio)
                es_ultimo_dir = (i == len(directorios) - 1) and len(archivos) == 0
                prefijo = "└── " if es_ultimo_dir else "├── "
                
                if mostrar:
                    print("│   " * nivel + prefijo + f"📁 {directorio}/")
                
                self.estadisticas["total_directorios"] += 1
                
                # Recursión
                sub_estructura = self.recorrer_directorio_recursivo(
                    ruta_completa, 
                    nivel + 1, 
                    mostrar
                )
                estructura["hijos"].append(sub_estructura)
            
            # Procesar archivos
            for i, archivo in enumerate(archivos):
                ruta_completa = os.path.join(ruta, archivo)
                es_ultimo = i == len(archivos) - 1
                prefijo = "└── " if es_ultimo else "├── "
                
                tamaño = self.obtener_tamaño_archivo(ruta_completa)
                extension = os.path.splitext(archivo)[1].lower()
                
                # Actualizar estadísticas
                self.estadisticas["total_archivos"] += 1
                self.estadisticas["tamaño_total"] += tamaño
                self.estadisticas["tipos_archivo"][extension] = \
                    self.estadisticas["tipos_archivo"].get(extension, 0) + 1
                
                # Icono según extensión
                iconos = {
                    '.csv': '📊',
                    '.txt': '📝',
                    '.json': '📋',
                    '.pkl': '🔒',
                    '.png': '🖼️',
                    '.jpg': '🖼️',
                    '.jpeg': '🖼️',
                    '.md': '📄',
                    '.py': '🐍'
                }
                icono = iconos.get(extension, '📄')
                
                if mostrar:
                    tamaño_str = self.formatear_tamaño(tamaño)
                    print("│   " * nivel + prefijo + f"{icono} {archivo} ({tamaño_str})")
                
                # Estructura de archivo
                archivo_info = {
                    "nombre": archivo,
                    "tipo": "archivo",
                    "ruta": ruta_completa,
                    "extension": extension,
                    "tamaño": tamaño
                }
                estructura["hijos"].append(archivo_info)
        
        except PermissionError:
            if mostrar:
                print("│   " * nivel + "✗ Acceso denegado")
        except Exception as e:
            if mostrar:
                print("│   " * nivel + f"✗ Error: {e}")
        
        return estructura
    
    def buscar_archivos_por_extension(self, extension, ruta=None):
        """
        Busca todos los archivos con una extensión específica
        
        Args:
            extension: Extensión a buscar (ej: '.json')
            ruta: Ruta donde buscar (usa ruta_base si es None)
            
        Returns:
            Lista de rutas de archivos encontrados
        """
        if ruta is None:
            ruta = self.ruta_base
        
        archivos_encontrados = []
        
        try:
            for raiz, directorios, archivos in os.walk(ruta):
                for archivo in archivos:
                    if archivo.endswith(extension):
                        ruta_completa = os.path.join(raiz, archivo)
                        archivos_encontrados.append(ruta_completa)
        except Exception as e:
            print(f"✗ Error en búsqueda: {e}")
        
        return archivos_encontrados
    
    def buscar_por_nombre(self, patron, ruta=None):
        """
        Busca archivos que contengan un patrón en su nombre
        
        Args:
            patron: Texto a buscar en el nombre
            ruta: Ruta donde buscar
            
        Returns:
            Lista de rutas de archivos encontrados
        """
        if ruta is None:
            ruta = self.ruta_base
        
        archivos_encontrados = []
        patron = patron.lower()
        
        try:
            for raiz, directorios, archivos in os.walk(ruta):
                for archivo in archivos:
                    if patron in archivo.lower():
                        ruta_completa = os.path.join(raiz, archivo)
                        archivos_encontrados.append(ruta_completa)
        except Exception as e:
            print(f"✗ Error en búsqueda: {e}")
        
        return archivos_encontrados
    
    def generar_informe_completo(self):
        """
        Genera un informe completo del sistema de archivos
        
        Returns:
            Diccionario con el informe
        """
        print("\n" + "="*60)
        print("INFORME DEL SISTEMA DE ARCHIVOS DE LOS RESTAURANTES")
        print("="*60)
        
        # Resetear estadísticas
        self.estadisticas = {
            "total_archivos": 0,
            "total_directorios": 0,
            "tamaño_total": 0,
            "tipos_archivo": {},
            "archivos_mas_grandes": []
        }
        
        # Generar estructura
        print("\n📂 Estructura de directorios:\n")
        print(f"📁 {os.path.basename(self.ruta_base) or self.ruta_base}/")
        estructura = self.recorrer_directorio_recursivo(mostrar=True)
        
        # Estadísticas
        print("\n" + "-"*60)
        print("📊 ESTADÍSTICAS")
        print("-"*60)
        print(f"Total de directorios: {self.estadisticas['total_directorios']}")
        print(f"Total de archivos: {self.estadisticas['total_archivos']}")
        print(f"Tamaño total: {self.formatear_tamaño(self.estadisticas['tamaño_total'])}")
        
        if self.estadisticas['tipos_archivo']:
            print("\nArchivos por tipo:")
            for ext, count in sorted(self.estadisticas['tipos_archivo'].items()):
                print(f"  {ext or 'sin extensión'}: {count} archivo(s)")
        
        return {
            "estructura": estructura,
            "estadisticas": self.estadisticas,
            "fecha_generacion": datetime.now().isoformat()
        }
    
    def guardar_informe_json(self, nombre_archivo="informe_restaurantes.json"):
        """
        Guarda el informe en formato JSON
        
        Args:
            nombre_archivo: Nombre del archivo de salida
        """
        informe = self.generar_informe_completo()
        
        ruta_salida = os.path.join(self.ruta_base, "logs", nombre_archivo)
        
        try:
            with open(ruta_salida, 'w', encoding='utf-8') as archivo:
                json.dump(informe, archivo, indent=2, ensure_ascii=False)
            print(f"\n✓ Informe guardado en: {ruta_salida}")
        except Exception as e:
            print(f"\n✗ Error al guardar informe: {e}")
    
    def limpiar_archivos_vacios(self, ruta=None):
        """
        Encuentra y lista archivos vacíos (0 bytes)
        
        Args:
            ruta: Ruta donde buscar
            
        Returns:
            Lista de archivos vacíos
        """
        if ruta is None:
            ruta = self.ruta_base
        
        archivos_vacios = []
        
        try:
            for raiz, directorios, archivos in os.walk(ruta):
                for archivo in archivos:
                    ruta_completa = os.path.join(raiz, archivo)
                    if self.obtener_tamaño_archivo(ruta_completa) == 0:
                        archivos_vacios.append(ruta_completa)
        except Exception as e:
            print(f"✗ Error: {e}")
        
        return archivos_vacios
    
    def obtener_archivos_recientes(self, dias=7, ruta=None):
        """
        Obtiene archivos modificados recientemente
        
        Args:
            dias: Número de días hacia atrás
            ruta: Ruta donde buscar
            
        Returns:
            Lista de tuplas (ruta, fecha_modificacion)
        """
        if ruta is None:
            ruta = self.ruta_base
        
        archivos_recientes = []
        limite_tiempo = datetime.now().timestamp() - (dias * 24 * 60 * 60)
        
        try:
            for raiz, directorios, archivos in os.walk(ruta):
                for archivo in archivos:
                    ruta_completa = os.path.join(raiz, archivo)
                    try:
                        tiempo_mod = os.path.getmtime(ruta_completa)
                        if tiempo_mod > limite_tiempo:
                            fecha = datetime.fromtimestamp(tiempo_mod)
                            archivos_recientes.append((ruta_completa, fecha))
                    except:
                        pass
        except Exception as e:
            print(f"✗ Error: {e}")
        
        return sorted(archivos_recientes, key=lambda x: x[1], reverse=True)


def demo_explorador():
    """Demostración del explorador de directorios"""
    print("\n" + "="*60)
    print("DEMOSTRACIÓN: Sistema de Exploración de Directorios")
    print("="*60)
    
    explorador = ExploradorRestaurantes()
    
    # Verificar si existe el directorio
    if not os.path.exists(explorador.ruta_base):
        print(f"\n⚠️  El directorio {explorador.ruta_base} no existe aún.")
        print("Ejecuta primero los otros módulos para crear la estructura.")
        return
    
    # 1. Generar informe completo
    print("\n1. Generando informe completo de los restaurantes...")
    informe = explorador.generar_informe_completo()
    
    # 2. Buscar archivos por extensión
    print("\n2. Buscando archivos JSON...")
    print("-" * 60)
    archivos_json = explorador.buscar_archivos_por_extension('.json')
    if archivos_json:
        print(f"Encontrados {len(archivos_json)} archivos JSON:")
        for archivo in archivos_json[:5]:  # Mostrar máximo 5
            print(f"  📋 {archivo}")
    else:
        print("No se encontraron archivos JSON")
    
    # 3. Buscar archivos pickle
    print("\n3. Buscando archivos pickle (binarios)...")
    print("-" * 60)
    archivos_pkl = explorador.buscar_archivos_por_extension('.pkl')
    if archivos_pkl:
        print(f"Encontrados {len(archivos_pkl)} archivos pickle:")
        for archivo in archivos_pkl[:5]:
            tamaño = explorador.formatear_tamaño(
                explorador.obtener_tamaño_archivo(archivo)
            )
            print(f"  🔒 {os.path.basename(archivo)} ({tamaño})")
    else:
        print("No se encontraron archivos pickle")
    
    # 4. Buscar imágenes
    print("\n4. Buscando imágenes...")
    print("-" * 60)
    imagenes = (explorador.buscar_archivos_por_extension('.png') +
               explorador.buscar_archivos_por_extension('.jpg'))
    if imagenes:
        print(f"Encontradas {len(imagenes)} imágenes:")
        for imagen in imagenes:
            tamaño = explorador.formatear_tamaño(
                explorador.obtener_tamaño_archivo(imagen)
            )
            print(f"  🖼️  {os.path.basename(imagen)} ({tamaño})")
    else:
        print("No se encontraron imágenes")
    
    # 5. Archivos recientes
    print("\n5. Archivos modificados recientemente (últimos 7 días)...")
    print("-" * 60)
    recientes = explorador.obtener_archivos_recientes(dias=7)
    if recientes:
        print(f"Encontrados {len(recientes)} archivos:")
        for ruta, fecha in recientes[:10]:  # Mostrar máximo 10
            print(f"  📅 {os.path.basename(ruta)}")
            print(f"     {fecha.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("No hay archivos recientes")
    
    # 6. Guardar informe
    print("\n6. Guardando informe en JSON...")
    print("-" * 60)
    explorador.guardar_informe_json()
    
    # 7. Resumen de capacidades
    print("\n7. Capacidades del explorador...")
    print("-" * 60)
    print("""
    El explorador de directorios puede:
    
    ✓ Visualizar estructura completa en árbol
    ✓ Calcular estadísticas de archivos y directorios
    ✓ Buscar archivos por extensión
    ✓ Buscar archivos por nombre (patrón)
    ✓ Listar archivos modificados recientemente
    ✓ Detectar archivos vacíos
    ✓ Generar informes en JSON
    ✓ Calcular tamaños totales
    ✓ Clasificar archivos por tipo
    
    Útil para:
    - Auditorías del sistema de archivos
    - Mantenimiento de la base de datos de restaurantes
    - Localización rápida de documentos
    - Análisis de uso de espacio
    - Generación de backups inteligentes
    """)


if __name__ == "__main__":
    demo_explorador()
