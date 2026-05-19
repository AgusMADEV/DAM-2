import os
import random
from PIL import Image

# -------------------------------------------------------
# Configuration
# -------------------------------------------------------

OUTPUT_FOLDER = "generated_images"
IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080
NUM_IMAGES = 10   # how many images to generate

# List of allowed colors (R, G, B)
PERMITTED_COLORS = [
    (255, 0,   0),     # red
    (0,   255, 0),     # green
    (0,   0,   255),   # blue
    (255, 255, 0),     # yellow
    (255, 255, 255),   # white
    (0,   0,   0)      # black
]

# -------------------------------------------------------
# Create folder if needed
# -------------------------------------------------------

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -------------------------------------------------------
# Image generation
# -------------------------------------------------------

for i in range(NUM_IMAGES):
    img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))
    pixels = img.load()

    for y in range(IMAGE_HEIGHT):
        for x in range(IMAGE_WIDTH):
            pixels[x, y] = random.choice(PERMITTED_COLORS)

    filename = f"image_{i+1:03d}.png"
    img.save(os.path.join(OUTPUT_FOLDER, filename))

print(f"{NUM_IMAGES} images created in '{OUTPUT_FOLDER}'")

