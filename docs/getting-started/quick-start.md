# 🚀 Inicio Rápido

Empieza a usar el Trading Bot Híbrido en menos de 10 minutos.

## ⚡ Configuración Rápida

### 1. Instalación Express

```bash
# Clonar y entrar al directorio
git clone https://github.com/tu-usuario/trading-bot.git
cd trading-bot

# Crear entorno virtual e instalar
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash
pip install -r requirements.txt
```

### 2. Configuración Mínima

```bash
# Copiar archivo de ejemplo
cp configs/.env.example configs/.env

# Editar con tus credenciales de Alpaca
nano configs/.env  # o usa tu editor favorito
```

Configuración mínima en `.env`:
```bash
ALPACA_API_KEY_ID=tu_api_key
ALPACA_API_SECRET_KEY=tu_secret_key
ALPACA_BASE_URL=https://paper-api.alpaca.markets
```

### 3. Primera Ejecución

```bash
python src/main.py
```

Deberías ver:
```
🚀 Trading Bot iniciado correctamente.
```

## 📊 Primer Backtest

Crea un archivo `scripts/my_first_backtest.py`:

```python
import vectorbt as vbt
import pandas as pd

# Descargar datos de ejemplo
data = vbt.YFData.download('AAPL', start='2023-01-01', end='2024-01-01')

# Estrategia simple: Media Móvil
fast_ma = vbt.MA.run(data.get('Close'), 10)
slow_ma = vbt.MA.run(data.get('Close'), 50)

# Señales de entrada/salida
entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

# Ejecutar backtest
portfolio = vbt.Portfolio.from_signals(
    data.get('Close'),
    entries,
    exits,
    init_cash=10000,
    fees=0.001
)

# Mostrar resultados
print(portfolio.stats())
print(f"\nRetorno Total: {portfolio.total_return():.2%}")
print(f"Sharpe Ratio: {portfolio.sharpe_ratio():.2f}")
```

Ejecutar:
```bash
python scripts/my_first_backtest.py
```

## 📈 Consultar Datos de Mercado

Crea `scripts/check_market.py`:

```python
import alpaca_trade_api as tradeapi
import os
from dotenv import load_dotenv

# Cargar credenciales
load_dotenv('configs/.env')

# Conectar a Alpaca
api = tradeapi.REST(
    os.getenv('ALPACA_API_KEY_ID'),
    os.getenv('ALPACA_API_SECRET_KEY'),
    os.getenv('ALPACA_BASE_URL')
)

# Obtener información de cuenta
account = api.get_account()
print(f"💰 Poder de compra: ${float(account.buying_power):,.2f}")
print(f"📊 Equity: ${float(account.equity):,.2f}")

# Obtener precio actual de una acción
symbol = 'AAPL'
barset = api.get_latest_bar(symbol)
print(f"\n📈 {symbol}: ${barset.c:.2f}")
```

Ejecutar:
```bash
python scripts/check_market.py
```

## 🔔 Configurar Alertas de Telegram

### 1. Crear Bot de Telegram

1. Abre Telegram y busca **@BotFather**
2. Envía `/newbot`
3. Sigue las instrucciones
4. Copia el token

### 2. Obtener Chat ID

1. Busca **@userinfobot**
2. Envía `/start`
3. Copia tu ID

### 3. Configurar en .env

```bash
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=987654321
```

### 4. Probar Alerta

Crea `scripts/test_telegram.py`:

```python
import os
from dotenv import load_dotenv
from telegram import Bot
import asyncio

load_dotenv('configs/.env')

async def send_alert():
    bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    await bot.send_message(
        chat_id=chat_id,
        text="🤖 Trading Bot conectado correctamente!"
    )
    print("✅ Mensaje enviado")

asyncio.run(send_alert())
```

Ejecutar:
```bash
python scripts/test_telegram.py
```

## 🎯 Próximos Pasos

Ahora que tienes el bot funcionando:

1. **Aprende más sobre arquitectura**
   - Lee [Visión General de Arquitectura](../architecture/overview.md)

2. **Explora estrategias de trading**
   - Revisa [Ejemplos de Estrategias](../examples/strategies/)

3. **Configura backtesting avanzado**
   - Consulta [Guía de Backtesting](../user-guide/backtesting.md)

4. **Implementa tu primera estrategia**
   - Sigue [Trading con Alpaca](../user-guide/alpaca-trading.md)

## 🆘 Problemas Comunes

### "ModuleNotFoundError: No module named 'vectorbt'"

```bash
pip install vectorbt --upgrade
```

### "Invalid API credentials"

Verifica que tus credenciales en `.env` sean correctas:
```bash
python scripts/verify_config.py
```

### El bot no se conecta a Alpaca

Asegúrate de usar la URL correcta:
- **Paper Trading**: `https://paper-api.alpaca.markets`
- **Live Trading**: `https://api.alpaca.markets`

## 📚 Recursos

- [Documentación Completa](../README.md)
- [Guía de Usuario](../user-guide/)
- [Ejemplos](../examples/)
