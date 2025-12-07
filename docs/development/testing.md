# 🧪 Testing

Guía completa de testing para el Trading Bot.

## 🎯 Filosofía de Testing

- **Test-Driven Development (TDD)** cuando sea posible
- **Cobertura mínima**: 80%
- **Tests automatizados** en CI/CD
- **Tests antes de merge** a develop/main

## 📊 Pirámide de Testing

```
        /\
       /  \      E2E Tests (10%)
      /____\
     /      \    Integration Tests (30%)
    /________\
   /          \  Unit Tests (60%)
  /____________\
```

## 🧪 Unit Testing

### Configuración

```bash
pip install pytest pytest-cov pytest-mock
```

### Estructura

```
tests/
├── unit/
│   ├── test_strategies.py
│   ├── test_indicators.py
│   ├── test_risk_manager.py
│   └── test_utils.py
├── integration/
│   ├── test_alpaca_integration.py
│   └── test_database.py
├── e2e/
│   └── test_trading_workflow.py
└── conftest.py  # Fixtures compartidos
```

### Ejemplo de Unit Test

```python
# tests/unit/test_indicators.py
import pytest
import pandas as pd
import numpy as np
from src.indicators import calculate_rsi, calculate_ma

class TestRSI:
    """Tests para el indicador RSI."""
    
    def test_rsi_range(self):
        """RSI debe estar entre 0 y 100."""
        prices = pd.Series([100, 102, 101, 103, 105, 104, 106, 108])
        rsi = calculate_rsi(prices, period=14)
        
        assert (rsi >= 0).all()
        assert (rsi <= 100).all()
    
    def test_rsi_oversold(self):
        """RSI debe detectar sobreventa."""
        prices = pd.Series([100, 95, 90, 85, 80, 75, 70, 65])
        rsi = calculate_rsi(prices, period=14)
        
        assert rsi.iloc[-1] < 30
    
    def test_rsi_with_nan(self):
        """RSI debe manejar valores NaN."""
        prices = pd.Series([100, np.nan, 101, 103])
        rsi = calculate_rsi(prices, period=14)
        
        assert not rsi.isna().all()

class TestMovingAverage:
    """Tests para medias móviles."""
    
    def test_sma_calculation(self):
        """SMA debe calcular correctamente."""
        prices = pd.Series([10, 20, 30, 40, 50])
        sma = calculate_ma(prices, period=3)
        
        expected = pd.Series([np.nan, np.nan, 20, 30, 40])
        pd.testing.assert_series_equal(sma, expected)
    
    def test_ema_calculation(self):
        """EMA debe calcular correctamente."""
        prices = pd.Series([10, 20, 30, 40, 50])
        ema = calculate_ma(prices, period=3, ma_type='ema')
        
        assert not ema.isna().all()
        assert len(ema) == len(prices)
```

### Fixtures

```python
# tests/conftest.py
import pytest
import pandas as pd
from datetime import datetime, timedelta

@pytest.fixture
def sample_ohlcv_data():
    """Genera datos OHLCV de ejemplo."""
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    
    data = pd.DataFrame({
        'Open': np.random.uniform(90, 110, 100),
        'High': np.random.uniform(95, 115, 100),
        'Low': np.random.uniform(85, 105, 100),
        'Close': np.random.uniform(90, 110, 100),
        'Volume': np.random.randint(1000000, 10000000, 100)
    }, index=dates)
    
    return data

@pytest.fixture
def mock_alpaca_api(mocker):
    """Mock de Alpaca API."""
    mock_api = mocker.Mock()
    mock_api.get_account.return_value = mocker.Mock(
        equity='100000',
        cash='50000',
        buying_power='100000'
    )
    return mock_api
```

## 🔗 Integration Testing

```python
# tests/integration/test_alpaca_integration.py
import pytest
import os
from src.brokers.alpaca_client import AlpacaClient

@pytest.mark.integration
class TestAlpacaIntegration:
    """Tests de integración con Alpaca API."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup para cada test."""
        self.client = AlpacaClient()
    
    def test_connection(self):
        """Test conexión a Alpaca."""
        account = self.client.get_account()
        
        assert account is not None
        assert hasattr(account, 'equity')
        assert hasattr(account, 'buying_power')
    
    def test_get_market_data(self):
        """Test obtención de datos de mercado."""
        data = self.client.get_bars('AAPL', '1Day', limit=10)
        
        assert data is not None
        assert len(data) > 0
        assert 'close' in data.columns
    
    @pytest.mark.slow
    def test_place_and_cancel_order(self):
        """Test colocar y cancelar orden."""
        # Colocar orden
        order = self.client.submit_order(
            symbol='AAPL',
            qty=1,
            side='buy',
            type='limit',
            limit_price=1.00  # Precio muy bajo, no se ejecutará
        )
        
        assert order is not None
        assert order.status in ['new', 'accepted']
        
        # Cancelar orden
        self.client.cancel_order(order.id)
        
        # Verificar cancelación
        cancelled_order = self.client.get_order(order.id)
        assert cancelled_order.status == 'canceled'
```

## 🎭 End-to-End Testing

```python
# tests/e2e/test_trading_workflow.py
import pytest
from src.bot import TradingBot
from src.strategies.rsi_strategy import RSIStrategy

@pytest.mark.e2e
class TestTradingWorkflow:
    """Tests end-to-end del flujo de trading."""
    
    def test_complete_trading_cycle(self):
        """Test ciclo completo de trading."""
        # Configurar bot
        config = {
            'strategy': 'rsi',
            'symbols': ['AAPL'],
            'paper_trading': True
        }
        
        bot = TradingBot(config)
        
        # Ejecutar ciclo
        bot.run_cycle()
        
        # Verificar resultados
        positions = bot.get_positions()
        orders = bot.get_orders()
        
        assert positions is not None
        assert orders is not None
    
    def test_strategy_execution(self):
        """Test ejecución de estrategia."""
        strategy = RSIStrategy(period=14)
        bot = TradingBot(strategy=strategy)
        
        # Simular ejecución
        signals = bot.generate_signals('AAPL')
        
        assert 'buy' in signals.columns
        assert 'sell' in signals.columns
```

## 🎯 Mocking

```python
# tests/unit/test_order_executor.py
import pytest
from unittest.mock import Mock, patch
from src.execution.order_executor import OrderExecutor

class TestOrderExecutor:
    """Tests para OrderExecutor con mocking."""
    
    @patch('src.brokers.alpaca_client.AlpacaClient')
    def test_execute_buy_order(self, mock_alpaca):
        """Test ejecución de orden de compra."""
        # Configurar mock
        mock_alpaca.return_value.submit_order.return_value = Mock(
            id='order123',
            status='filled',
            symbol='AAPL',
            qty=10
        )
        
        # Ejecutar
        executor = OrderExecutor(mock_alpaca())
        order = executor.execute_buy('AAPL', 10)
        
        # Verificar
        assert order.id == 'order123'
        assert order.status == 'filled'
        mock_alpaca.return_value.submit_order.assert_called_once()
```

## 📊 Coverage

### Ejecutar con Coverage

```bash
# Coverage básico
pytest --cov=src

# Coverage con reporte HTML
pytest --cov=src --cov-report=html

# Coverage con reporte en terminal
pytest --cov=src --cov-report=term-missing

# Coverage mínimo requerido
pytest --cov=src --cov-fail-under=80
```

### Configuración de Coverage

```ini
# .coveragerc
[run]
source = src
omit =
    */tests/*
    */venv/*
    */__init__.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
```

## 🚀 Comandos de Testing

```bash
# Todos los tests
pytest

# Tests específicos
pytest tests/unit/test_indicators.py
pytest tests/unit/test_indicators.py::TestRSI::test_rsi_range

# Por marcadores
pytest -m unit
pytest -m integration
pytest -m "not slow"

# Verbose
pytest -v

# Con output
pytest -s

# Parallel execution
pytest -n auto

# Stop on first failure
pytest -x

# Last failed
pytest --lf
```

## ⚙️ Configuración pytest

```ini
# pytest.ini
[pytest]
minversion = 6.0
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow tests

addopts =
    -v
    --strict-markers
    --cov=src
    --cov-report=term-missing
    --cov-fail-under=80
```

## 📚 Best Practices

### 1. Nombres Descriptivos

```python
# ✅ BUENO
def test_rsi_returns_values_between_0_and_100():
    pass

# ❌ MALO
def test_rsi():
    pass
```

### 2. Arrange-Act-Assert

```python
def test_calculate_position_size():
    # Arrange
    account_value = 10000
    price = 100
    risk_pct = 0.1
    
    # Act
    position_size = calculate_position_size(account_value, price, risk_pct)
    
    # Assert
    assert position_size == 10
```

### 3. Un Assert por Test (cuando sea posible)

```python
# ✅ BUENO
def test_rsi_minimum_value():
    rsi = calculate_rsi(prices)
    assert (rsi >= 0).all()

def test_rsi_maximum_value():
    rsi = calculate_rsi(prices)
    assert (rsi <= 100).all()

# ❌ MALO (múltiples asserts no relacionados)
def test_rsi():
    rsi = calculate_rsi(prices)
    assert (rsi >= 0).all()
    assert (rsi <= 100).all()
    assert len(rsi) == len(prices)
```

### 4. Usar Fixtures

```python
@pytest.fixture
def trading_strategy():
    return RSIStrategy(period=14)

def test_strategy_generates_signals(trading_strategy):
    signals = trading_strategy.generate_signals(data)
    assert signals is not None
```

## 🔄 CI/CD Integration

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

---

**Recursos**:
- [pytest Documentation](https://docs.pytest.org/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)
