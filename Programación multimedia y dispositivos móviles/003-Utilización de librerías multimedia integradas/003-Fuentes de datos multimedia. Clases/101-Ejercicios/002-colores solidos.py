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

# -------------------------------------------------------
# Create output folder
# -------------------------------------------------------

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -------------------------------------------------------
# Generate images
# -------------------------------------------------------

for i in range(NUM_IMAGES):
    color = random.choice(PERMITTED_COLORS)
    img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), color)

    filename = f"image_{i+1:03d}.png"
    img.save(os.path.join(OUTPUT_FOLDER, filename))

print(f"{NUM_IMAGES} solid-color images created in '{OUTPUT_FOLDER}'")

