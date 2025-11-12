"""
Módulo de filtros para procesamiento de imágenes
Implementa diversos filtros aplicables a imágenes usando PIL/Pillow
"""

from PIL import Image, ImageFilter, ImageEnhance
import os

class FiltrosImagen:
    """
    Clase que contiene todos los filtros disponibles para aplicar a las imágenes
    Cada método es un filtro diferente que puede ser aplicado de forma paralela
    """
    
    @staticmethod
    def invertir_colores(imagen):
        """
        Invierte los colores de la imagen (negativo)
        
        Args:
            imagen: Objeto PIL Image
            
        Returns:
            Imagen con colores invertidos
        """
        pixels = imagen.load()
        width, height = imagen.size
        
        for x in range(width):
            for y in range(height):
                pixel = imagen.getpixel((x, y))
                if isinstance(pixel, tuple) and len(pixel) >= 3:
                    pixels[x, y] = (255 - pixel[0], 255 - pixel[1], 255 - pixel[2])
                    
        return imagen
    
    @staticmethod
    def escala_grises(imagen):
        """
        Convierte la imagen a escala de grises
        
        Args:
            imagen: Objeto PIL Image
            
        Returns:
            Imagen en escala de grises
        """
        return imagen.convert('L').convert('RGB')
    
    @staticmethod
    def blur(imagen, radio=5):
        """
        Aplica efecto de desenfoque (blur) a la imagen
        
        Args:
            imagen: Objeto PIL Image
            radio: Intensidad del blur (default: 5)
            
        Returns:
            Imagen con efecto blur
        """
        return imagen.filter(ImageFilter.GaussianBlur(radius=radio))
    
    @staticmethod
    def nitidez(imagen, factor=2.0):
        """
        Aumenta la nitidez de la imagen
        
        Args:
            imagen: Objeto PIL Image
            factor: Factor de nitidez (default: 2.0)
            
        Returns:
            Imagen con mayor nitidez
        """
        enhancer = ImageEnhance.Sharpness(imagen)
        return enhancer.enhance(factor)
    
    @staticmethod
    def brillo(imagen, factor=1.5):
        """
        Ajusta el brillo de la imagen
        
        Args:
            imagen: Objeto PIL Image
            factor: Factor de brillo (default: 1.5)
            
        Returns:
            Imagen con brillo ajustado
        """
        enhancer = ImageEnhance.Brightness(imagen)
        return enhancer.enhance(factor)
    
    @staticmethod
    def contraste(imagen, factor=1.5):
        """
        Ajusta el contraste de la imagen
        
        Args:
            imagen: Objeto PIL Image
            factor: Factor de contraste (default: 1.5)
            
        Returns:
            Imagen con contraste ajustado
        """
        enhancer = ImageEnhance.Contrast(imagen)
        return enhancer.enhance(factor)
    
    @staticmethod
    def sepia(imagen):
        """
        Aplica un filtro sepia vintage a la imagen
        
        Args:
            imagen: Objeto PIL Image
            
        Returns:
            Imagen con efecto sepia
        """
        pixels = imagen.load()
        width, height = imagen.size
        
        for x in range(width):
            for y in range(height):
                pixel = imagen.getpixel((x, y))
                if isinstance(pixel, tuple) and len(pixel) >= 3:
                    r, g, b = pixel[0], pixel[1], pixel[2]
                    
                    # Fórmula sepia
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                    
                    # Asegurar que los valores estén en el rango 0-255
                    pixels[x, y] = (min(255, tr), min(255, tg), min(255, tb))
                    
        return imagen
    
    @staticmethod
    def detectar_bordes(imagen):
        """
        Detecta y resalta los bordes de la imagen
        
        Args:
            imagen: Objeto PIL Image
            
        Returns:
            Imagen con bordes detectados
        """
        return imagen.filter(ImageFilter.FIND_EDGES)
    
    @staticmethod
    def relieve(imagen):
        """
        Aplica efecto de relieve a la imagen
        
        Args:
            imagen: Objeto PIL Image
            
        Returns:
            Imagen con efecto relieve
        """
        return imagen.filter(ImageFilter.EMBOSS)
    
    @staticmethod
    def posterizar(imagen, bits=4):
        """
        Reduce el número de colores en la imagen (efecto poster)
        
        Args:
            imagen: Objeto PIL Image
            bits: Número de bits por canal (default: 4)
            
        Returns:
            Imagen posterizada
        """
        from PIL import ImageOps
        return ImageOps.posterize(imagen, bits)
    
    @staticmethod
    def redimensionar(imagen, porcentaje=50):
        """
        Redimensiona la imagen a un porcentaje del tamaño original
        
        Args:
            imagen: Objeto PIL Image
            porcentaje: Porcentaje del tamaño original (default: 50)
            
        Returns:
            Imagen redimensionada
        """
        width, height = imagen.size
        nuevo_ancho = int(width * porcentaje / 100)
        nuevo_alto = int(height * porcentaje / 100)
        return imagen.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
    
    @staticmethod
    def marca_agua(imagen, texto="PROCESADO", opacidad=0.3):
        """
        Añade una marca de agua a la imagen
        
        Args:
            imagen: Objeto PIL Image
            texto: Texto de la marca de agua (default: "PROCESADO")
            opacidad: Opacidad de la marca (default: 0.3)
            
        Returns:
            Imagen con marca de agua
        """
        from PIL import ImageDraw, ImageFont
        
        # Crear una capa transparente
        marca = Image.new('RGBA', imagen.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(marca)
        
        # Intentar usar una fuente del sistema, si no, usar la predeterminada
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        # Calcular posición centrada
        bbox = draw.textbbox((0, 0), texto, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        width, height = imagen.size
        posicion = ((width - text_width) // 2, (height - text_height) // 2)
        
        # Dibujar texto con opacidad
        alpha = int(255 * opacidad)
        draw.text(posicion, texto, fill=(255, 255, 255, alpha), font=font)
        
        # Combinar con la imagen original
        imagen_rgba = imagen.convert('RGBA')
        resultado = Image.alpha_composite(imagen_rgba, marca)
        
        return resultado.convert('RGB')
    
    @staticmethod
    def obtener_filtros_disponibles():
        """
        Retorna un diccionario con todos los filtros disponibles
        
        Returns:
            Dict con nombre del filtro y su función
        """
        return {
            'invertir': FiltrosImagen.invertir_colores,
            'grises': FiltrosImagen.escala_grises,
            'blur': FiltrosImagen.blur,
            'nitidez': FiltrosImagen.nitidez,
            'brillo': FiltrosImagen.brillo,
            'contraste': FiltrosImagen.contraste,
            'sepia': FiltrosImagen.sepia,
            'bordes': FiltrosImagen.detectar_bordes,
            'relieve': FiltrosImagen.relieve,
            'posterizar': FiltrosImagen.posterizar,
            'redimensionar': FiltrosImagen.redimensionar,
            'marca_agua': FiltrosImagen.marca_agua
        }


def aplicar_filtro(ruta_entrada, ruta_salida, nombre_filtro, parametros=None):
    """
    Aplica un filtro específico a una imagen
    Función independiente para ser usada en procesamiento paralelo
    
    Args:
        ruta_entrada: Ruta de la imagen de entrada
        ruta_salida: Ruta donde guardar la imagen procesada
        nombre_filtro: Nombre del filtro a aplicar
        parametros: Parámetros adicionales para el filtro (opcional)
        
    Returns:
        True si se procesó correctamente, False en caso contrario
    """
    try:
        # Cargar imagen
        imagen = Image.open(ruta_entrada)
        
        # Obtener el filtro
        filtros = FiltrosImagen.obtener_filtros_disponibles()
        
        if nombre_filtro not in filtros:
            print(f"Filtro '{nombre_filtro}' no encontrado")
            return False
        
        filtro = filtros[nombre_filtro]
        
        # Aplicar filtro
        if parametros:
            imagen_procesada = filtro(imagen.copy(), **parametros)
        else:
            imagen_procesada = filtro(imagen.copy())
        
        # Guardar resultado
        imagen_procesada.save(ruta_salida)
        
        return True
        
    except Exception as e:
        print(f"Error al procesar {ruta_entrada}: {str(e)}")
        return False
