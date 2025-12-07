# 📦 Instalación

Esta guía te ayudará a instalar y configurar el Trading Bot Híbrido en tu sistema.

## 📋 Requisitos Previos

### Software Requerido
- **Python**: 3.10 o superior
- **Git**: Para clonar el repositorio
- **pip**: Gestor de paquetes de Python (incluido con Python)
- **Docker** (opcional): Para deployment containerizado

### Cuentas Necesarias
- **Alpaca**: Cuenta de trading (paper o live)
  - Registrarse en: https://alpaca.markets
  - Obtener API Key y Secret Key
- **Telegram** (opcional): Para recibir alertas
  - Crear un bot con @BotFather
  - Obtener el token del bot

## 🔧 Instalación Paso a Paso

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/trading-bot.git
cd trading-bot
```

### 2. Crear Entorno Virtual

**Windows (PowerShell/CMD):**
```bash
python -m venv venv
venv\Scripts\activate
```

**Windows (Git Bash):**
```bash
python -m venv venv
source venv/Scripts/activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Actualizar pip

```bash
python -m pip install --upgrade pip
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Verificar Instalación

```bash
python src/main.py
```

Deberías ver el mensaje:
```
🚀 Trading Bot iniciado correctamente.
```

## 🐳 Instalación con Docker

### 1. Construir la Imagen

```bash
docker build -t trading-bot -f docker/Dockerfile .
```

### 2. Ejecutar el Contenedor

```bash
docker run --rm trading-bot
```

### 3. Con Variables de Entorno

```bash
docker run --rm \
  -e ALPACA_API_KEY_ID=tu_api_key \
  -e ALPACA_API_SECRET_KEY=tu_secret \
  trading-bot
```

## 🔍 Verificación de Dependencias

Verifica que todas las librerías se instalaron correctamente:

```python
import pandas
import numpy
import matplotlib
import vectorbt
import alpaca_trade_api
import telegram

print("✅ Todas las dependencias instaladas correctamente")
```

## 🐛 Solución de Problemas

### Error: "No module named 'vectorbt'"

```bash
pip install vectorbt --upgrade
```

### Error: "Microsoft Visual C++ 14.0 is required"

En Windows, instala:
- [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

### Error de permisos en Linux/macOS

```bash
pip install --user -r requirements.txt
```

## ➡️ Siguiente Paso

Una vez instalado, continúa con la [**Configuración**](configuration.md) del bot.

## 📚 Recursos Adicionales

- [Documentación de Python](https://docs.python.org/3/)
- [Guía de venv](https://docs.python.org/3/library/venv.html)
- [Docker Documentation](https://docs.docker.com/)
