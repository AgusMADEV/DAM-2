from PIL import Image, ImageOps
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

NUCLEOS = 1
ENTRADA = "agustin.png"
SALIDA  = "agustin3.png"

def procesa_bloque(img, y0, y1):
    """
    Recorta [y0:y1) y devuelve el recorte invertido.
    """
    box = (0, y0, img.width, y1)
    recorte = img.crop(box)
    # ImageOps.invert suele liberar el GIL (C-level), ideal para hilos
    return y0, ImageOps.invert(recorte.convert("RGB"))

def main():
    inicio = time.time()
    img = Image.open(ENTRADA).convert("RGB")

    alto = img.height
    ancho = img.width
    bloque_altura = alto // NUCLEOS
    # La última franja absorbe el resto (si no divide exacto)
    rangos = []
    for i in range(NUCLEOS):
        y0 = i * bloque_altura
        y1 = (i + 1) * bloque_altura if i < NUCLEOS - 1 else alto
        rangos.append((y0, y1))

    # Procesamos en paralelo por hilos
    resultados = []
    with ThreadPoolExecutor(max_workers=NUCLEOS) as ex:
        futs = [ex.submit(procesa_bloque, img, y0, y1) for (y0, y1) in rangos]
        for f in as_completed(futs):
            resultados.append(f.result())

    # Montamos la imagen final
    salida = Image.new("RGB", (ancho, alto))
    # Ordenamos por y0 para pegar en orden
    for y0, bloque in sorted(resultados, key=lambda t: t[0]):
        salida.paste(bloque, (0, y0))

    salida.save(SALIDA, quality=95)
    print(f"{time.time()-inicio:.3f} segundos")

if __name__ == "__main__":
    main()
