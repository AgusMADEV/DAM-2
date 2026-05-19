"""
BIBLIOTECA DIGITAL - Versión 4.0
Esteganografía en Imágenes

Implementa ocultación de información en imágenes usando el bit menos significativo (LSB).
Permite codificar y decodificar datos de libros en imágenes de manera invisible.
"""

import os
from PIL import Image
import json


class Esteganografia:
    """Clase para codificar y decodificar información en imágenes"""
    
    def __init__(self, ruta_base="restaurantes_datos"):
        self.ruta_base = ruta_base
        self.ruta_imagenes = f"{ruta_base}/imagenes"
        self._asegurar_directorio()
    
    def _asegurar_directorio(self):
        """Asegura que exista el directorio de imágenes"""
        try:
            os.makedirs(self.ruta_imagenes, exist_ok=True)
        except Exception as e:
            print(f"Error al crear directorio: {e}")
    
    def texto_a_binario(self, texto):
        """
        Convierte texto a representación binaria
        
        Args:
            texto: String a convertir
            
        Returns:
            String con la representación binaria
        """
        return ''.join(format(ord(char), '08b') for char in texto)
    
    def binario_a_texto(self, binario):
        """
        Convierte binario a texto
        
        Args:
            binario: String con representación binaria
            
        Returns:
            Texto decodificado
        """
        texto = ''
        for i in range(0, len(binario), 8):
            byte = binario[i:i+8]
            if len(byte) == 8:
                texto += chr(int(byte, 2))
        return texto
    
    def codificar_imagen(self, ruta_imagen_original, datos, ruta_imagen_salida=None):
        """
        Codifica información en una imagen usando LSB (Least Significant Bit)
        
        Args:
            ruta_imagen_original: Ruta de la imagen base
            datos: Datos a ocultar (puede ser dict, str, etc.)
            ruta_imagen_salida: Ruta donde guardar la imagen codificada
            
        Returns:
            Boolean indicando éxito
        """
        try:
            # Convertir datos a JSON si es un diccionario
            if isinstance(datos, dict):
                mensaje = json.dumps(datos, ensure_ascii=False)
            else:
                mensaje = str(datos)
            
            # Agregar delimitador para saber dónde termina el mensaje
            mensaje += "<<<FIN>>>"
            
            # Convertir mensaje a binario
            mensaje_binario = self.texto_a_binario(mensaje)
            
            # Cargar imagen
            imagen = Image.open(ruta_imagen_original)
            
            # Verificar si la imagen puede almacenar el mensaje
            pixeles_necesarios = len(mensaje_binario)
            pixeles_disponibles = imagen.size[0] * imagen.size[1] * 3  # RGB
            
            if pixeles_necesarios > pixeles_disponibles:
                print(f"✗ Error: La imagen es muy pequeña para el mensaje")
                print(f"  Necesarios: {pixeles_necesarios} bits")
                print(f"  Disponibles: {pixeles_disponibles} bits")
                return False
            
            # Convertir imagen a RGB si no lo es
            if imagen.mode != 'RGB':
                imagen = imagen.convert('RGB')
            
            # Obtener píxeles
            pixeles = list(imagen.getdata())
            
            # Codificar mensaje en los píxeles
            indice_mensaje = 0
            pixeles_modificados = []
            
            for pixel in pixeles:
                if indice_mensaje < len(mensaje_binario):
                    # Modificar cada componente RGB
                    r, g, b = pixel
                    
                    # Modificar bit menos significativo del rojo
                    if indice_mensaje < len(mensaje_binario):
                        r = (r & 0xFE) | int(mensaje_binario[indice_mensaje])
                        indice_mensaje += 1
                    
                    # Modificar bit menos significativo del verde
                    if indice_mensaje < len(mensaje_binario):
                        g = (g & 0xFE) | int(mensaje_binario[indice_mensaje])
                        indice_mensaje += 1
                    
                    # Modificar bit menos significativo del azul
                    if indice_mensaje < len(mensaje_binario):
                        b = (b & 0xFE) | int(mensaje_binario[indice_mensaje])
                        indice_mensaje += 1
                    
                    pixeles_modificados.append((r, g, b))
                else:
                    pixeles_modificados.append(pixel)
            
            # Crear nueva imagen con píxeles modificados
            imagen_codificada = Image.new(imagen.mode, imagen.size)
            imagen_codificada.putdata(pixeles_modificados)
            
            # Guardar imagen
            if not ruta_imagen_salida:
                nombre_base = os.path.basename(ruta_imagen_original)
                nombre_sin_ext = os.path.splitext(nombre_base)[0]
                ruta_imagen_salida = f"{self.ruta_imagenes}/{nombre_sin_ext}_codificada.png"
            
            imagen_codificada.save(ruta_imagen_salida, 'PNG')
            
            print(f"✓ Datos codificados exitosamente en la imagen")
            print(f"  Mensaje: {len(mensaje)} caracteres")
            print(f"  Imagen guardada en: {ruta_imagen_salida}")
            
            return True
            
        except FileNotFoundError:
            print(f"✗ Error: Imagen no encontrada: {ruta_imagen_original}")
            return False
        except Exception as e:
            print(f"✗ Error al codificar imagen: {e}")
            return False
    
    def decodificar_imagen(self, ruta_imagen_codificada):
        """
        Decodifica información oculta en una imagen
        
        Args:
            ruta_imagen_codificada: Ruta de la imagen con datos ocultos
            
        Returns:
            Datos decodificados o None si hay error
        """
        try:
            # Cargar imagen
            imagen = Image.open(ruta_imagen_codificada)
            
            # Convertir a RGB si es necesario
            if imagen.mode != 'RGB':
                imagen = imagen.convert('RGB')
            
            # Obtener píxeles
            pixeles = list(imagen.getdata())
            
            # Extraer bits
            mensaje_binario = ''
            
            for pixel in pixeles:
                r, g, b = pixel
                
                # Extraer bit menos significativo de cada componente
                mensaje_binario += str(r & 1)
                mensaje_binario += str(g & 1)
                mensaje_binario += str(b & 1)
            
            # Convertir binario a texto
            mensaje = self.binario_a_texto(mensaje_binario)
            
            # Buscar delimitador de fin
            delimitador = "<<<FIN>>>"
            fin = mensaje.find(delimitador)
            
            if fin != -1:
                mensaje = mensaje[:fin]
                print(f"✓ Datos decodificados exitosamente")
                print(f"  Longitud: {len(mensaje)} caracteres")
                
                # Intentar parsear como JSON
                try:
                    datos = json.loads(mensaje)
                    return datos
                except:
                    return mensaje
            else:
                print(f"✗ No se encontró el delimitador de fin")
                return None
                
        except FileNotFoundError:
            print(f"✗ Error: Imagen no encontrada: {ruta_imagen_codificada}")
            return None
        except Exception as e:
            print(f"✗ Error al decodificar imagen: {e}")
            return None
    
    def crear_imagen_base(self, ancho=800, alto=600, color=(255, 255, 255), 
                          nombre="imagen_base.png"):
        """
        Crea una imagen base simple para usar en demos
        
        Args:
            ancho: Ancho de la imagen
            alto: Alto de la imagen
            color: Color RGB de fondo
            nombre: Nombre del archivo
            
        Returns:
            Ruta de la imagen creada
        """
        try:
            imagen = Image.new('RGB', (ancho, alto), color)
            ruta = f"{self.ruta_imagenes}/{nombre}"
            imagen.save(ruta, 'PNG')
            print(f"✓ Imagen base creada: {ruta}")
            return ruta
        except Exception as e:
            print(f"✗ Error al crear imagen base: {e}")
            return None
    
    def comparar_imagenes_visualmente(self, ruta1, ruta2):
        """
        Compara dos imágenes píxel por píxel y muestra diferencias
        
        Args:
            ruta1: Ruta de la primera imagen
            ruta2: Ruta de la segunda imagen
        """
        try:
            img1 = Image.open(ruta1)
            img2 = Image.open(ruta2)
            
            if img1.size != img2.size:
                print("✗ Las imágenes tienen diferentes tamaños")
                return
            
            pixeles1 = list(img1.getdata())
            pixeles2 = list(img2.getdata())
            
            diferencias = 0
            for p1, p2 in zip(pixeles1, pixeles2):
                if p1 != p2:
                    diferencias += 1
            
            total_pixeles = len(pixeles1)
            porcentaje = (diferencias / total_pixeles) * 100
            
            print(f"Comparación de imágenes:")
            print(f"  Total píxeles: {total_pixeles}")
            print(f"  Píxeles diferentes: {diferencias}")
            print(f"  Porcentaje de cambio: {porcentaje:.6f}%")
            print(f"  ⚠️  Cambio imperceptible al ojo humano (<{porcentaje:.1f}%)")
            
        except Exception as e:
            print(f"✗ Error al comparar imágenes: {e}")


def demo_esteganografia():
    """Demostración del sistema de esteganografía"""
    print("\n" + "="*60)
    print("DEMOSTRACIÓN: Esteganografía en Imágenes")
    print("="*60)
    
    esteg = Esteganografia()
    
    # 1. Crear imagen base para la demostración
    print("\n1. Creando imagen base para la demostración...")
    print("-" * 60)
    ruta_base = esteg.crear_imagen_base(
        ancho=800, 
        alto=600, 
        color=(135, 206, 235),  # Azul cielo
        nombre="portada_biblioteca.png"
    )
    
    # 2. Preparar datos de un libro para ocultar
    print("\n2. Preparando datos secretos del libro...")
    print("-" * 60)
    libro_secreto = {
        "isbn": "978-0-13-110362-7",
        "titulo": "El Quijote",
        "autor": "Miguel de Cervantes",
        "año": "1605",
        "genero": "Novela",
        "paginas": 863,
        "editorial": "Francisco de Robles",
        "ubicacion_secreta": "Estantería 3, Fila 2, Posición 7",
        "valor_estimado": "15000 EUR",
        "edicion": "Primera edición original"
    }
    
    print("Datos a ocultar:")
    for clave, valor in libro_secreto.items():
        print(f"  {clave}: {valor}")
    
    # 3. Codificar datos en la imagen
    print("\n3. Codificando datos en la imagen...")
    print("-" * 60)
    if ruta_base:
        exito = esteg.codificar_imagen(
            ruta_imagen_original=ruta_base,
            datos=libro_secreto,
            ruta_imagen_salida=f"{esteg.ruta_imagenes}/portada_con_datos.png"
        )
        
        if exito:
            # 4. Comparar imágenes
            print("\n4. Comparando imagen original vs codificada...")
            print("-" * 60)
            esteg.comparar_imagenes_visualmente(
                ruta_base,
                f"{esteg.ruta_imagenes}/portada_con_datos.png"
            )
            
            # 5. Decodificar datos
            print("\n5. Decodificando datos ocultos...")
            print("-" * 60)
            datos_recuperados = esteg.decodificar_imagen(
                f"{esteg.ruta_imagenes}/portada_con_datos.png"
            )
            
            if datos_recuperados:
                print("\nDatos recuperados:")
                for clave, valor in datos_recuperados.items():
                    print(f"  {clave}: {valor}")
                
                # Verificar integridad
                print("\n6. Verificando integridad de los datos...")
                print("-" * 60)
                if datos_recuperados == libro_secreto:
                    print("✓ ¡Datos recuperados correctamente!")
                    print("✓ La información coincide 100% con el original")
                else:
                    print("✗ Hay diferencias en los datos")
    
    # 7. Explicación técnica
    print("\n7. Explicación técnica del proceso...")
    print("-" * 60)
    print("""
    Esteganografía LSB (Least Significant Bit):
    
    1. Cada píxel RGB tiene 3 valores (0-255)
    2. Se modifica el bit menos significativo de cada valor
    3. Cambio máximo por componente: ±1 (imperceptible)
    4. Capacidad: 3 bits por píxel
    
    Ejemplo:
    - Rojo original: 135 (10000111 en binario)
    - Bit a ocultar: 1
    - Rojo modificado: 135 (10000111) - Sin cambio si ya era 1
    
    Ventajas:
    ✓ Invisible al ojo humano
    ✓ No afecta la calidad de la imagen
    ✓ Difícil de detectar sin análisis forense
    
    Usos en la biblioteca:
    - Ocultar ubicaciones de libros raros
    - Proteger datos sensibles de valoración
    - Marcas de agua digitales invisibles
    - Sistema de autenticación de documentos
    """)
    
    print("\n8. Cálculo de capacidad...")
    print("-" * 60)
    ancho, alto = 800, 600
    pixeles_totales = ancho * alto
    bits_disponibles = pixeles_totales * 3
    caracteres_max = bits_disponibles // 8
    print(f"Imagen de {ancho}x{alto} píxeles:")
    print(f"  Píxeles: {pixeles_totales:,}")
    print(f"  Bits disponibles: {bits_disponibles:,}")
    print(f"  Capacidad máxima: {caracteres_max:,} caracteres")
    print(f"  Equivalente a: ~{caracteres_max/1024:.1f} KB de texto")


if __name__ == "__main__":
    demo_esteganografia()
