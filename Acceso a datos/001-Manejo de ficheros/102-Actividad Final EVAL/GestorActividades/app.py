"""Punto de entrada para el Gestor Personal de Actividades.

Ejecutar: python app.py
"""
from ui.controllers import AppController
import logging
from pathlib import Path


def main():
    # Asegurar que el directorio de logs exista antes de configurar logging
    Path('logs').mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename='logs/app.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')
    controller = AppController()
    controller.run()

if __name__ == '__main__':
    main()
