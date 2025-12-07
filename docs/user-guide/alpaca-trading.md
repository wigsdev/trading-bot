# 📊 Trading con Alpaca

Guía completa para operar acciones US utilizando la API de Alpaca.

## 🎯 Introducción

Alpaca es un broker que permite trading automatizado de acciones US a través de su API. Este bot utiliza Alpaca para:
- Ejecutar órdenes automáticamente
- Obtener datos de mercado en tiempo real
- Gestionar posiciones y portfolio

## 🔑 Configuración Inicial

### 1. Crear Cuenta en Alpaca

1. Visita [alpaca.markets](https://alpaca.markets)
2. Regístrate para una cuenta
3. Completa el proceso de verificación

### 2. Obtener API Keys

```bash
# En Alpaca Dashboard:
# 1. Ve a "Paper Trading" (para pruebas)
# 2. Navega a "API Keys"
# 3. Genera nuevas claves
# 4. Copia Key ID y Secret Key
```

### 3. Configurar en el Bot

Edita `configs/.env`:

```bash
ALPACA_API_KEY_ID=PK1234567890ABCDEF
ALPACA_API_SECRET_KEY=tu_secret_key_aqui
ALPACA_BASE_URL=https://paper-api.alpaca.markets  # Paper trading
# ALPACA_BASE_URL=https://api.alpaca.markets  # Live trading (¡CUIDADO!)
```

## 📈 Operaciones Básicas

### Consultar Información de Cuenta

```python
import alpaca_trade_api as tradeapi
import os
from dotenv import load_dotenv

load_dotenv('configs/.env')

# Conectar a Alpaca
api = tradeapi.REST(
    os.getenv('ALPACA_API_KEY_ID'),
    os.getenv('ALPACA_API_SECRET_KEY'),
    os.getenv('ALPACA_BASE_URL')
)

# Obtener información de cuenta
account = api.get_account()

print(f"💰 Equity: ${float(account.equity):,.2f}")
print(f"💵 Cash: ${float(account.cash):,.2f}")
print(f"📊 Buying Power: ${float(account.buying_power):,.2f}")
print(f"📈 Portfolio Value: ${float(account.portfolio_value):,.2f}")
```

### Obtener Datos de Mercado

```python
from datetime import datetime, timedelta

# Precio actual
symbol = 'AAPL'
latest_bar = api.get_latest_bar(symbol)
print(f"{symbol}: ${latest_bar.c:.2f}")

# Datos históricos
end = datetime.now()
start = end - timedelta(days=30)

bars = api.get_bars(
    symbol,
    '1Day',
    start=start.isoformat(),
    end=end.isoformat()
).df

print(bars.tail())
```

### Colocar Órdenes

```python
# Orden de mercado (compra)
order = api.submit_order(
    symbol='AAPL',
    qty=10,
    side='buy',
    type='market',
    time_in_force='day'
)

print(f"✅ Orden colocada: {order.id}")

# Orden limitada (venta)
order = api.submit_order(
    symbol='AAPL',
    qty=10,
    side='sell',
    type='limit',
    limit_price=150.00,
    time_in_force='gtc'  # Good till cancelled
)

# Orden con stop loss
order = api.submit_order(
    symbol='AAPL',
    qty=10,
    side='buy',
    type='market',
    time_in_force='day',
    stop_loss={'stop_price': 145.00}
)
```

### Consultar Posiciones

```python
# Todas las posiciones
positions = api.list_positions()

for position in positions:
    print(f"{position.symbol}: {position.qty} shares @ ${float(position.avg_entry_price):.2f}")
    print(f"  P&L: ${float(position.unrealized_pl):,.2f} ({float(position.unrealized_plpc)*100:.2f}%)")

# Posición específica
try:
    position = api.get_position('AAPL')
    print(f"AAPL Position: {position.qty} shares")
except:
    print("No position in AAPL")
```

### Consultar Órdenes

```python
# Órdenes abiertas
orders = api.list_orders(status='open')
print(f"Órdenes abiertas: {len(orders)}")

# Historial de órdenes
orders = api.list_orders(
    status='all',
    limit=10
)

for order in orders:
    print(f"{order.symbol}: {order.side} {order.qty} @ {order.type}")
    print(f"  Status: {order.status}")

# Cancelar orden
api.cancel_order(order.id)
```

## 🤖 Integración con el Bot

### Ejemplo de Estrategia Automatizada

```python
# src/strategies/alpaca_strategy.py
import alpaca_trade_api as tradeapi
import pandas as pd
from datetime import datetime, timedelta

class AlpacaTradingBot:
    def __init__(self, config):
        self.api = tradeapi.REST(
            config['api_key'],
            config['secret_key'],
            config['base_url']
        )
        self.symbols = config['symbols']
        self.max_position_size = config['max_position_size']
    
    def get_market_data(self, symbol, days=30):
        """Obtiene datos históricos."""
        end = datetime.now()
        start = end - timedelta(days=days)
        
        bars = self.api.get_bars(
            symbol,
            '1Day',
            start=start.isoformat(),
            end=end.isoformat()
        ).df
        
        return bars
    
    def calculate_signals(self, data):
        """Calcula señales de trading (ejemplo: MA crossover)."""
        data['SMA_20'] = data['close'].rolling(window=20).mean()
        data['SMA_50'] = data['close'].rolling(window=50).mean()
        
        # Señal de compra: SMA 20 cruza por encima de SMA 50
        data['buy_signal'] = (data['SMA_20'] > data['SMA_50']) & \
                             (data['SMA_20'].shift(1) <= data['SMA_50'].shift(1))
        
        # Señal de venta: SMA 20 cruza por debajo de SMA 50
        data['sell_signal'] = (data['SMA_20'] < data['SMA_50']) & \
                              (data['SMA_20'].shift(1) >= data['SMA_50'].shift(1))
        
        return data
    
    def execute_trades(self, symbol, signals):
        """Ejecuta operaciones basadas en señales."""
        latest_signal = signals.iloc[-1]
        
        # Verificar si tenemos posición
        try:
            position = self.api.get_position(symbol)
            has_position = True
            qty = int(position.qty)
        except:
            has_position = False
            qty = 0
        
        # Ejecutar según señal
        if latest_signal['buy_signal'] and not has_position:
            # Comprar
            order = self.api.submit_order(
                symbol=symbol,
                qty=self.max_position_size,
                side='buy',
                type='market',
                time_in_force='day'
            )
            print(f"🟢 BUY {symbol}: {self.max_position_size} shares")
            return order
        
        elif latest_signal['sell_signal'] and has_position:
            # Vender
            order = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side='sell',
                type='market',
                time_in_force='day'
            )
            print(f"🔴 SELL {symbol}: {qty} shares")
            return order
        
        return None
    
    def run(self):
        """Ciclo principal del bot."""
        print("🤖 Bot iniciado...")
        
        for symbol in self.symbols:
            print(f"\n📊 Analizando {symbol}...")
            
            # Obtener datos
            data = self.get_market_data(symbol)
            
            # Calcular señales
            signals = self.calculate_signals(data)
            
            # Ejecutar trades
            order = self.execute_trades(symbol, signals)
            
            if order:
                print(f"✅ Orden ejecutada: {order.id}")
            else:
                print(f"⏸️  Sin señales para {symbol}")

# Uso
if __name__ == "__main__":
    config = {
        'api_key': os.getenv('ALPACA_API_KEY_ID'),
        'secret_key': os.getenv('ALPACA_API_SECRET_KEY'),
        'base_url': os.getenv('ALPACA_BASE_URL'),
        'symbols': ['AAPL', 'MSFT', 'GOOGL'],
        'max_position_size': 10
    }
    
    bot = AlpacaTradingBot(config)
    bot.run()
```

## ⚠️ Consideraciones Importantes

### Paper Trading vs Live Trading

```python
# ✅ Paper Trading (Recomendado para pruebas)
ALPACA_BASE_URL=https://paper-api.alpaca.markets

# ⚠️ Live Trading (Dinero real)
ALPACA_BASE_URL=https://api.alpaca.markets
```

### Límites de la API

- **200 requests por minuto** por API key
- Implementar rate limiting:

```python
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=200, period=60)
def api_call():
    return api.get_account()
```

### Horarios de Mercado

```python
# Verificar si el mercado está abierto
clock = api.get_clock()

if clock.is_open:
    print("✅ Mercado abierto")
else:
    print("❌ Mercado cerrado")
    print(f"Próxima apertura: {clock.next_open}")
```

### Gestión de Riesgos

```python
class RiskManager:
    def __init__(self, max_position_pct=0.1, max_loss_pct=0.02):
        self.max_position_pct = max_position_pct
        self.max_loss_pct = max_loss_pct
    
    def calculate_position_size(self, account_value, price):
        """Calcula tamaño de posición basado en % del portfolio."""
        max_position_value = account_value * self.max_position_pct
        qty = int(max_position_value / price)
        return qty
    
    def calculate_stop_loss(self, entry_price):
        """Calcula precio de stop loss."""
        stop_price = entry_price * (1 - self.max_loss_pct)
        return round(stop_price, 2)

# Uso
risk_mgr = RiskManager(max_position_pct=0.1, max_loss_pct=0.02)

account = api.get_account()
account_value = float(account.equity)
current_price = 150.00

qty = risk_mgr.calculate_position_size(account_value, current_price)
stop_loss = risk_mgr.calculate_stop_loss(current_price)

print(f"Tamaño de posición: {qty} shares")
print(f"Stop loss: ${stop_loss}")
```

## 📚 Recursos

- [Alpaca API Documentation](https://alpaca.markets/docs/)
- [alpaca-trade-api Python](https://github.com/alpacahq/alpaca-trade-api-python)
- [Alpaca Community](https://forum.alpaca.markets/)

## 🆘 Troubleshooting

### Error: "Invalid API credentials"
- Verifica que las claves sean correctas
- Asegúrate de usar la URL correcta (paper vs live)

### Error: "Insufficient buying power"
- Verifica el saldo de tu cuenta
- Reduce el tamaño de la posición

### Error: "Market is closed"
- El mercado US opera de 9:30 AM a 4:00 PM ET
- Verifica horarios con `api.get_clock()`

---

**Próximo paso**: [Backtesting](backtesting.md) para probar tus estrategias
