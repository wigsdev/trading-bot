# test_connection.py
# 📘 Script para verificar que el entorno y las dependencias básicas están correctas.

import sys
import requests
import pandas as pd

def test_environment():
    print("✅ Python ejecutándose correctamente.")
    print(f"Versión de Python: {sys.version}")
    print(f"Versión de pandas: {pd.__version__}")

    try:
        response = requests.get("https://api.github.com")
        if response.status_code == 200:
            print("🌐 Conexión HTTP exitosa con GitHub API.")
        else:
            print(f"⚠️ Conexión HTTP falló: {response.status_code}")
    except Exception as e:
        print(f"❌ Error al conectar: {e}")

if __name__ == "__main__":
    test_environment()
