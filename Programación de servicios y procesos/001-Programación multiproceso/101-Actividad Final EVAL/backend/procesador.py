"""
Procesador de imágenes multinúcleo
Distribuye el procesamiento de múltiples imágenes entre los núcleos disponibles
usando threading y multiprocessing
"""

import os
import time
import threading
import multiprocessing
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from filtros import aplicar_filtro, FiltrosImagen


class ProcesadorImagenes:
    """
    Clase principal para procesar múltiples imágenes en paralelo
    Utiliza threading y multiprocessing para maximizar el uso de CPU
    """
    
    def __init__(self, callback_progreso=None):
        """
        Inicializa el procesador
        
        Args:
            callback_progreso: Función callback para reportar progreso (opcional)
        """
        self.num_nucleos = multiprocessing.cpu_count()
        self.callback_progreso = callback_progreso
        self.lock = threading.Lock()
        self.imagenes_procesadas = 0
        self.total_imagenes = 0
        self.tiempo_inicio = 0
        self.estadisticas = {
            'exitosas': 0,
            'fallidas': 0,
            'tiempo_total': 0,
            'nucleos_usados': self.num_nucleos
        }
        
    def _reportar_progreso(self, imagen, estado, mensaje=""):
        """
        Reporta el progreso del procesamiento
        
        Args:
            imagen: Nombre de la imagen procesada
            estado: Estado del procesamiento ('procesando', 'completado', 'error')
            mensaje: Mensaje adicional
        """
        with self.lock:
            if estado == 'completado':
                self.imagenes_procesadas += 1
                self.estadisticas['exitosas'] += 1
            elif estado == 'error':
                self.imagenes_procesadas += 1
                self.estadisticas['fallidas'] += 1
            
            porcentaje = (self.imagenes_procesadas / self.total_imagenes * 100) if self.total_imagenes > 0 else 0
            tiempo_transcurrido = time.time() - self.tiempo_inicio
            
            info = {
                'imagen': imagen,
                'estado': estado,
                'mensaje': mensaje,
                'procesadas': self.imagenes_procesadas,
                'total': self.total_imagenes,
                'porcentaje': round(porcentaje, 2),
                'tiempo_transcurrido': round(tiempo_transcurrido, 2),
                'nucleos': self.num_nucleos
            }
            
            if self.callback_progreso:
                self.callback_progreso(info)
    
    def procesar_con_threads(self, imagenes, filtro, directorio_salida, max_workers=None):
        """
        Procesa imágenes usando ThreadPoolExecutor
        Ideal para operaciones I/O bound
        
        Args:
            imagenes: Lista de rutas de imágenes a procesar
            filtro: Nombre del filtro a aplicar
            directorio_salida: Directorio donde guardar las imágenes procesadas
            max_workers: Número máximo de threads (default: núcleos * 2)
            
        Returns:
            Estadísticas del procesamiento
        """
        if max_workers is None:
            max_workers = self.num_nucleos * 2
        
        self.total_imagenes = len(imagenes)
        self.imagenes_procesadas = 0
        self.tiempo_inicio = time.time()
        
        print(f"\n🚀 Iniciando procesamiento con THREADS")
        print(f"📊 Núcleos disponibles: {self.num_nucleos}")
        print(f"🔧 Workers (threads): {max_workers}")
        print(f"📁 Imágenes a procesar: {self.total_imagenes}")
        print(f"🎨 Filtro: {filtro}\n")
        
        # Crear directorio de salida si no existe
        Path(directorio_salida).mkdir(parents=True, exist_ok=True)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futuros = []
            
            for ruta_imagen in imagenes:
                nombre_archivo = os.path.basename(ruta_imagen)
                nombre_sin_ext, ext = os.path.splitext(nombre_archivo)
                nombre_salida = f"{nombre_sin_ext}_{filtro}{ext}"
                ruta_salida = os.path.join(directorio_salida, nombre_salida)
                
                futuro = executor.submit(
                    self._procesar_imagen_individual,
                    ruta_imagen,
                    ruta_salida,
                    filtro,
                    'thread'
                )
                futuros.append(futuro)
            
            # Esperar a que todas las tareas terminen
            for futuro in as_completed(futuros):
                try:
                    futuro.result()
                except Exception as e:
                    print(f"❌ Error en thread: {str(e)}")
        
        self.estadisticas['tiempo_total'] = time.time() - self.tiempo_inicio
        return self.estadisticas
    
    def procesar_con_procesos(self, imagenes, filtro, directorio_salida, max_workers=None):
        """
        Procesa imágenes usando ProcessPoolExecutor
        Ideal para operaciones CPU bound (mejor rendimiento)
        
        Args:
            imagenes: Lista de rutas de imágenes a procesar
            filtro: Nombre del filtro a aplicar
            directorio_salida: Directorio donde guardar las imágenes procesadas
            max_workers: Número máximo de procesos (default: núcleos)
            
        Returns:
            Estadísticas del procesamiento
        """
        if max_workers is None:
            max_workers = self.num_nucleos
        
        self.total_imagenes = len(imagenes)
        self.imagenes_procesadas = 0
        self.tiempo_inicio = time.time()
        
        print(f"\n🚀 Iniciando procesamiento con PROCESOS PARALELOS")
        print(f"📊 Núcleos disponibles: {self.num_nucleos}")
        print(f"🔧 Workers (procesos): {max_workers}")
        print(f"📁 Imágenes a procesar: {self.total_imagenes}")
        print(f"🎨 Filtro: {filtro}\n")
        
        # Crear directorio de salida si no existe
        Path(directorio_salida).mkdir(parents=True, exist_ok=True)
        
        # Preparar tareas
        tareas = []
        for ruta_imagen in imagenes:
            nombre_archivo = os.path.basename(ruta_imagen)
            nombre_sin_ext, ext = os.path.splitext(nombre_archivo)
            nombre_salida = f"{nombre_sin_ext}_{filtro}{ext}"
            ruta_salida = os.path.join(directorio_salida, nombre_salida)
            
            tareas.append((ruta_imagen, ruta_salida, filtro))
        
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futuros = []
            
            for tarea in tareas:
                futuro = executor.submit(aplicar_filtro, *tarea)
                futuros.append((futuro, tarea[0]))
            
            # Esperar y reportar progreso
            for futuro, ruta_imagen in futuros:
                nombre_archivo = os.path.basename(ruta_imagen)
                try:
                    resultado = futuro.result()
                    if resultado:
                        self._reportar_progreso(nombre_archivo, 'completado', 'Procesado exitosamente')
                    else:
                        self._reportar_progreso(nombre_archivo, 'error', 'Error al procesar')
                except Exception as e:
                    self._reportar_progreso(nombre_archivo, 'error', str(e))
        
        self.estadisticas['tiempo_total'] = time.time() - self.tiempo_inicio
        return self.estadisticas
    
    def _procesar_imagen_individual(self, ruta_entrada, ruta_salida, filtro, modo):
        """
        Procesa una imagen individual (usado por threads)
        
        Args:
            ruta_entrada: Ruta de la imagen de entrada
            ruta_salida: Ruta de salida
            filtro: Nombre del filtro
            modo: 'thread' o 'process'
        """
        nombre_archivo = os.path.basename(ruta_entrada)
        
        try:
            self._reportar_progreso(nombre_archivo, 'procesando', f'Procesando con {modo}...')
            
            resultado = aplicar_filtro(ruta_entrada, ruta_salida, filtro)
            
            if resultado:
                self._reportar_progreso(nombre_archivo, 'completado', 'Procesado exitosamente')
            else:
                self._reportar_progreso(nombre_archivo, 'error', 'Error al aplicar filtro')
                
        except Exception as e:
            self._reportar_progreso(nombre_archivo, 'error', str(e))
    
    def procesar_batch(self, imagenes, filtros, directorio_salida, modo='procesos'):
        """
        Procesa un batch de imágenes aplicando múltiples filtros
        
        Args:
            imagenes: Lista de rutas de imágenes
            filtros: Lista de filtros a aplicar
            directorio_salida: Directorio de salida
            modo: 'threads' o 'procesos' (default: 'procesos')
            
        Returns:
            Lista de estadísticas para cada filtro
        """
        resultados = []
        
        for filtro in filtros:
            print(f"\n{'='*60}")
            print(f"Aplicando filtro: {filtro.upper()}")
            print(f"{'='*60}")
            
            directorio_filtro = os.path.join(directorio_salida, filtro)
            
            if modo == 'threads':
                stats = self.procesar_con_threads(imagenes, filtro, directorio_filtro)
            else:
                stats = self.procesar_con_procesos(imagenes, filtro, directorio_filtro)
            
            stats['filtro'] = filtro
            resultados.append(stats)
            
            # Reiniciar estadísticas para el siguiente filtro
            self.estadisticas = {
                'exitosas': 0,
                'fallidas': 0,
                'tiempo_total': 0,
                'nucleos_usados': self.num_nucleos
            }
        
        return resultados
    
    def comparar_rendimiento(self, imagenes, filtro, directorio_salida):
        """
        Compara el rendimiento entre threads y procesos
        
        Args:
            imagenes: Lista de imágenes a procesar
            filtro: Filtro a aplicar
            directorio_salida: Directorio de salida
            
        Returns:
            Diccionario con comparación de rendimientos
        """
        print("\n" + "="*60)
        print("COMPARACIÓN DE RENDIMIENTO: THREADS vs PROCESOS")
        print("="*60)
        
        # Test con threads
        dir_threads = os.path.join(directorio_salida, "test_threads")
        stats_threads = self.procesar_con_threads(imagenes, filtro, dir_threads)
        
        # Reiniciar estadísticas
        self.estadisticas = {
            'exitosas': 0,
            'fallidas': 0,
            'tiempo_total': 0,
            'nucleos_usados': self.num_nucleos
        }
        
        # Test con procesos
        dir_procesos = os.path.join(directorio_salida, "test_procesos")
        stats_procesos = self.procesar_con_procesos(imagenes, filtro, dir_procesos)
        
        # Calcular mejora
        mejora = ((stats_threads['tiempo_total'] - stats_procesos['tiempo_total']) 
                  / stats_threads['tiempo_total'] * 100)
        
        comparacion = {
            'threads': stats_threads,
            'procesos': stats_procesos,
            'mejora_porcentual': round(mejora, 2),
            'ganador': 'procesos' if stats_procesos['tiempo_total'] < stats_threads['tiempo_total'] else 'threads'
        }
        
        print("\n" + "="*60)
        print("RESULTADOS DE LA COMPARACIÓN")
        print("="*60)
        print(f"⏱️  Tiempo con THREADS: {stats_threads['tiempo_total']:.2f} segundos")
        print(f"⏱️  Tiempo con PROCESOS: {stats_procesos['tiempo_total']:.2f} segundos")
        print(f"📈 Mejora: {mejora:.2f}% {'más rápido' if mejora > 0 else 'más lento'}")
        print(f"🏆 Ganador: {comparacion['ganador'].upper()}")
        print("="*60)
        
        return comparacion


def obtener_imagenes_directorio(directorio, extensiones=None):
    """
    Obtiene todas las imágenes de un directorio
    
    Args:
        directorio: Ruta del directorio
        extensiones: Lista de extensiones permitidas (default: jpg, jpeg, png, bmp, gif)
        
    Returns:
        Lista de rutas de imágenes
    """
    if extensiones is None:
        extensiones = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    
    imagenes = []
    
    if not os.path.exists(directorio):
        print(f"⚠️  El directorio {directorio} no existe")
        return imagenes
    
    for archivo in os.listdir(directorio):
        ext = os.path.splitext(archivo)[1].lower()
        if ext in extensiones:
            ruta_completa = os.path.join(directorio, archivo)
            imagenes.append(ruta_completa)
    
    return imagenes


# Función de callback de ejemplo
def callback_ejemplo(info):
    """
    Función de callback de ejemplo para mostrar progreso
    """
    print(f"[{info['porcentaje']:.1f}%] {info['imagen']} - {info['estado']} - {info['mensaje']}")


if __name__ == "__main__":
    """
    Script principal para ejecutar el procesador de imágenes
    """
    # Configuración
    DIR_ENTRADA = "../input_images"
    DIR_SALIDA = "../output_images"
    
    # Crear procesador
    procesador = ProcesadorImagenes(callback_progreso=callback_ejemplo)
    
    # Obtener imágenes
    imagenes = obtener_imagenes_directorio(DIR_ENTRADA)
    
    if not imagenes:
        print("⚠️  No se encontraron imágenes en el directorio de entrada")
        print(f"📁 Coloca imágenes en: {os.path.abspath(DIR_ENTRADA)}")
    else:
        print(f"\n✅ Se encontraron {len(imagenes)} imágenes")
        
        # Ejemplo 1: Procesar con un filtro usando procesos
        print("\n" + "="*60)
        print("EJEMPLO 1: Procesamiento con procesos paralelos")
        print("="*60)
        stats = procesador.procesar_con_procesos(imagenes, 'blur', DIR_SALIDA)
        
        print("\n📊 ESTADÍSTICAS FINALES:")
        print(f"✅ Exitosas: {stats['exitosas']}")
        print(f"❌ Fallidas: {stats['fallidas']}")
        print(f"⏱️  Tiempo total: {stats['tiempo_total']:.2f} segundos")
        print(f"⚡ Imágenes/segundo: {stats['exitosas']/stats['tiempo_total']:.2f}")
        
        # Ejemplo 2: Procesar múltiples filtros
        if len(imagenes) >= 3:
            print("\n" + "="*60)
            print("EJEMPLO 2: Batch con múltiples filtros")
            print("="*60)
            
            # Reiniciar estadísticas
            procesador.estadisticas = {
                'exitosas': 0,
                'fallidas': 0,
                'tiempo_total': 0,
                'nucleos_usados': procesador.num_nucleos
            }
            
            filtros = ['grises', 'sepia', 'invertir']
            resultados = procesador.procesar_batch(imagenes[:3], filtros, DIR_SALIDA)
            
            print("\n📊 RESUMEN FINAL:")
            for resultado in resultados:
                print(f"\n🎨 Filtro: {resultado['filtro']}")
                print(f"   ⏱️  Tiempo: {resultado['tiempo_total']:.2f}s")
                print(f"   ✅ Exitosas: {resultado['exitosas']}")
