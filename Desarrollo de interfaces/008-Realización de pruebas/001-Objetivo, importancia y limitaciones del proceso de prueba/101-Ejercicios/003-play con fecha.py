from playwright.sync_api import sync_playwright
from pathlib import Path
import time

html_file = Path("index2.html").resolve()

# Epoch en milisegundos
epoch_ms = int(time.time() * 1000)
output_file = f"output_{epoch_ms}.jpg"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 800})

    page.goto(f"file://{html_file}", wait_until="load")
    page.screenshot(path=output_file, type="jpeg", quality=90)

    browser.close()

