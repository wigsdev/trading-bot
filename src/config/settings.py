"""
Archivo de configuración base del proyecto.
Lee las variables de entorno (.env) y expone los valores de forma segura.
"""

import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

class Settings:
    """Clase que contiene la configuración general del proyecto."""

    ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
    ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
    ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")

    # Validación simple para asegurar que las claves existen
    if not ALPACA_API_KEY or not ALPACA_SECRET_KEY:
        raise ValueError("⚠️ Faltan claves de API en el archivo .env")

# Instancia global
settings = Settings()
