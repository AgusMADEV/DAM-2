from playwright.sync_api import sync_playwright
from pathlib import Path
import time

html_file = Path("index3.html").resolve()

# Crear carpeta "imagenes" si no existe
output_dir = Path("imagenes")
output_dir.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    for i in range(100):
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})

        page.goto(f"file://{html_file}", wait_until="load")

    
        # Epoch en milisegundos
        epoch_ms = int(time.time() * 1000)
        output_file = output_dir / f"output_{epoch_ms}.jpg"

        page.screenshot(path=str(output_file), type="jpeg", quality=90)

        # Pequeña pausa para asegurar epoch distinto
        time.sleep(0.01)

        browser.close()

