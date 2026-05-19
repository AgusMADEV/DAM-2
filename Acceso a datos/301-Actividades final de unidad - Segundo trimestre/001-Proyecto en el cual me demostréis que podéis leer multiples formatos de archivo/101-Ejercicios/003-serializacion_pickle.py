"""
RESTAURANTES DE ESPAÑA - Versión 3.0
Serialización con Pickle (Binario)

Implementa serialización y deserialización de objetos complejos usando pickle.
Permite guardar y recuperar objetos Python completos incluyendo clases personalizadas.
"""

import pickle
import os
from datetime import datetime


class Restaurante:
    """Clase que representa un restaurante con todas sus propiedades"""
    
    def __init__(self, cif, nombre, chef, ciudad, tipo_cocina, estrellas_michelin, precio_medio):
        self.cif = cif
        self.nombre = nombre
        self.chef = chef
        self.ciudad = ciudad
        self.tipo_cocina = tipo_cocina
        self.estrellas_michelin = estrellas_michelin
        self.precio_medio = precio_medio
        self.fecha_registro = datetime.now()
        self.reservas = []
        self.reseñas = []
    
    def agregar_reserva(self, cliente, fecha_reserva, num_comensales=2):
        """Registra una reserva en el restaurante"""
        reserva = {
            "cliente": cliente,
            "fecha_reserva": fecha_reserva,
            "num_comensales": num_comensales,
            "fecha_registro": datetime.now()
        }
        self.reservas.append(reserva)
    
    def agregar_reseña(self, usuario, calificacion, comentario):
        """Agrega una reseña al restaurante"""
        reseña = {
            "usuario": usuario,
            "calificacion": calificacion,
            "comentario": comentario,
            "fecha": datetime.now()
        }
        self.reseñas.append(reseña)
    
    def acepta_reservas(self):
        """Verifica si el restaurante acepta reservas"""
        return True  # Todos aceptan reservas por defecto
    
    def calificacion_promedio(self):
        """Calcula la calificación promedio del restaurante"""
        if not self.reseñas:
            return 0
        total = sum(r['calificacion'] for r in self.reseñas)
        return round(total / len(self.reseñas), 2)
    
    def __str__(self):
        estrellas = "⭐"*int(self.estrellas_michelin) if self.estrellas_michelin.isdigit() else ""
        return f"{self.nombre} - {self.chef} ({self.ciudad}) {estrellas}"
    
    def __repr__(self):
        return f"Restaurante('{self.cif}', '{self.nombre}')"


class SistemaRestaurantesBinario:
    """Gestión de restaurantes usando serialización binaria con pickle"""
    
    def __init__(self, ruta_base="restaurantes_datos"):
        self.ruta_base = ruta_base
        self.ruta_binario = f"{ruta_base}/binario"
        self._asegurar_directorio()
        self.restaurantes = []
    
    def _asegurar_directorio(self):
        """Asegura que exista el directorio de archivos binarios"""
        try:
            os.makedirs(self.ruta_binario, exist_ok=True)
        except Exception as e:
            print(f"Error al crear directorio: {e}")
    
    def guardar_restaurante_binario(self, restaurante, nombre_archivo=None):
        """
        Serializa y guarda un objeto Restaurante en formato binario
        
        Args:
            restaurante: Objeto de la clase Restaurante
            nombre_archivo: Nombre del archivo (opcional, usa CIF si no se especifica)
            
        Returns:
            Boolean indicando éxito
        """
        if not nombre_archivo:
            # Usar CIF como nombre de archivo, reemplazando caracteres no válidos
            nombre_archivo = restaurante.cif.replace("-", "_") + ".pkl"
        
        ruta_completa = f"{self.ruta_binario}/{nombre_archivo}"
        
        try:
            with open(ruta_completa, 'wb') as archivo:
                pickle.dump(restaurante, archivo)
            print(f"✓ Restaurante serializado y guardado: {nombre_archivo}")
            return True
        except Exception as e:
            print(f"✗ Error al guardar restaurante: {e}")
            return False
    
    def cargar_restaurante_binario(self, nombre_archivo):
        """
        Deserializa y carga un objeto Restaurante desde archivo binario
        
        Args:
            nombre_archivo: Nombre del archivo .pkl
            
        Returns:
            Objeto Restaurante deserializado o None si hay error
        """
        ruta_completa = f"{self.ruta_binario}/{nombre_archivo}"
        
        try:
            with open(ruta_completa, 'rb') as archivo:
                restaurante = pickle.load(archivo)
            print(f"✓ Restaurante deserializado: {restaurante.nombre}")
            return restaurante
        except FileNotFoundError:
            print(f"✗ Archivo no encontrado: {nombre_archivo}")
            return None
        except Exception as e:
            print(f"✗ Error al cargar restaurante: {e}")
            return None
    
    def guardar_coleccion_completa(self, restaurantes, nombre_archivo="restaurantes_completos.pkl"):
        """
        Guarda una colección completa de restaurantes en un solo archivo
        
        Args:
            restaurantes: Lista de objetos Restaurante
            nombre_archivo: Nombre del archivo
            
        Returns:
            Boolean indicando éxito
        """
        ruta_completa = f"{self.ruta_binario}/{nombre_archivo}"
        
        try:
            with open(ruta_completa, 'wb') as archivo:
                pickle.dump(restaurantes, archivo)
            print(f"✓ Colección de {len(restaurantes)} restaurantes guardada")
            return True
        except Exception as e:
            print(f"✗ Error al guardar colección: {e}")
            return False
    
    def cargar_coleccion_completa(self, nombre_archivo="restaurantes_completos.pkl"):
        """
        Carga una colección completa de restaurantes desde un archivo
        
        Args:
            nombre_archivo: Nombre del archivo
            
        Returns:
            Lista de objetos Restaurante o lista vacía si hay error
        """
        ruta_completa = f"{self.ruta_binario}/{nombre_archivo}"
        
        try:
            with open(ruta_completa, 'rb') as archivo:
                restaurantes = pickle.load(archivo)
            print(f"✓ Colección de {len(restaurantes)} restaurantes cargada")
            return restaurantes
        except FileNotFoundError:
            print(f"✗ Archivo no encontrado: {nombre_archivo}")
            return []
        except Exception as e:
            print(f"✗ Error al cargar colección: {e}")
            return []
    
    def guardar_estado_sistema(self, nombre_archivo="estado_sistema.pkl"):
        """
        Guarda el estado completo del sistema (self)
        
        Args:
            nombre_archivo: Nombre del archivo
            
        Returns:
            Boolean indicando éxito
        """
        ruta_completa = f"{self.ruta_binario}/{nombre_archivo}"
        
        try:
            with open(ruta_completa, 'wb') as archivo:
                pickle.dump(self, archivo)
            print(f"✓ Estado completo del sistema guardado")
            return True
        except Exception as e:
            print(f"✗ Error al guardar estado: {e}")
            return False
    
    @staticmethod
    def cargar_estado_sistema(ruta_base="restaurantes_datos", 
                              nombre_archivo="estado_sistema.pkl"):
        """
        Carga el estado completo de un sistema guardado
        
        Args:
            ruta_base: Ruta base del sistema
            nombre_archivo: Nombre del archivo
            
        Returns:
            Objeto SistemaRestaurantesBinario o None si hay error
        """
        ruta_completa = f"{ruta_base}/binario/{nombre_archivo}"
        
        try:
            with open(ruta_completa, 'rb') as archivo:
                sistema = pickle.load(archivo)
            print(f"✓ Estado completo del sistema cargado")
            return sistema
        except FileNotFoundError:
            print(f"✗ Archivo no encontrado: {nombre_archivo}")
            return None
        except Exception as e:
            print(f"✗ Error al cargar estado: {e}")
            return None


def demo_serializacion_pickle():
    """Demostración del sistema de serialización con pickle"""
    print("\n" + "="*60)
    print("DEMOSTRACIÓN: Serialización Binaria con Pickle")
    print("="*60)
    
    sistema = SistemaRestaurantesBinario()
    
    # Leer restaurantes desde el CSV
    print("\n📖 Leyendo datos desde el archivo CSV...")
    print("-" * 60)
    import csv
    restaurantes_csv = []
    try:
        with open("restaurantes_datos/texto/restaurantes.csv", 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            restaurantes_csv = list(lector)
        print(f"✓ {len(restaurantes_csv)} restaurantes leídos desde CSV")
    except FileNotFoundError:
        print("✗ Archivo CSV no encontrado")
        return
    except Exception as e:
        print(f"✗ Error al leer CSV: {e}")
        return
    
    # 1. Crear objetos Restaurante complejos desde CSV
    print("\n1. Creando objetos Restaurante con datos del CSV...")
    print("-" * 60)
    
    # Procesar TODOS los restaurantes del CSV
    objetos_restaurante = []
    for i, datos in enumerate(restaurantes_csv):
        rest = Restaurante(
            cif=datos['cif'],
            nombre=datos['nombre'],
            chef=datos['chef'],
            ciudad=datos['ciudad'],
            tipo_cocina=datos['tipo_cocina'],
            estrellas_michelin=datos['estrellas_michelin'],
            precio_medio=datos['precio_medio']
        )
        # Agregar algunas reseñas de ejemplo
        rest.agregar_reseña("Usuario de prueba", 5, "Excelente restaurante")
        if i == 0:
            rest.agregar_reserva("Cliente Ejemplo", datetime(2026, 4, 15), 2)
        objetos_restaurante.append(rest)
        # Mostrar solo los primeros 5 para no saturar la pantalla
        if i < 5:
            print(f"✓ Creado: {rest}")
            print(f"  - {len(rest.reseñas)} reseña(s), calificación: {rest.calificacion_promedio()}/5")
        elif i == 5:
            print(f"... procesando los {len(restaurantes_csv) - 5} restaurantes restantes ...")
    
    print(f"\n✓ Total de objetos Restaurante creados: {len(objetos_restaurante)}")
    
    # Usar el primer restaurante para las demos posteriores
    rest1, rest2, rest3 = objetos_restaurante[0], objetos_restaurante[1], objetos_restaurante[2]
    
    # 1.5. Limpiar archivos pickle antiguos
    print("\n🧹 Limpiando archivos pickle antiguos...")
    print("-" * 60)
    try:
        archivos_eliminados = 0
        # Listar todos los archivos en el directorio binario
        if os.path.exists(sistema.ruta_binario):
            for archivo in os.listdir(sistema.ruta_binario):
                if archivo.endswith('.pkl'):
                    ruta_archivo = os.path.join(sistema.ruta_binario, archivo)
                    os.remove(ruta_archivo)
                    print(f"  ✓ Eliminado: {archivo}")
                    archivos_eliminados += 1
        print(f"✓ Total: {archivos_eliminados} archivos antiguos eliminados")
    except Exception as e:
        print(f"⚠ Error al limpiar archivos: {e}")
    
    # 2. Guardar restaurantes individualmente
    print("\n2. Serializando restaurantes individuales...")
    print("-" * 60)
    for i, rest in enumerate(objetos_restaurante):
        sistema.guardar_restaurante_binario(rest)
        # Mostrar solo los primeros 5 para no saturar la pantalla
        if i >= 5:
            break
    
    if len(objetos_restaurante) > 5:
        print(f"... serializando los {len(objetos_restaurante) - 5} restaurantes restantes ...")
        for rest in objetos_restaurante[5:]:
            sistema.guardar_restaurante_binario(rest)
    
    print(f"\n✓ Total: {len(objetos_restaurante)} restaurantes serializados individualmente")
    
    # 3. Cargar un restaurante individual
    print("\n3. Deserializando un restaurante individual...")
    print("-" * 60)
    # Usar el CIF del segundo restaurante
    nombre_archivo = rest2.cif.replace("-", "_") + ".pkl"
    rest_cargado = sistema.cargar_restaurante_binario(nombre_archivo)
    if rest_cargado:
        print(f"Nombre: {rest_cargado.nombre}")
        print(f"Chef: {rest_cargado.chef}")
        print(f"Calificación: {rest_cargado.calificacion_promedio()}/5")
        print(f"Estrellas: {'⭐'*int(rest_cargado.estrellas_michelin)}")
        print(f"Fecha de registro: {rest_cargado.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 4. Guardar colección completa
    print("\n4. Guardando colección completa...")
    print("-" * 60)
    sistema.guardar_coleccion_completa(objetos_restaurante)
    
    # 5. Cargar colección completa
    print("\n5. Cargando colección completa...")
    print("-" * 60)
    restaurantes_cargados = sistema.cargar_coleccion_completa()
    print(f"\nMostrando primeros 5 de {len(restaurantes_cargados)}:")
    for i, rest in enumerate(restaurantes_cargados[:5]):
        estrellas = "⭐"*int(rest.estrellas_michelin)
        print(f"{estrellas} {rest.nombre} ({rest.ciudad}) - Calificación: {rest.calificacion_promedio()}/5")
    if len(restaurantes_cargados) > 5:
        print(f"... y {len(restaurantes_cargados) - 5} restaurantes más")
    
    # 6. Demostrar ventajas de pickle
    print("\n6. Ventajas de la serialización con pickle...")
    print("-" * 60)
    print("✓ Guarda objetos Python completos (no solo datos)")
    print("✓ Preserva tipos de datos complejos (datetime, listas, etc.)")
    print("✓ Mantiene las relaciones entre objetos")
    print("✓ Más eficiente en espacio que JSON para objetos complejos")
    print("✓ Más rápido que JSON para serialización/deserialización")
    print("\n⚠️  Advertencia: Solo usar pickle con datos de confianza")
    print("   (riesgo de seguridad con archivos de origen desconocido)")
    
    # 7. Comparación de tamaños
    print("\n7. Comparación con formato JSON...")
    print("-" * 60)
    import json
    
    # Intentar convertir a JSON (perderá información)
    try:
        rest_dict = {
            "cif": rest1.cif,
            "nombre": rest1.nombre,
            "chef": rest1.chef,
            "ciudad": rest1.ciudad,
            "tipo_cocina": rest1.tipo_cocina,
            "estrellas_michelin": rest1.estrellas_michelin,
            "precio_medio": rest1.precio_medio
        }
        json_str = json.dumps(rest_dict, indent=2, ensure_ascii=False)
        print("JSON (solo datos básicos):")
        print(f"  Tamaño: {len(json_str)} caracteres")
        print(f"  ✗ Se pierden: reseñas, reservas, fecha_registro, métodos")
        
        # Tamaño del pickle
        import sys
        pickle_bytes = pickle.dumps(rest1)
        print(f"\nPickle (objeto completo):")
        print(f"  Tamaño: {len(pickle_bytes)} bytes")
        print(f"  ✓ Se preserva TODO: reseñas, reservas, métodos, etc.")
        
    except Exception as e:
        print(f"Error en comparación: {e}")


if __name__ == "__main__":
    demo_serializacion_pickle()
