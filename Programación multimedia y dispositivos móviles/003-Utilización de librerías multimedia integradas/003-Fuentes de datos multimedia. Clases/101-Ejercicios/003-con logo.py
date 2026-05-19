import os
import random
from PIL import Image

# -------------------------------------------------------
# Configuration
# -------------------------------------------------------

OUTPUT_FOLDER = "generated_images"
IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080
NUM_IMAGES = 10   # number of images to generate

# List of allowed solid colors (R, G, B)
PERMITTED_COLORS = [
    (255, 0,   0),     # red
    (0,   255, 0),     # green
    (0,   0,   255),   # blue
    (255, 255, 0),     # yellow
    (255, 255, 255),   # white
    (0,   0,   0)      # black
]

LOGO_FILENAME = "logo.png"   # logo file in the same folder as this script
THRESHOLD_VALUE = 128        # threshold for black/white conversion
MIN_SCALE = 0.5              # relative to original logo
MAX_SCALE = 2.0
MIN_ROTATION = -30           # degrees
MAX_ROTATION = 30

# -------------------------------------------------------
# Prepare output folder
# -------------------------------------------------------

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -------------------------------------------------------
# Load and prepare logo (thresholded black on transparent)
# -------------------------------------------------------

if not os.path.isfile(LOGO_FILENAME):
    raise FileNotFoundError(f"Logo file '{LOGO_FILENAME}' not found in current folder.")

# Load as grayscale
logo_gray = Image.open(LOGO_FILENAME).convert("L")

# Apply threshold (produces pure black or white)
logo_bw = logo_gray.point(lambda p: 255 if p >= THRESHOLD_VALUE else 0)

# Create an RGBA logo: black where logo is dark, transparent where white
# Black pixels = logo; white = background -> transparent
logo_rgba = Image.new("RGBA", logo_bw.size, (0, 0, 0, 255))  # black with full alpha
alpha = logo_bw.point(lambda p: 255 - p)  # invert: black(0)->255, white(255)->0
logo_rgba.putalpha(alpha)

# -------------------------------------------------------
# Generate images
# -------------------------------------------------------

for i in range(NUM_IMAGES):
    # 1. Solid-color background
    bg_color = random.choice(PERMITTED_COLORS)
    img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), bg_color)

    # 2. Random scale
    scale = random.uniform(MIN_SCALE, MAX_SCALE)
    new_w = max(1, int(logo_rgba.width * scale))
    new_h = max(1, int(logo_rgba.height * scale))
    logo_scaled = logo_rgba.resize((new_w, new_h), resample=Image.LANCZOS)

    # 3. Random rotation
    angle = random.uniform(MIN_ROTATION, MAX_ROTATION)
    logo_transformed = logo_scaled.rotate(angle, expand=True, resample=Image.BICUBIC)

    # 4. Random position (ensure it stays within the image if possible)
    lw, lh = logo_transformed.size
    max_x = max(0, IMAGE_WIDTH - lw)
    max_y = max(0, IMAGE_HEIGHT - lh)

    # If logo is larger than the image, it will be anchored at (0,0)
    pos_x = random.randint(0, max_x) if max_x > 0 else 0
    pos_y = random.randint(0, max_y) if max_y > 0 else 0

    # 5. Paste logo using its alpha as mask
    img.paste(logo_transformed, (pos_x, pos_y), logo_transformed)

    # 6. Save
    filename = f"image_{i+1:03d}.png"
    img.save(os.path.join(OUTPUT_FOLDER, filename))

print(f"{NUM_IMAGES} images created in '{OUTPUT_FOLDER}' with logo overlay.")

