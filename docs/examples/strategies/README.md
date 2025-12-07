# 📚 Ejemplos de Estrategias de Trading

Esta carpeta contiene ejemplos de estrategias de trading implementadas para el Trading Bot.

## 🎯 Estrategias Disponibles

### 1. [Media Móvil (Moving Average)](moving-average.md)
Estrategia basada en el cruce de medias móviles.

**Características**:
- Simplicidad y claridad
- Funciona bien en tendencias
- Parámetros configurables

**Nivel**: Principiante

---

### 2. [RSI Strategy](rsi-strategy.md)
Estrategia basada en el indicador RSI (Relative Strength Index).

**Características**:
- Detecta sobrecompra/sobreventa
- Ideal para reversiones
- Múltiples variaciones

**Nivel**: Principiante-Intermedio

---

## 🚀 Cómo Usar

### 1. Estudiar la Estrategia
Lee la documentación de cada estrategia para entender:
- Lógica de trading
- Parámetros configurables
- Ventajas y desventajas

### 2. Backtest
Prueba la estrategia con datos históricos:

```python
from src.strategies.ma_crossover_strategy import MACrossoverStrategy
import vectorbt as vbt

# Descargar datos
data = vbt.YFData.download('AAPL', start='2023-01-01').get('Close')

# Crear estrategia
strategy = MACrossoverStrategy(fast_period=20, slow_period=50)

# Backtest
signals = strategy.generate_signals(pd.DataFrame({'Close': data}))
portfolio = vbt.Portfolio.from_signals(data, signals['buy'], signals['sell'])

# Resultados
print(portfolio.stats())
```

### 3. Optimizar
Encuentra los mejores parámetros para tu activo:

```python
# Ver ejemplos de optimización en cada estrategia
```

### 4. Paper Trading
Prueba en paper trading antes de usar dinero real:

```python
# Configurar en configs/.env
ALPACA_BASE_URL=https://paper-api.alpaca.markets
```

### 5. Live Trading
Solo después de validar exhaustivamente:

```python
# ⚠️ CUIDADO: Dinero real
ALPACA_BASE_URL=https://api.alpaca.markets
```

## 📊 Comparación de Estrategias

| Estrategia | Complejidad | Win Rate | Sharpe | Mejor en |
|------------|-------------|----------|--------|----------|
| MA Crossover | Baja | 40-50% | 0.5-1.5 | Tendencias |
| RSI | Media | 45-55% | 0.8-1.8 | Reversiones |

## 🔧 Crear Tu Propia Estrategia

### Plantilla Base

```python
# src/strategies/my_strategy.py
from .base import TradingStrategy
import pandas as pd

class MyStrategy(TradingStrategy):
    """Tu estrategia personalizada."""
    
    def __init__(self, param1=10, param2=20):
        super().__init__({'name': 'My Strategy'})
        self.param1 = param1
        self.param2 = param2
    
    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calcula indicadores necesarios."""
        data = data.copy()
        # Tu lógica aquí
        return data
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Genera señales de trading."""
        data = self.calculate_indicators(data)
        
        signals = pd.DataFrame(index=data.index)
        # Tu lógica de señales aquí
        signals['buy'] = False  # Condición de compra
        signals['sell'] = False  # Condición de venta
        
        return signals
```

## 📚 Recursos de Aprendizaje

### Libros
- "Algorithmic Trading" - Ernest P. Chan
- "Quantitative Trading" - Ernest P. Chan
- "Python for Finance" - Yves Hilpisch

### Cursos Online
- [QuantConnect](https://www.quantconnect.com/)
- [Quantopian Lectures](https://www.quantopian.com/lectures)
- [Coursera - Machine Learning for Trading](https://www.coursera.org/)

### Comunidades
- [QuantConnect Forum](https://www.quantconnect.com/forum)
- [Reddit r/algotrading](https://www.reddit.com/r/algotrading/)
- [Alpaca Community](https://forum.alpaca.markets/)

## ⚠️ Advertencias

1. **Backtesting ≠ Resultados Futuros**
   - El rendimiento pasado no garantiza resultados futuros
   - Siempre prueba en paper trading primero

2. **Overfitting**
   - No optimices demasiado los parámetros
   - Usa datos out-of-sample para validar

3. **Costos de Trading**
   - Considera comisiones y slippage
   - Más trades = más costos

4. **Gestión de Riesgo**
   - Nunca arriesgues más del 1-2% por trade
   - Usa stop losses
   - Diversifica

## 🆘 Soporte

¿Preguntas sobre las estrategias?
- [GitHub Issues](https://github.com/tu-usuario/trading-bot/issues)
- [Discussions](https://github.com/tu-usuario/trading-bot/discussions)

---

**¡Feliz Trading!** 📈
