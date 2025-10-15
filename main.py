"""
main.py
---------------------
Entry point del bot de trading.
Este archivo será responsable de inicializar la configuración,
cargar los parámetros y ejecutar los módulos principales del sistema.
"""

from src.config import settings


def main():
    """Función principal del bot de trading."""
    print("🚀 Trading bot iniciado correctamente.")
    print(f"Configuración cargada desde: {settings.CONFIG_PATH}")


if __name__ == "__main__":
    main()
