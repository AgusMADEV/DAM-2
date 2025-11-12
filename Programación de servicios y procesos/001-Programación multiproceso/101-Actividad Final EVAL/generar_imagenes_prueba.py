"""
Script para generar imágenes de prueba para el procesador
Crea imágenes de diferentes tamaños y colores
"""

from PIL import Image, ImageDraw, ImageFont
import os
import random

def crear_imagen_gradiente(ancho, alto, color_inicio, color_fin, nombre):
    """Crea una imagen con gradiente de color"""
    imagen = Image.new('RGB', (ancho, alto))
    draw = ImageDraw.Draw(imagen)
    
    for y in range(alto):
        # Interpolar entre colores
        factor = y / alto
        r = int(color_inicio[0] + (color_fin[0] - color_inicio[0]) * factor)
        g = int(color_inicio[1] + (color_fin[1] - color_inicio[1]) * factor)
        b = int(color_inicio[2] + (color_fin[2] - color_inicio[2]) * factor)
        
        draw.line([(0, y), (ancho, y)], fill=(r, g, b))
    
    # Añadir texto
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    texto = f"Imagen de Prueba\n{ancho}x{alto}"
    bbox = draw.textbbox((0, 0), texto, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    posicion = ((ancho - text_width) // 2, (alto - text_height) // 2)
    
    # Fondo para el texto
    draw.rectangle([posicion[0]-10, posicion[1]-10, 
                   posicion[0]+text_width+10, posicion[1]+text_height+10],
                  fill=(0, 0, 0, 128))
    
    draw.text(posicion, texto, fill=(255, 255, 255), font=font)
    
    return imagen

def crear_imagen_geometrica(ancho, alto, nombre):
    """Crea una imagen con formas geométricas"""
    imagen = Image.new('RGB', (ancho, alto), color=(40, 40, 60))
    draw = ImageDraw.Draw(imagen)
    
    # Dibujar círculos aleatorios
    for _ in range(10):
        x = random.randint(0, ancho)
        y = random.randint(0, alto)
        radio = random.randint(20, 100)
        color = (random.randint(100, 255), 
                random.randint(100, 255), 
                random.randint(100, 255))
        draw.ellipse([x-radio, y-radio, x+radio, y+radio], 
                    fill=color, outline=(255, 255, 255))
    
    # Añadir texto
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()
    
    draw.text((20, 20), nombre, fill=(255, 255, 255), font=font)
    
    return imagen

def crear_imagen_patron(ancho, alto, nombre):
    """Crea una imagen con patrón de cuadrícula"""
    imagen = Image.new('RGB', (ancho, alto), color=(255, 255, 255))
    draw = ImageDraw.Draw(imagen)
    
    tamanio_cuadro = 40
    colores = [
        (255, 100, 100), (100, 255, 100), (100, 100, 255),
        (255, 255, 100), (255, 100, 255), (100, 255, 255)
    ]
    
    for x in range(0, ancho, tamanio_cuadro):
        for y in range(0, alto, tamanio_cuadro):
            color = random.choice(colores)
            draw.rectangle([x, y, x+tamanio_cuadro, y+tamanio_cuadro], 
                          fill=color, outline=(0, 0, 0))
    
    # Añadir texto
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()
    
    draw.rectangle([10, 10, 300, 60], fill=(0, 0, 0, 200))
    draw.text((20, 20), nombre, fill=(255, 255, 255), font=font)
    
    return imagen

def main():
    """Función principal para generar imágenes de prueba"""
    
    # Crear directorio si no existe
    directorio = "../101-Actividad Final EVAL/input_images"
    os.makedirs(directorio, exist_ok=True)
    
    print("🎨 Generando imágenes de prueba...")
    print(f"📁 Directorio: {os.path.abspath(directorio)}")
    print("="*60)
    
    imagenes_generadas = []
    
    # Generar 5 imágenes con gradientes
    colores = [
        ((255, 0, 0), (0, 0, 255)),      # Rojo a azul
        ((0, 255, 0), (255, 255, 0)),    # Verde a amarillo
        ((128, 0, 128), (255, 192, 203)), # Púrpura a rosa
        ((0, 128, 128), (255, 165, 0)),  # Turquesa a naranja
        ((70, 130, 180), (255, 255, 255)) # Azul acero a blanco
    ]
    
    for i, (color_inicio, color_fin) in enumerate(colores, 1):
        nombre = f"gradiente_{i:02d}"
        ruta = os.path.join(directorio, f"{nombre}.jpg")
        
        imagen = crear_imagen_gradiente(800, 600, color_inicio, color_fin, nombre)
        imagen.save(ruta, quality=95)
        imagenes_generadas.append(ruta)
        print(f"✅ Creada: {nombre}.jpg (800x600)")
    
    # Generar 3 imágenes geométricas
    for i in range(1, 4):
        nombre = f"geometrica_{i:02d}"
        ruta = os.path.join(directorio, f"{nombre}.jpg")
        
        ancho = random.choice([640, 800, 1024])
        alto = random.choice([480, 600, 768])
        
        imagen = crear_imagen_geometrica(ancho, alto, nombre)
        imagen.save(ruta, quality=95)
        imagenes_generadas.append(ruta)
        print(f"✅ Creada: {nombre}.jpg ({ancho}x{alto})")
    
    # Generar 2 imágenes con patrones
    for i in range(1, 3):
        nombre = f"patron_{i:02d}"
        ruta = os.path.join(directorio, f"{nombre}.jpg")
        
        imagen = crear_imagen_patron(800, 600, nombre)
        imagen.save(ruta, quality=95)
        imagenes_generadas.append(ruta)
        print(f"✅ Creada: {nombre}.jpg (800x600)")
    
    print("="*60)
    print(f"🎉 ¡Completado! Se generaron {len(imagenes_generadas)} imágenes de prueba")
    print(f"📁 Ubicación: {os.path.abspath(directorio)}")
    print("\n💡 Ahora puedes:")
    print("   1. Iniciar el servidor: python backend/servidor_websocket.py")
    print("   2. Abrir frontend/index.html en tu navegador")
    print("   3. ¡Procesar estas imágenes con diferentes filtros!")

if __name__ == "__main__":
    main()
