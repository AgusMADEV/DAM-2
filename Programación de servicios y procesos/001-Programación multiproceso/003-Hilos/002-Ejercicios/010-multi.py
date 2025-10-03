import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
from PIL import Image

# ------------------------
# Parámetros
# ------------------------
NUCLEOS = 6
ENTRADA = "agustin.png"
SALIDA  = "agustin_blur_threads.png"
SIGMA   = 5   # Sube a 3.0, 5.0, etc. para más carga (y ganar más con paralelismo)

# ------------------------
# Utilidades Gaussianas
# ------------------------
def gaussian_kernel1d(sigma: float, radius: int | None = None) -> np.ndarray:
    """
    Genera un kernel gaussiano 1D normalizado.
    radius por defecto = ceil(3*sigma).
    """
    if sigma <= 0:
        return np.array([1.0], dtype=np.float32)
    if radius is None:
        radius = int(np.ceil(3.0 * sigma))
    x = np.arange(-radius, radius + 1, dtype=np.float32)
    k = np.exp(-(x**2) / (2 * sigma * sigma))
    k /= k.sum()
    return k.astype(np.float32)

def convolve1d_reflect(img: np.ndarray, kernel: np.ndarray, axis: int) -> np.ndarray:
    """
    Convolución 1D separable a lo largo de 'axis' con padding reflect.
    img: (H, W, C) float32
    kernel: (K,) float32
    """
    radius = (kernel.size - 1) // 2
    if radius == 0:
        return img.copy()

    pad_width = [(0, 0), (0, 0), (0, 0)]
    pad_width[axis] = (radius, radius)
    padded = np.pad(img, pad_width=pad_width, mode="reflect")

    out = np.zeros_like(img, dtype=np.float32)
    for offset, w in enumerate(kernel):
        d = offset - radius
        if axis == 0:
            slice_src = padded[radius + d : radius + d + img.shape[0], :, :]
        elif axis == 1:
            slice_src = padded[:, radius + d : radius + d + img.shape[1], :]
        else:
            raise ValueError("axis debe ser 0 (vertical) o 1 (horizontal)")
        out += w * slice_src
    return out

def gaussian_blur_separable(img_f32: np.ndarray, sigma: float) -> np.ndarray:
    """
    Aplica blur gaussiano separable (horizontal + vertical) a img_f32 (H,W,C).
    """
    k = gaussian_kernel1d(sigma)
    tmp = convolve1d_reflect(img_f32, k, axis=1)  # horizontal (x)
    out = convolve1d_reflect(tmp, k, axis=0)      # vertical (y)
    return out

# ------------------------
# Paralelo con hilos (franjas con solape)
# ------------------------
def procesa_bloque(img_arr: np.ndarray, y0: int, y1: int, sigma: float) -> tuple[int, np.ndarray]:
    """
    Procesa el bloque [y0:y1) con solape vertical para evitar costuras.
    Devuelve (y0, bloque_blur_sin_solape).
    """
    radius = int(np.ceil(3.0 * sigma))
    H, _, _ = img_arr.shape

    y0_pad = max(0, y0 - radius)
    y1_pad = min(H, y1 + radius)

    bloque = img_arr[y0_pad:y1_pad, :, :]
    bloque_blur = gaussian_blur_separable(bloque, sigma)

    recorte_y0 = y0 - y0_pad
    recorte_y1 = recorte_y0 + (y1 - y0)
    bloque_final = bloque_blur[recorte_y0:recorte_y1, :, :]
    return y0, bloque_final

def blur_threads(img_arr: np.ndarray, sigma: float, n_workers: int) -> np.ndarray:
    H, W, C = img_arr.shape
    out = np.empty_like(img_arr, dtype=np.float32)

    base = H // n_workers
    rangos = []
    for i in range(n_workers):
        y0 = i * base
        y1 = (i + 1) * base if i < n_workers - 1 else H
        if y0 < y1:
            rangos.append((y0, y1))

    resultados = []
    with ThreadPoolExecutor(max_workers=n_workers) as ex:
        futs = [ex.submit(procesa_bloque, img_arr, y0, y1, sigma) for (y0, y1) in rangos]
        for f in as_completed(futs):
            resultados.append(f.result())

    for y0, bloque in sorted(resultados, key=lambda t: t[0]):
        out[y0:y0 + bloque.shape[0], :, :] = bloque

    return out

# ------------------------
# Main
# ------------------------
def main():
    inicio = time.time()
    img = Image.open(ENTRADA).convert("RGB")
    arr_u8 = np.array(img, dtype=np.uint8)
    arr_f32 = arr_u8.astype(np.float32)

    out_f32 = blur_threads(arr_f32, SIGMA, NUCLEOS)
    out_u8 = np.clip(np.rint(out_f32), 0, 255).astype(np.uint8)

    Image.fromarray(out_u8).save(SALIDA, quality=95)
    print(f"Threads: {time.time()-inicio:.3f} s  (workers={NUCLEOS}, sigma={SIGMA})")

if __name__ == "__main__":
    main()
