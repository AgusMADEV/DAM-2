import os
import random
from PIL import Image, ImageChops

# -------------------------------------------------------
# Configuración
# -------------------------------------------------------

GALERIA_FOLDER = "galeria"
OUTPUT_FOLDER = "generated_images"
LOGO_FILENAME = "logo.png"

IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080

NUM_OUTPUT_IMAGES = 20  # cuántas imágenes finales quieres generar

# Colores permitidos (RGB)
PERMITTED_COLORS = [
    (255, 0, 0),       # rojo
    (0, 255, 0),       # verde
    (0, 0, 255),       # azul
    (255, 255, 0),     # amarillo
    (255, 255, 255),   # blanco
    (0, 0, 0)          # negro
]

# Parámetros del logo
LOGO_ALPHA_FACTOR = 0.2  # 20 % transparencia global
MIN_SCALE = 0.5
MAX_SCALE = 2.0
MIN_ROTATION = -30
MAX_ROTATION = 30

# Modo de mezcla con la imagen de galería: "screen" o "add"
BLEND_MODE = "screen"

# Extensiones consideradas como imagen
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp", ".tif", ".tiff")

# -------------------------------------------------------
# Preparar carpetas
# -------------------------------------------------------

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -------------------------------------------------------
# Cargar lista de imágenes de galeria
# -------------------------------------------------------

if not os.path.isdir(GALERIA_FOLDER):
    raise FileNotFoundError(f"La carpeta '{GALERIA_FOLDER}' no existe.")

galeria_files = [
    os.path.join(GALERIA_FOLDER, f)
    for f in os.listdir(GALERIA_FOLDER)
    if f.lower().endswith(IMAGE_EXTENSIONS)
]

if not galeria_files:
    raise RuntimeError(f"No se han encontrado imágenes en la carpeta '{GALERIA_FOLDER}'.")

# -------------------------------------------------------
# Cargar logo (si se puede). Si falla, se trabajará sin logo.
# -------------------------------------------------------

logo_original = None
try:
    if os.path.isfile(LOGO_FILENAME):
        logo_original = Image.open(LOGO_FILENAME).convert("RGBA")
    else:
        print(f"Aviso: no se ha encontrado '{LOGO_FILENAME}'. Se generarán imágenes sin logo.")
except Exception as e:
    print(f"Aviso: error al cargar el logo '{LOGO_FILENAME}': {e}")
    logo_original = None

# -------------------------------------------------------
# Función de mezcla (screen o add)
# -------------------------------------------------------

def blend_with_background(background_rgb, overlay_rgb):
    """Mezcla background y overlay usando el modo configurado."""
    if BLEND_MODE.lower() == "add":
        return ImageChops.add(background_rgb, overlay_rgb, scale=1.0, offset=0)
    else:
        # por defecto, screen
        return ImageChops.screen(background_rgb, overlay_rgb)

# -------------------------------------------------------
# Generar imágenes de salida
# -------------------------------------------------------

for idx in range(1, NUM_OUTPUT_IMAGES + 1):
    try:
        # 1. Fondo de color aleatorio
        bg_color = random.choice(PERMITTED_COLORS)
        background = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), bg_color)

        # 2. Elegir una imagen aleatoria de galeria y procesarla
        random_img_path = random.choice(galeria_files)
        try:
            img = Image.open(random_img_path).convert("L")  # escala de grises
        except Exception as e_img:
            print(f"Aviso: no se pudo abrir la imagen '{random_img_path}': {e_img}")
            # si falla la imagen de galería, generamos solo fondo (y logo si hay) y seguimos
            img = None

        if img is not None:
            # duplicar luminosidad (clamp a 255)
            img = img.point(lambda p: 255 if p * 2 > 255 else int(p * 2))

            # redimensionar a 1920x1080 para mezclar
            img_resized = img.resize((IMAGE_WIDTH, IMAGE_HEIGHT), resample=Image.LANCZOS)

            # convertir a RGB para mezclar
            overlay_rgb = img_resized.convert("RGB")

            # mezcla con el fondo
            background = blend_with_background(background, overlay_rgb)

        # 3. Colocar el logo encima con posición, rotación y escala aleatorias (20 % transparencia)
        if logo_original is not None:
            # copia de trabajo del logo
            logo = logo_original.copy()

            # escala aleatoria
            scale = random.uniform(MIN_SCALE, MAX_SCALE)
            new_w = max(1, int(logo.width * scale))
            new_h = max(1, int(logo.height * scale))
            logo = logo.resize((new_w, new_h), resample=Image.LANCZOS)

            # rotación aleatoria
            angle = random.uniform(MIN_ROTATION, MAX_ROTATION)
            logo = logo.rotate(angle, expand=True, resample=Image.BICUBIC)

            # aplicar 20 % de transparencia (sobre la alpha existente)
            if logo.mode != "RGBA":
                logo = logo.convert("RGBA")
            r, g, b, a = logo.split()
            a = a.point(lambda p: int(p * LOGO_ALPHA_FACTOR))
            logo = Image.merge("RGBA", (r, g, b, a))

            # posición aleatoria dentro de la imagen
            lw, lh = logo.size
            max_x = max(0, IMAGE_WIDTH - lw)
            max_y = max(0, IMAGE_HEIGHT - lh)
            pos_x = random.randint(0, max_x) if max_x > 0 else 0
            pos_y = random.randint(0, max_y) if max_y > 0 else 0

            # pegar sobre el fondo
            background = background.convert("RGBA")
            background.paste(logo, (pos_x, pos_y), logo)
        else:
            background = background.convert("RGB")

        # 4. Guardar resultado
        output_filename = f"output_{idx:03d}.png"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        background.save(output_path)

    except Exception as e:
        # Cualquier fallo en esta iteración se ignora, se continúa con la siguiente
        print(f"Aviso: error procesando salida {idx}: {e}")
        continue

print(f"Proceso terminado. Imágenes generadas en '{OUTPUT_FOLDER}'.")

