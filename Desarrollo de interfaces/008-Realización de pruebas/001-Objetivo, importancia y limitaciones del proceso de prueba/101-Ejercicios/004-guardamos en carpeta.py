from playwright.sync_api import sync_playwright
from pathlib import Path
import time

html_file = Path("index2.html").resolve()

# Crear carpeta "imagenes" si no existe
output_dir = Path("imagenes")
output_dir.mkdir(parents=True, exist_ok=True)

# Epoch en milisegundos
epoch_ms = int(time.time() * 1000)
output_file = output_dir / f"output_{epoch_ms}.jpg"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 800})

    page.goto(f"file://{html_file}", wait_until="load")
    page.screenshot(path=str(output_file), type="jpeg", quality=90)

    browser.close()

