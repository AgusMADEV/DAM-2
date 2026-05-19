import os
import random
from PIL import Image, ImageChops, ImageDraw, ImageFont

# -------------------------------------------------------
# Configuration
# -------------------------------------------------------

GALERIA_FOLDER = "galeria"
OUTPUT_FOLDER = "generated_images"
LOGO_FILENAME = "logo.png"

IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080

NUM_OUTPUT_IMAGES = 20  # how many final images to generate

# Allowed background colors (RGB)
PERMITTED_COLORS = [
    (255, 0, 0),       # red
    (0, 255, 0),       # green
    (0, 0, 255),       # blue
    (255, 255, 0),     # yellow
    (255, 255, 255),   # white
    (0, 0, 0)          # black
]

# Logo parameters
LOGO_ALPHA_FACTOR = 0.2  # 20% transparency global
MIN_SCALE = 0.5
MAX_SCALE = 2.0
MIN_ROTATION = -30
MAX_ROTATION = 30

# Blend mode with gallery image: "screen" or "add"
BLEND_MODE = "screen"

# Text parameters
TEXT_STRING = "Sample text here"    # text to draw (centered)
FONT_FILENAME = "Ubuntu-B.ttf"      # font file in the same folder as this script
FONT_SIZE = 120                     # font size
TEXT_COLOR = (255, 255, 255)        # text color (RGB), e.g. white

# Image extensions
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp", ".tif", ".tiff")

# -------------------------------------------------------
# Prepare folders
# -------------------------------------------------------

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -------------------------------------------------------
# Load gallery images
# -------------------------------------------------------

if not os.path.isdir(GALERIA_FOLDER):
    raise FileNotFoundError(f"Gallery folder '{GALERIA_FOLDER}' does not exist.")

galeria_files = [
    os.path.join(GALERIA_FOLDER, f)
    for f in os.listdir(GALERIA_FOLDER)
    if f.lower().endswith(IMAGE_EXTENSIONS)
]

if not galeria_files:
    raise RuntimeError(f"No images found in folder '{GALERIA_FOLDER}'.")

# -------------------------------------------------------
# Load logo (if possible). If fails, work without logo.
# -------------------------------------------------------

logo_original = None
try:
    if os.path.isfile(LOGO_FILENAME):
        logo_original = Image.open(LOGO_FILENAME).convert("RGBA")
    else:
        print(f"Warning: logo file '{LOGO_FILENAME}' not found. Images will be generated without logo.")
except Exception as e:
    print(f"Warning: error loading logo '{LOGO_FILENAME}': {e}")
    logo_original = None

# -------------------------------------------------------
# Load font (if possible). If fails, work without text.
# -------------------------------------------------------

font = None
if TEXT_STRING:
    try:
        if os.path.isfile(FONT_FILENAME):
            font = ImageFont.truetype(FONT_FILENAME, FONT_SIZE)
        else:
            print(f"Warning: font file '{FONT_FILENAME}' not found. Text will not be drawn.")
    except Exception as e:
        print(f"Warning: error loading font '{FONT_FILENAME}': {e}")
        font = None

# -------------------------------------------------------
# Blend function (screen or add)
# -------------------------------------------------------

def blend_with_background(background_rgb, overlay_rgb):
    """Blend background and overlay using configured mode."""
    if BLEND_MODE.lower() == "add":
        return ImageChops.add(background_rgb, overlay_rgb, scale=1.0, offset=0)
    else:
        # you changed to multiply instead of true 'screen'
        return ImageChops.multiply(background_rgb, overlay_rgb)

# -------------------------------------------------------
# Generate output images
# -------------------------------------------------------

for idx in range(1, NUM_OUTPUT_IMAGES + 1):
    try:
        # 1. Random-color background
        bg_color = random.choice(PERMITTED_COLORS)
        background = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), bg_color)

        # 2. Pick a random gallery image, grayscale, 2x lightness, blend
        random_img_path = random.choice(galeria_files)
        try:
            img = Image.open(random_img_path).convert("L")  # grayscale
        except Exception as e_img:
            print(f"Warning: could not open gallery image '{random_img_path}': {e_img}")
            img = None  # continue with just background (and logo/text)

        if img is not None:
            # double lightness (clamp to 255)
            img = img.point(lambda p: 255 if p * 2 > 255 else int(p * 2))

            # resize to 1920x1080 for blending
            img_resized = img.resize((IMAGE_WIDTH, IMAGE_HEIGHT), resample=Image.LANCZOS)

            # convert to RGB for blending
            overlay_rgb = img_resized.convert("RGB")

            # blend with background
            background = blend_with_background(background, overlay_rgb)

        # from here on, work in RGBA (for logo and optional text)
        background = background.convert("RGBA")

        # 3. Logo on top (random position, rotation, scale, 20% transparency)
        if logo_original is not None:
            # work copy
            logo = logo_original.copy()

            # random scale
            scale = random.uniform(MIN_SCALE, MAX_SCALE)
            new_w = max(1, int(logo.width * scale))
            new_h = max(1, int(logo.height * scale))
            logo = logo.resize((new_w, new_h), resample=Image.LANCZOS)

            # random rotation
            angle = random.uniform(MIN_ROTATION, MAX_ROTATION)
            logo = logo.rotate(angle, expand=True, resample=Image.BICUBIC)

            # apply 20% alpha
            if logo.mode != "RGBA":
                logo = logo.convert("RGBA")
            r, g, b, a = logo.split()
            a = a.point(lambda p: int(p * LOGO_ALPHA_FACTOR))
            logo = Image.merge("RGBA", (r, g, b, a))

            # random position inside canvas
            lw, lh = logo.size
            max_x = max(0, IMAGE_WIDTH - lw)
            max_y = max(0, IMAGE_HEIGHT - lh)
            pos_x = random.randint(0, max_x) if max_x > 0 else 0
            pos_y = random.randint(0, max_y) if max_y > 0 else 0

            background.paste(logo, (pos_x, pos_y), logo)

        # 4. Centered text (if font loaded and TEXT_STRING not empty)
        if font is not None and TEXT_STRING:
            draw = ImageDraw.Draw(background)

            # get text bounding box to compute center
            # textbbox returns (left, top, right, bottom)
            bbox = draw.textbbox((0, 0), TEXT_STRING, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]

            text_x = (IMAGE_WIDTH - text_w) // 2
            text_y = (IMAGE_HEIGHT - text_h) // 2

            # if background is RGBA, add alpha to TEXT_COLOR
            if background.mode == "RGBA":
                fill_color = TEXT_COLOR + (255,)
                outline_color = (0, 0, 0, 255)
            else:
                fill_color = TEXT_COLOR
                outline_color = (0, 0, 0)

            # draw text with black outline
            offsets = [(-2, 0), (2, 0), (0, -2), (0, 2),
                       (-2, -2), (-2, 2), (2, -2), (2, 2)]

            # first draw outline
            for ox, oy in offsets:
                draw.text((text_x + ox, text_y + oy),
                          TEXT_STRING, font=font, fill=outline_color)

            # then draw main text
            draw.text((text_x, text_y), TEXT_STRING, font=font, fill=fill_color)

        # 5. Save result
        output_filename = f"output_{idx:03d}.png"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        background.save(output_path)

    except Exception as e:
        # any failure on this iteration: warn and continue
        print(f"Warning: error processing output {idx}: {e}")
        continue

print(f"Done. Images generated in '{OUTPUT_FOLDER}'.")

