from pydub import AudioSegment
import numpy as np
from PIL import Image, ImageDraw

def cargar_audio(ruta_archivo):
    """Carga un archivo MP3 y lo convierte en array de muestras"""
    audio = AudioSegment.from_mp3(ruta_archivo)
    samples = np.array(audio.get_array_of_samples())
    return samples, audio

def generar_waveform(samples, ancho=1200, alto=400, color_onda=(59, 130, 246)):
    """
    Genera una imagen de waveform con cápsulas redondeadas
    
    Parámetros:
    - samples: array de muestras de audio
    - ancho: ancho de la imagen en píxeles
    - alto: alto de la imagen en píxeles
    - color_onda: color RGB de la onda
    """
    # Crear imagen con fondo blanco
    imagen = Image.new('RGB', (ancho, alto), color=(255, 255, 255))
    draw = ImageDraw.Draw(imagen)
    
    # Calcular cuántas muestras agrupar en cada píxel
    muestras_por_pixel = len(samples) // ancho
    
    # Normalizar valores para que encajen en la altura
    valor_maximo = max(abs(samples.min()), abs(samples.max()))
    
    # Dibujar la waveform
    for x in range(ancho):
        # Obtener el rango de muestras para este píxel
        inicio = x * muestras_por_pixel
        fin = inicio + muestras_por_pixel
        
        if fin > len(samples):
            break
            
        # Obtener el valor máximo en este segmento
        segmento = samples[inicio:fin]
        valor_max = abs(segmento).max()
        
        # Normalizar el valor (0 a 1)
        valor_normalizado = valor_max / valor_maximo
        
        # Calcular la altura de la barra
        altura_barra = int((alto / 2) * valor_normalizado)
        
        # Coordenadas de la cápsula
        centro_y = alto // 2
        y1 = centro_y - altura_barra
        y2 = centro_y + altura_barra
        
        # Ancho de cada barra
        ancho_barra = 2
        
        # Dibujar cápsula redondeada (rectángulo con bordes redondeados)
        draw.rounded_rectangle(
            [(x, y1), (x + ancho_barra, y2)],
            radius=ancho_barra // 2,
            fill=color_onda
        )
    
    return imagen

def main():
    """Función principal que ejecuta todo el proceso"""
    print("🎵 Generador de Waveform")
    print("-" * 40)
    
    # Ruta del archivo MP3
    ruta_mp3 = "0802.mp3"
    
    print(f"📂 Cargando archivo: {ruta_mp3}")
    samples, audio = cargar_audio(ruta_mp3)
    print(f"✓ Audio cargado: {len(samples)} muestras")
    print(f"  - Duración: {len(audio) / 1000:.2f} segundos")
    print(f"  - Canales: {audio.channels}")
    print(f"  - Sample rate: {audio.frame_rate} Hz")
    
    print("\n🎨 Generando waveform...")
    imagen = generar_waveform(samples, ancho=1200, alto=400)
    
    # Guardar la imagen
    nombre_salida = "waveform.png"
    imagen.save(nombre_salida)
    print(f"✓ Waveform guardada como: {nombre_salida}")
    
    print("\n✅ Proceso completado con éxito!")

if __name__ == "__main__":
    main()
