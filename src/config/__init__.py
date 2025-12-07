"""
src/config/__init__.py
---------------------
Módulo de configuración global.
Aquí se definirá la ruta de los archivos de configuración
y se manejarán las variables de entorno.
"""

import os

# Ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Carpeta de configuración
CONFIG_PATH = os.path.join(BASE_DIR, "src", "config")

# Exponer variables para importación externa
__all__ = ["BASE_DIR", "CONFIG_PATH"]
