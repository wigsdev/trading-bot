# 📊 Estrategia: Media Móvil (Moving Average)

Ejemplo de estrategia de trading basada en el cruce de medias móviles.

## 🎯 Descripción

La estrategia de cruce de medias móviles es una de las más populares en trading algorítmico. Utiliza dos medias móviles de diferentes períodos para generar señales de compra y venta.

### Lógica

- **Señal de COMPRA**: Cuando la media móvil rápida cruza por encima de la media móvil lenta
- **Señal de VENTA**: Cuando la media móvil rápida cruza por debajo de la media móvil lenta

## 📈 Implementación

```python
# src/strategies/ma_crossover_strategy.py
import pandas as pd
import numpy as np
from typing import Dict, Any
from .base import TradingStrategy

class MACrossoverStrategy(TradingStrategy):
    """
    Estrategia de cruce de medias móviles.
    
    Parámetros:
        fast_period (int): Período de la media móvil rápida (default: 20)
        slow_period (int): Período de la media móvil lenta (default: 50)
        ma_type (str): Tipo de media móvil - 'sma' o 'ema' (default: 'sma')
    """
    
    def __init__(
        self,
        fast_period: int = 20,
        slow_period: int = 50,
        ma_type: str = 'sma'
    ):
        super().__init__({'name': 'MA Crossover Strategy'})
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.ma_type = ma_type.lower()
        
        if self.fast_period >= self.slow_period:
            raise ValueError("fast_period debe ser menor que slow_period")
    
    def calculate_ma(self, prices: pd.Series, period: int) -> pd.Series:
        """
        Calcula media móvil.
        
        Args:
            prices: Serie de precios
            period: Período de la media móvil
        
        Returns:
            Serie con valores de la media móvil
        """
        if self.ma_type == 'sma':
            return prices.rolling(window=period).mean()
        elif self.ma_type == 'ema':
            return prices.ewm(span=period, adjust=False).mean()
        else:
            raise ValueError(f"ma_type no válido: {self.ma_type}")
    
    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula las medias móviles.
        
        Args:
            data: DataFrame con columna 'Close'
        
        Returns:
            DataFrame con columnas adicionales de indicadores
        """
        data = data.copy()
        
        # Calcular medias móviles
        data['MA_Fast'] = self.calculate_ma(data['Close'], self.fast_period)
        data['MA_Slow'] = self.calculate_ma(data['Close'], self.slow_period)
        
        return data
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Genera señales de trading basadas en cruces de medias móviles.
        
        Args:
            data: DataFrame con columna 'Close'
        
        Returns:
            DataFrame con columnas 'buy' y 'sell'
        """
        # Calcular indicadores
        data = self.calculate_indicators(data)
        
        # Crear DataFrame de señales
        signals = pd.DataFrame(index=data.index)
        
        # Detectar cruces
        # Compra: MA rápida cruza por encima de MA lenta
        signals['buy'] = (
            (data['MA_Fast'] > data['MA_Slow']) &
            (data['MA_Fast'].shift(1) <= data['MA_Slow'].shift(1))
        )
        
        # Venta: MA rápida cruza por debajo de MA lenta
        signals['sell'] = (
            (data['MA_Fast'] < data['MA_Slow']) &
            (data['MA_Fast'].shift(1) >= data['MA_Slow'].shift(1))
        )
        
        return signals
    
    def get_parameters(self) -> Dict[str, Any]:
        """Retorna los parámetros de la estrategia."""
        return {
            'fast_period': self.fast_period,
            'slow_period': self.slow_period,
            'ma_type': self.ma_type
        }
```

## 🧪 Backtesting

```python
# examples/backtest_ma_strategy.py
import vectorbt as vbt
import pandas as pd
from src.strategies.ma_crossover_strategy import MACrossoverStrategy

# Descargar datos
data = vbt.YFData.download(
    'AAPL',
    start='2023-01-01',
    end='2024-01-01'
).get('Close')

# Crear estrategia
strategy = MACrossoverStrategy(fast_period=20, slow_period=50, ma_type='sma')

# Generar señales
df = pd.DataFrame({'Close': data})
signals = strategy.generate_signals(df)

# Ejecutar backtest
portfolio = vbt.Portfolio.from_signals(
    data,
    entries=signals['buy'],
    exits=signals['sell'],
    init_cash=10000,
    fees=0.001,  # 0.1% comisión
    slippage=0.0005  # 0.05% slippage
)

# Mostrar resultados
print("=" * 50)
print("RESULTADOS DEL BACKTEST")
print("=" * 50)
print(portfolio.stats())

print("\n" + "=" * 50)
print("MÉTRICAS CLAVE")
print("=" * 50)
print(f"Retorno Total: {portfolio.total_return():.2%}")
print(f"Sharpe Ratio: {portfolio.sharpe_ratio():.2f}")
print(f"Max Drawdown: {portfolio.max_drawdown():.2%}")
print(f"Win Rate: {portfolio.trades.win_rate:.2%}")
print(f"Total Trades: {portfolio.trades.count()}")

# Visualizar
portfolio.plot().show()
```

## 📊 Optimización de Parámetros

```python
# examples/optimize_ma_strategy.py
import vectorbt as vbt
import pandas as pd
import numpy as np

# Descargar datos
data = vbt.YFData.download(
    'AAPL',
    start='2023-01-01',
    end='2024-01-01'
).get('Close')

# Rangos de parámetros a probar
fast_periods = np.arange(10, 50, 5)
slow_periods = np.arange(30, 100, 10)

# Calcular todas las combinaciones de MAs
fast_ma = vbt.MA.run(data, window=fast_periods)
slow_ma = vbt.MA.run(data, window=slow_periods)

# Generar señales para todas las combinaciones
entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

# Ejecutar backtests
portfolio = vbt.Portfolio.from_signals(
    data,
    entries,
    exits,
    init_cash=10000,
    fees=0.001
)

# Encontrar mejor combinación
sharpe_ratios = portfolio.sharpe_ratio()
best_idx = sharpe_ratios.idxmax()

print("=" * 50)
print("OPTIMIZACIÓN DE PARÁMETROS")
print("=" * 50)
print(f"Mejor Fast Period: {best_idx[0]}")
print(f"Mejor Slow Period: {best_idx[1]}")
print(f"Sharpe Ratio: {sharpe_ratios.max():.2f}")

# Visualizar heatmap
sharpe_ratios.vbt.heatmap(
    xaxis_title='Slow Period',
    yaxis_title='Fast Period',
    title='Sharpe Ratio Heatmap'
).show()
```

## 📈 Ejemplo de Uso en Vivo

```python
# examples/live_ma_trading.py
import alpaca_trade_api as tradeapi
import pandas as pd
import os
from dotenv import load_dotenv
from src.strategies.ma_crossover_strategy import MACrossoverStrategy

load_dotenv('configs/.env')

class LiveMATradingBot:
    """Bot de trading en vivo con estrategia MA."""
    
    def __init__(self):
        self.api = tradeapi.REST(
            os.getenv('ALPACA_API_KEY_ID'),
            os.getenv('ALPACA_API_SECRET_KEY'),
            os.getenv('ALPACA_BASE_URL')
        )
        self.strategy = MACrossoverStrategy(fast_period=20, slow_period=50)
        self.symbol = 'AAPL'
        self.position_size = 10
    
    def get_historical_data(self, days=100):
        """Obtiene datos históricos."""
        from datetime import datetime, timedelta
        
        end = datetime.now()
        start = end - timedelta(days=days)
        
        bars = self.api.get_bars(
            self.symbol,
            '1Day',
            start=start.isoformat(),
            end=end.isoformat()
        ).df
        
        return bars
    
    def check_position(self):
        """Verifica si tenemos posición abierta."""
        try:
            position = self.api.get_position(self.symbol)
            return int(position.qty)
        except:
            return 0
    
    def execute_trade(self, signal_type):
        """Ejecuta operación basada en señal."""
        current_position = self.check_position()
        
        if signal_type == 'buy' and current_position == 0:
            # Comprar
            order = self.api.submit_order(
                symbol=self.symbol,
                qty=self.position_size,
                side='buy',
                type='market',
                time_in_force='day'
            )
            print(f"🟢 BUY {self.symbol}: {self.position_size} shares")
            return order
        
        elif signal_type == 'sell' and current_position > 0:
            # Vender
            order = self.api.submit_order(
                symbol=self.symbol,
                qty=current_position,
                side='sell',
                type='market',
                time_in_force='day'
            )
            print(f"🔴 SELL {self.symbol}: {current_position} shares")
            return order
        
        return None
    
    def run(self):
        """Ejecuta el bot."""
        print(f"🤖 Iniciando bot con estrategia MA Crossover...")
        print(f"📊 Symbol: {self.symbol}")
        print(f"⚡ Fast MA: {self.strategy.fast_period}")
        print(f"🐌 Slow MA: {self.strategy.slow_period}")
        
        # Obtener datos
        data = self.get_historical_data()
        
        # Generar señales
        signals = self.strategy.generate_signals(data)
        
        # Obtener última señal
        latest_signal = signals.iloc[-1]
        
        # Ejecutar trade si hay señal
        if latest_signal['buy']:
            self.execute_trade('buy')
        elif latest_signal['sell']:
            self.execute_trade('sell')
        else:
            print("⏸️  Sin señales de trading")

if __name__ == "__main__":
    bot = LiveMATradingBot()
    bot.run()
```

## 📊 Resultados Esperados

### Ventajas

✅ **Simplicidad**: Fácil de entender e implementar  
✅ **Tendencias**: Funciona bien en mercados con tendencia clara  
✅ **Automatizable**: Señales objetivas y claras  

### Desventajas

❌ **Whipsaws**: Muchas señales falsas en mercados laterales  
❌ **Lag**: Señales tardías por naturaleza de las MAs  
❌ **Optimización**: Requiere ajuste de parámetros por activo  

### Métricas Típicas

- **Win Rate**: 40-50%
- **Sharpe Ratio**: 0.5-1.5
- **Max Drawdown**: 15-25%

## 🔧 Variaciones

### 1. Triple MA Crossover

```python
class TripleMACrossover(TradingStrategy):
    """Usa 3 MAs para confirmar tendencia."""
    
    def __init__(self, fast=10, medium=20, slow=50):
        self.fast = fast
        self.medium = medium
        self.slow = slow
    
    def generate_signals(self, data):
        ma_fast = data['Close'].rolling(self.fast).mean()
        ma_medium = data['Close'].rolling(self.medium).mean()
        ma_slow = data['Close'].rolling(self.slow).mean()
        
        signals = pd.DataFrame(index=data.index)
        
        # Compra: todas las MAs alineadas alcista
        signals['buy'] = (ma_fast > ma_medium) & (ma_medium > ma_slow)
        
        # Venta: todas las MAs alineadas bajista
        signals['sell'] = (ma_fast < ma_medium) & (ma_medium < ma_slow)
        
        return signals
```

### 2. MA con Filtro de Volumen

```python
def generate_signals_with_volume(self, data):
    """Señales confirmadas por volumen."""
    signals = self.generate_signals(data)
    
    # Volumen promedio
    avg_volume = data['Volume'].rolling(20).mean()
    
    # Solo señales con volumen alto
    signals['buy'] = signals['buy'] & (data['Volume'] > avg_volume * 1.5)
    signals['sell'] = signals['sell'] & (data['Volume'] > avg_volume * 1.5)
    
    return signals
```

## 📚 Referencias

- [Moving Averages - Investopedia](https://www.investopedia.com/terms/m/movingaverage.asp)
- [VectorBT Documentation](https://vectorbt.dev/)
- [Technical Analysis Library](https://technical-analysis-library-in-python.readthedocs.io/)

---

**Próximo**: [RSI Strategy](rsi-strategy.md)
