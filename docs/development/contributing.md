# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al Trading Bot Híbrido! Esta guía te ayudará a empezar.

## 📋 Tabla de Contenidos

1. [Código de Conducta](#código-de-conducta)
2. [Cómo Contribuir](#cómo-contribuir)
3. [Proceso de Development](#proceso-de-development)
4. [Estándares de Código](#estándares-de-código)
5. [Pull Requests](#pull-requests)
6. [Reportar Bugs](#reportar-bugs)
7. [Sugerir Features](#sugerir-features)

## 📜 Código de Conducta

### Nuestro Compromiso

Nos comprometemos a hacer de este proyecto una experiencia libre de acoso para todos, independientemente de:
- Edad
- Tamaño corporal
- Discapacidad
- Etnia
- Identidad y expresión de género
- Nivel de experiencia
- Nacionalidad
- Apariencia personal
- Raza
- Religión
- Identidad y orientación sexual

### Comportamiento Esperado

✅ **SÍ**:
- Usar lenguaje acogedor e inclusivo
- Respetar diferentes puntos de vista
- Aceptar críticas constructivas
- Enfocarse en lo mejor para la comunidad
- Mostrar empatía hacia otros miembros

❌ **NO**:
- Usar lenguaje o imágenes sexualizadas
- Trolling, comentarios insultantes o ataques personales
- Acoso público o privado
- Publicar información privada de otros
- Conducta no profesional

## 🚀 Cómo Contribuir

### Formas de Contribuir

1. **Reportar bugs** 🐛
2. **Sugerir nuevas features** 💡
3. **Mejorar documentación** 📚
4. **Escribir código** 💻
5. **Revisar Pull Requests** 👀
6. **Ayudar a otros usuarios** 🤝

### Primeros Pasos

1. **Fork el repositorio**
   ```bash
   # Haz clic en "Fork" en GitHub
   ```

2. **Clona tu fork**
   ```bash
   git clone https://github.com/tu-usuario/trading-bot.git
   cd trading-bot
   ```

3. **Agrega el repositorio original como upstream**
   ```bash
   git remote add upstream https://github.com/original-owner/trading-bot.git
   ```

4. **Crea un entorno virtual**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Dependencias de desarrollo
   ```

## 🔧 Proceso de Development

### 1. Sincroniza tu Fork

```bash
git checkout develop
git fetch upstream
git merge upstream/develop
```

### 2. Crea una Rama de Feature

```bash
# Para nueva funcionalidad
git checkout -b feat/nombre-descriptivo

# Para bug fix
git checkout -b fix/descripcion-del-bug

# Para documentación
git checkout -b docs/que-documentas
```

### 3. Desarrolla tu Feature

```python
# Escribe código limpio y bien documentado
def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """
    Calcula el Relative Strength Index (RSI).
    
    Args:
        prices: Serie de precios
        period: Período para el cálculo (default: 14)
    
    Returns:
        Serie con valores de RSI (0-100)
    
    Example:
        >>> prices = pd.Series([100, 102, 101, 103, 105])
        >>> rsi = calculate_rsi(prices, period=14)
    """
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi
```

### 4. Escribe Tests

```python
# tests/test_indicators.py
import pytest
import pandas as pd
from src.indicators import calculate_rsi

def test_rsi_range():
    """RSI debe estar entre 0 y 100."""
    prices = pd.Series([100, 102, 101, 103, 105, 104, 106, 108])
    rsi = calculate_rsi(prices, period=14)
    
    assert (rsi >= 0).all()
    assert (rsi <= 100).all()

def test_rsi_oversold():
    """RSI debe detectar condiciones de sobreventa."""
    # Precios en tendencia bajista
    prices = pd.Series([100, 95, 90, 85, 80, 75, 70, 65])
    rsi = calculate_rsi(prices, period=14)
    
    # RSI debería ser bajo
    assert rsi.iloc[-1] < 30

def test_rsi_overbought():
    """RSI debe detectar condiciones de sobrecompra."""
    # Precios en tendencia alcista
    prices = pd.Series([100, 105, 110, 115, 120, 125, 130, 135])
    rsi = calculate_rsi(prices, period=14)
    
    # RSI debería ser alto
    assert rsi.iloc[-1] > 70
```

### 5. Ejecuta Tests

```bash
# Todos los tests
pytest

# Con coverage
pytest --cov=src --cov-report=html

# Solo tests unitarios
pytest tests/unit/

# Tests específicos
pytest tests/test_indicators.py::test_rsi_range
```

### 6. Verifica el Código

```bash
# Linting
flake8 src/ tests/

# Type checking
mypy src/

# Format checking
black --check src/ tests/
```

### 7. Commit tus Cambios

Usamos **Conventional Commits**:

```bash
# Formato
<type>(<scope>): <subject>

# Tipos
feat:     Nueva funcionalidad
fix:      Bug fix
docs:     Documentación
style:    Formato de código
refactor: Refactorización
test:     Tests
chore:    Mantenimiento

# Ejemplos
git commit -m "feat(indicators): add RSI calculation function

- Implement RSI calculation with configurable period
- Add comprehensive unit tests
- Update documentation with examples"

git commit -m "fix(alpaca): handle connection timeout errors

Fixes #123"

git commit -m "docs(readme): update installation instructions"
```

### 8. Push a tu Fork

```bash
git push origin feat/nombre-descriptivo
```

### 9. Crea Pull Request

1. Ve a tu fork en GitHub
2. Haz clic en "Pull Request"
3. Selecciona `develop` como base branch
4. Completa la plantilla de PR

## 📝 Estándares de Código

### Python Style Guide

Seguimos **PEP 8** con algunas adaptaciones:

```python
# ✅ BUENO

class RSIStrategy(TradingStrategy):
    """Estrategia basada en RSI."""
    
    def __init__(self, period: int = 14, oversold: float = 30, 
                 overbought: float = 70):
        """
        Inicializa la estrategia RSI.
        
        Args:
            period: Período para calcular RSI
            oversold: Umbral de sobreventa
            overbought: Umbral de sobrecompra
        """
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Genera señales de trading."""
        rsi = self.calculate_rsi(data['Close'])
        
        signals = pd.DataFrame(index=data.index)
        signals['buy'] = rsi < self.oversold
        signals['sell'] = rsi > self.overbought
        
        return signals


# ❌ MALO

class rsistrategy:  # Nombre no sigue PascalCase
    def __init__(self,p,o,ob):  # Nombres no descriptivos
        self.p=p  # Sin espacios
        self.o=o
        self.ob=ob
    
    def gen_sig(self,d):  # Sin type hints, sin docstring
        r=self.calc_rsi(d['Close'])  # Nombres abreviados
        s=pd.DataFrame(index=d.index)
        s['buy']=r<self.o
        s['sell']=r>self.ob
        return s
```

### Convenciones de Nombres

```python
# Clases: PascalCase
class TradingStrategy:
    pass

# Funciones y variables: snake_case
def calculate_moving_average():
    total_return = 0.0

# Constantes: UPPER_SNAKE_CASE
MAX_POSITION_SIZE = 1000
DEFAULT_PERIOD = 14

# Privados: prefijo con _
class MyClass:
    def __init__(self):
        self._private_var = 0
    
    def _private_method(self):
        pass
```

### Documentación

```python
def backtest_strategy(
    strategy: TradingStrategy,
    data: pd.DataFrame,
    initial_capital: float = 10000,
    commission: float = 0.001
) -> Dict[str, float]:
    """
    Ejecuta backtest de una estrategia de trading.
    
    Esta función simula el rendimiento histórico de una estrategia
    de trading usando datos OHLCV.
    
    Args:
        strategy: Instancia de TradingStrategy a testear
        data: DataFrame con columnas OHLCV (Open, High, Low, Close, Volume)
        initial_capital: Capital inicial en USD (default: 10000)
        commission: Comisión por operación como decimal (default: 0.001 = 0.1%)
    
    Returns:
        Diccionario con métricas de rendimiento:
        - 'total_return': Retorno total como decimal
        - 'sharpe_ratio': Sharpe ratio anualizado
        - 'max_drawdown': Máximo drawdown como decimal
        - 'win_rate': Porcentaje de operaciones ganadoras
    
    Raises:
        ValueError: Si data no contiene las columnas requeridas
        TypeError: Si strategy no es instancia de TradingStrategy
    
    Example:
        >>> strategy = RSIStrategy(period=14)
        >>> data = load_historical_data('AAPL', '2023-01-01', '2024-01-01')
        >>> results = backtest_strategy(strategy, data)
        >>> print(f"Total Return: {results['total_return']:.2%}")
        Total Return: 15.32%
    """
    # Implementación...
    pass
```

### Type Hints

```python
from typing import List, Dict, Optional, Union, Tuple
import pandas as pd

def process_signals(
    signals: pd.DataFrame,
    symbols: List[str],
    config: Dict[str, Union[int, float]],
    risk_limit: Optional[float] = None
) -> Tuple[List[str], Dict[str, float]]:
    """Procesa señales de trading con type hints."""
    pass
```

## 🔍 Pull Requests

### Plantilla de PR

```markdown
## Descripción
Breve descripción de los cambios realizados.

## Tipo de Cambio
- [ ] Bug fix (cambio que corrige un issue)
- [ ] Nueva feature (cambio que agrega funcionalidad)
- [ ] Breaking change (fix o feature que causa que funcionalidad existente no funcione como antes)
- [ ] Documentación

## ¿Cómo se ha testeado?
Describe las pruebas que ejecutaste para verificar tus cambios.

- [ ] Test A
- [ ] Test B

## Checklist
- [ ] Mi código sigue los estándares del proyecto
- [ ] He realizado self-review de mi código
- [ ] He comentado mi código, especialmente en áreas difíciles
- [ ] He actualizado la documentación
- [ ] Mis cambios no generan nuevos warnings
- [ ] He agregado tests que prueban que mi fix es efectivo o que mi feature funciona
- [ ] Tests unitarios nuevos y existentes pasan localmente
- [ ] Cambios dependientes han sido merged

## Screenshots (si aplica)
Agrega screenshots para ayudar a explicar tus cambios.

## Issues Relacionados
Fixes #123
Closes #456
```

### Proceso de Review

1. **Automated Checks**
   - Tests deben pasar
   - Linting debe pasar
   - Coverage no debe disminuir

2. **Code Review**
   - Al menos 1 aprobación requerida
   - Todos los comentarios deben ser resueltos

3. **Merge**
   - Squash and merge para features
   - Merge commit para releases

## 🐛 Reportar Bugs

### Antes de Reportar

1. Verifica que usas la última versión
2. Busca en issues existentes
3. Intenta reproducir el bug

### Plantilla de Bug Report

```markdown
## Descripción del Bug
Descripción clara y concisa del bug.

## Para Reproducir
Pasos para reproducir el comportamiento:
1. Ve a '...'
2. Ejecuta '...'
3. Observa error

## Comportamiento Esperado
Descripción de lo que esperabas que sucediera.

## Comportamiento Actual
Descripción de lo que realmente sucedió.

## Screenshots
Si aplica, agrega screenshots.

## Entorno
- OS: [e.g. Windows 11]
- Python Version: [e.g. 3.10.5]
- Trading Bot Version: [e.g. 1.0.0]

## Logs
```
Pega logs relevantes aquí
```

## Contexto Adicional
Cualquier otra información relevante.
```

## 💡 Sugerir Features

### Plantilla de Feature Request

```markdown
## ¿Tu feature request está relacionada con un problema?
Descripción clara del problema. Ej: "Siempre me frustra cuando [...]"

## Describe la solución que te gustaría
Descripción clara de lo que quieres que suceda.

## Describe alternativas que has considerado
Descripción de soluciones o features alternativas.

## Contexto Adicional
Cualquier otro contexto o screenshots sobre el feature request.

## Beneficios
- Beneficio 1
- Beneficio 2

## Posibles Desventajas
- Desventaja 1
- Desventaja 2
```

## 🏆 Reconocimiento

Los contribuidores serán reconocidos en:
- README.md (sección Contributors)
- Release notes
- Documentación

## 📚 Recursos

- [Conventional Commits](https://www.conventionalcommits.org/)
- [PEP 8](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)

## 🆘 ¿Necesitas Ayuda?

- **GitHub Discussions**: Para preguntas generales
- **GitHub Issues**: Para bugs y features
- **Email**: [tu-email@example.com]

---

¡Gracias por contribuir! 🎉
