from PIL import Image, ImageOps
from concurrent.futures import ThreadPoolExecutor, as_completed
import time, os

NUCLEOS = os.cpu_count()
ENTRADA = "agustin.png"
SALIDA  = "agustin2.png"

def procesa_bloque(img, y0, y1):
    box = (0, y0, img.width, y1)
    recorte = img.crop(box)
    return y0, ImageOps.invert(recorte.convert("RGB"))

def main():
    inicio = time.time()
    with Image.open(ENTRADA) as im:
        img = im.convert("RGB")
        img.load()

    alto, ancho = img.height, img.width
    numero_hilos = max(1, min(NUCLEOS, alto))
    bloque_altura = alto // numero_hilos

    rangos = []
    for i in range(numero_hilos):
        y0 = i * bloque_altura
        y1 = (i + 1) * bloque_altura if i < numero_hilos - 1 else alto
        if y1 > y0:
            rangos.append((y0, y1))

    resultados = []
    with ThreadPoolExecutor(max_workers=numero_hilos) as ex:
        futs = [ex.submit(procesa_bloque, img, y0, y1) for (y0, y1) in rangos]
        for f in as_completed(futs):
            resultados.append(f.result())

    salida = Image.new("RGB", (ancho, alto))
    for y0, bloque in sorted(resultados, key=lambda t: t[0]):
        salida.paste(bloque, (0, y0))

    salida.save(SALIDA, quality=95)
    tiempo_final = time.time() - inicio
    print(f"{tiempo_final:.3f} segundos")

if __name__ == "__main__":
    main()
