# 📜 Reglas de Desarrollo - Trading Bot

**Versión**: 1.0.0  
**Última Actualización**: 2024-12-07  
**Estado**: ✅ Activo

---

## 🎯 Objetivo

Establecer reglas claras y consistentes para el desarrollo del Trading Bot, asegurando calidad, mantenibilidad y colaboración efectiva.

---

## 📋 Tabla de Contenidos

1. [Git y Control de Versiones](#git-y-control-de-versiones)
2. [Conventional Commits](#conventional-commits)
3. [Branching Strategy](#branching-strategy)
4. [Code Review](#code-review)
5. [Estándares de Código](#estándares-de-código)
6. [Testing](#testing)
7. [Documentación](#documentación)
8. [Seguridad](#seguridad)
9. [Performance](#performance)
10. [Deployment](#deployment)

---

## 🔀 Git y Control de Versiones

### Reglas Generales

1. **✅ OBLIGATORIO**: Usar Conventional Commits en español
2. **✅ OBLIGATORIO**: Commits atómicos (un cambio lógico por commit)
3. **✅ OBLIGATORIO**: Mensajes descriptivos y claros
4. **❌ PROHIBIDO**: Commits directos a `main` o `develop`
5. **❌ PROHIBIDO**: Force push a ramas compartidas
6. **❌ PROHIBIDO**: Commits con archivos `.env` o credenciales

### Configuración Requerida

```bash
# Configurar nombre y email
git config user.name "Tu Nombre"
git config user.email "tu.email@example.com"

# Configurar editor
git config core.editor "code --wait"

# Configurar line endings
git config core.autocrlf true  # Windows
git config core.autocrlf input  # Linux/Mac
```

---

## 📝 Conventional Commits

### Formato

```
<tipo>(<ámbito>): <descripción corta>

<cuerpo opcional>

<footer opcional>
```

### Tipos Permitidos

| Tipo | Uso | Ejemplo |
|------|-----|---------|
| **feat** | Nueva funcionalidad | `feat(strategies): añadir estrategia RSI` |
| **fix** | Corrección de bug | `fix(alpaca): corregir timeout en API` |
| **docs** | Documentación | `docs(readme): actualizar guía de instalación` |
| **style** | Formato de código | `style(main): aplicar black formatter` |
| **refactor** | Refactorización | `refactor(data): simplificar cache layer` |
| **perf** | Mejora de performance | `perf(signals): optimizar cálculo de RSI` |
| **test** | Tests | `test(strategies): añadir tests para MA` |
| **build** | Sistema de build | `build(docker): actualizar Dockerfile` |
| **ci** | CI/CD | `ci(github): añadir workflow de tests` |
| **chore** | Tareas de mantenimiento | `chore(deps): actualizar dependencias` |
| **revert** | Revertir cambio | `revert: revertir feat(strategies)` |

### Ámbitos Comunes

- `strategies` - Estrategias de trading
- `data` - Capa de datos
- `brokers` - Integraciones con brokers
- `execution` - Ejecución de órdenes
- `alerts` - Sistema de alertas
- `backtesting` - Motor de backtesting
- `utils` - Utilidades
- `config` - Configuración
- `docs` - Documentación

### Ejemplos de Commits

#### ✅ BUENOS

```bash
# Nueva funcionalidad
git commit -m "feat(strategies): implementar estrategia RSI

- Añadir clase RSIStrategy con parámetros configurables
- Implementar cálculo de RSI con período ajustable
- Añadir señales de compra/venta basadas en umbrales
- Incluir tests unitarios con 95% coverage

Closes #32"

# Corrección de bug
git commit -m "fix(alpaca): corregir manejo de timeout en get_bars

El cliente de Alpaca no manejaba correctamente los timeouts
de red, causando que el bot se detuviera.

- Añadir timeout de 5 segundos a todas las llamadas API
- Implementar retry con backoff exponencial
- Añadir logging de errores de red

Fixes #45"

# Documentación
git commit -m "docs(architecture): añadir diagramas de flujo de datos

- Crear diagramas Mermaid para flujo de trading
- Documentar flujo de backtesting
- Añadir ejemplos de uso"

# Refactorización
git commit -m "refactor(data): extraer lógica de cache a clase separada

- Crear CacheLayer como clase independiente
- Implementar interface para diferentes backends
- Añadir soporte para Redis (opcional)
- Mantener compatibilidad con cache in-memory

BREAKING CHANGE: DataManager ahora requiere CacheLayer en constructor"
```

#### ❌ MALOS

```bash
# Muy vago
git commit -m "fix bug"

# Sin tipo
git commit -m "añadir nueva feature"

# Mezcla múltiples cambios
git commit -m "feat: añadir RSI, fix bugs, update docs"

# En inglés (debe ser español)
git commit -m "feat: add RSI strategy"
```

### Breaking Changes

Para cambios que rompen compatibilidad:

```bash
git commit -m "feat(config): cambiar formato de configuración a YAML

Migrar de JSON a YAML para mejor legibilidad.

BREAKING CHANGE: Los archivos config.json deben convertirse a config.yaml
Ver docs/migration/v2.0.md para guía de migración"
```

---

## 🌿 Branching Strategy

### Ramas Principales

```
main (producción)
  ↑
develop (desarrollo)
  ↑
feature/* (nuevas features)
hotfix/* (fixes urgentes)
release/* (preparación de releases)
```

### Nomenclatura de Ramas

#### Feature Branches

```bash
# Formato: feat/<task-id>-<descripcion-corta>
git checkout -b feat/TASK-032-rsi-strategy
git checkout -b feat/TASK-025-data-manager
```

#### Fix Branches

```bash
# Formato: fix/<task-id>-<descripcion-corta>
git checkout -b fix/TASK-047-alpaca-timeout
git checkout -b fix/critical-order-execution
```

#### Hotfix Branches

```bash
# Formato: hotfix/<version>-<descripcion>
git checkout -b hotfix/v1.0.1-security-patch
```

#### Release Branches

```bash
# Formato: release/<version>
git checkout -b release/v1.0.0
```

### Workflow de Feature

```bash
# 1. Crear rama desde develop
git checkout develop
git pull origin develop
git checkout -b feat/TASK-032-rsi-strategy

# 2. Desarrollar y commitear
git add src/strategies/rsi_strategy.py
git commit -m "feat(strategies): implementar estrategia RSI"

# 3. Mantener actualizado con develop
git fetch origin
git rebase origin/develop

# 4. Push y crear PR
git push origin feat/TASK-032-rsi-strategy
# Crear Pull Request en GitHub

# 5. Después de merge, eliminar rama local
git checkout develop
git pull origin develop
git branch -d feat/TASK-032-rsi-strategy
```

---

## 👀 Code Review

### Reglas de Code Review

1. **✅ OBLIGATORIO**: Al menos 1 aprobación antes de merge
2. **✅ OBLIGATORIO**: Todos los comentarios resueltos
3. **✅ OBLIGATORIO**: Tests pasando
4. **✅ OBLIGATORIO**: Coverage no disminuye
5. **⚠️ RECOMENDADO**: Revisar en menos de 24 horas

### Checklist del Reviewer

- [ ] **Funcionalidad**: ¿El código hace lo que debe hacer?
- [ ] **Tests**: ¿Hay tests adecuados?
- [ ] **Documentación**: ¿Está documentado?
- [ ] **Estándares**: ¿Sigue los estándares de código?
- [ ] **Performance**: ¿Hay problemas de rendimiento?
- [ ] **Seguridad**: ¿Hay vulnerabilidades?
- [ ] **Mantenibilidad**: ¿Es fácil de entender y mantener?

### Comentarios de Review

#### ✅ BUENOS

```
# Constructivo y específico
"Considera usar un diccionario aquí en lugar de múltiples if-else 
para mejor mantenibilidad. Ejemplo: {...}"

# Pregunta para entender
"¿Por qué elegiste este enfoque en lugar de usar el patrón Strategy?"

# Sugerencia con justificación
"Sugiero añadir un timeout aquí para evitar bloqueos indefinidos 
en caso de problemas de red."
```

#### ❌ MALOS

```
# Muy vago
"Esto no se ve bien"

# Sin contexto
"Cambiar esto"

# Agresivo
"Esto está mal hecho"
```

---

## 💻 Estándares de Código

### Python Style Guide

Seguimos **PEP 8** con estas especificaciones:

#### Formato

```python
# ✅ BUENO

class TradingStrategy(ABC):
    """
    Clase base para estrategias de trading.
    
    Esta clase define la interfaz que todas las estrategias
    deben implementar.
    
    Attributes:
        name (str): Nombre de la estrategia
        config (dict): Configuración de la estrategia
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa la estrategia.
        
        Args:
            config: Diccionario de configuración
            
        Raises:
            ValueError: Si la configuración es inválida
        """
        self.name = config.get('name', 'UnnamedStrategy')
        self.config = config
    
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Genera señales de trading.
        
        Args:
            data: DataFrame con datos OHLCV
            
        Returns:
            DataFrame con columnas 'buy' y 'sell'
            
        Example:
            >>> strategy = RSIStrategy()
            >>> signals = strategy.generate_signals(data)
            >>> print(signals.head())
        """
        pass


# ❌ MALO

class tradingstrategy:  # Nombre no sigue PascalCase
    def __init__(self,c):  # Sin type hints, sin docstring
        self.c=c  # Sin espacios, nombre no descriptivo
    
    def gen_sig(self,d):  # Nombre abreviado, sin documentación
        pass
```

#### Type Hints

```python
# ✅ OBLIGATORIO usar type hints

from typing import List, Dict, Optional, Union
import pandas as pd

def calculate_rsi(
    prices: pd.Series,
    period: int = 14
) -> pd.Series:
    """Calcula RSI."""
    pass

def execute_order(
    symbol: str,
    qty: int,
    side: str,
    order_type: str = 'market'
) -> Optional[Dict[str, Any]]:
    """Ejecuta orden."""
    pass
```

#### Docstrings

```python
# ✅ OBLIGATORIO para clases y funciones públicas

def backtest_strategy(
    strategy: TradingStrategy,
    data: pd.DataFrame,
    initial_capital: float = 10000
) -> Dict[str, float]:
    """
    Ejecuta backtest de una estrategia.
    
    Args:
        strategy: Estrategia a testear
        data: Datos históricos OHLCV
        initial_capital: Capital inicial en USD
        
    Returns:
        Diccionario con métricas:
        - total_return: Retorno total
        - sharpe_ratio: Sharpe ratio
        - max_drawdown: Máximo drawdown
        
    Raises:
        ValueError: Si data no tiene columnas requeridas
        
    Example:
        >>> strategy = RSIStrategy()
        >>> results = backtest_strategy(strategy, data)
        >>> print(f"Return: {results['total_return']:.2%}")
    """
    pass
```

#### Naming Conventions

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
API_TIMEOUT = 5

# Privados: prefijo con _
class MyClass:
    def __init__(self):
        self._private_var = 0
    
    def _private_method(self):
        pass
```

### Herramientas de Calidad

#### Linting

```bash
# Flake8 (obligatorio)
flake8 src/ --max-line-length=100

# Pylint (recomendado)
pylint src/

# MyPy para type checking (obligatorio)
mypy src/
```

#### Formatting

```bash
# Black (obligatorio antes de commit)
black src/ tests/

# isort para imports (obligatorio)
isort src/ tests/
```

#### Pre-commit Hook

```bash
# Instalar pre-commit
pip install pre-commit

# Configurar
pre-commit install

# Ejecutar manualmente
pre-commit run --all-files
```

---

## 🧪 Testing

### Reglas de Testing

1. **✅ OBLIGATORIO**: Tests para toda nueva funcionalidad
2. **✅ OBLIGATORIO**: Coverage mínimo 80%
3. **✅ OBLIGATORIO**: Tests pasando antes de merge
4. **⚠️ RECOMENDADO**: TDD cuando sea posible

### Estructura de Tests

```
tests/
├── unit/              # Tests unitarios
│   ├── test_strategies.py
│   ├── test_indicators.py
│   └── test_utils.py
├── integration/       # Tests de integración
│   ├── test_alpaca.py
│   └── test_database.py
├── e2e/              # Tests end-to-end
│   └── test_trading_flow.py
└── conftest.py       # Fixtures compartidos
```

### Nomenclatura de Tests

```python
# ✅ BUENO - Descriptivo y claro

def test_rsi_returns_values_between_0_and_100():
    """RSI debe retornar valores entre 0 y 100."""
    pass

def test_order_executor_validates_insufficient_funds():
    """OrderExecutor debe rechazar órdenes sin fondos suficientes."""
    pass

def test_strategy_generates_buy_signal_when_rsi_below_30():
    """Estrategia debe generar señal de compra cuando RSI < 30."""
    pass


# ❌ MALO - Vago

def test_rsi():
    pass

def test_order():
    pass
```

### Patrón AAA (Arrange-Act-Assert)

```python
def test_calculate_position_size():
    """Test cálculo de tamaño de posición."""
    # Arrange (Preparar)
    account_value = 10000
    price = 100
    risk_pct = 0.1
    
    # Act (Actuar)
    position_size = calculate_position_size(account_value, price, risk_pct)
    
    # Assert (Afirmar)
    assert position_size == 10
    assert isinstance(position_size, int)
```

### Comandos de Testing

```bash
# Ejecutar todos los tests
pytest

# Con coverage
pytest --cov=src --cov-report=html --cov-report=term

# Solo unit tests
pytest tests/unit/

# Solo un archivo
pytest tests/unit/test_strategies.py

# Solo un test específico
pytest tests/unit/test_strategies.py::test_rsi_calculation

# Con output verbose
pytest -v

# Detener en primer fallo
pytest -x

# Re-ejecutar últimos fallos
pytest --lf
```

---

## 📚 Documentación

### Reglas de Documentación

1. **✅ OBLIGATORIO**: Actualizar docs con cada feature
2. **✅ OBLIGATORIO**: Docstrings en funciones públicas
3. **✅ OBLIGATORIO**: README actualizado
4. **⚠️ RECOMENDADO**: Ejemplos de código funcionales

### Actualización de Documentación

```bash
# Al añadir nueva feature
1. Actualizar docs/user-guide/ si aplica
2. Actualizar docs/examples/ con ejemplos
3. Actualizar TASK_LIST.md marcando tarea como completada
4. Actualizar ROADMAP.md si completa un hito

# Commit de documentación
git commit -m "docs(user-guide): añadir guía de estrategia RSI

- Documentar parámetros de RSIStrategy
- Añadir ejemplos de uso
- Incluir casos de uso comunes"
```

---

## 🔒 Seguridad

### Reglas de Seguridad

1. **❌ PROHIBIDO**: Commitear credenciales o API keys
2. **❌ PROHIBIDO**: Hardcodear secrets en código
3. **✅ OBLIGATORIO**: Usar variables de entorno
4. **✅ OBLIGATORIO**: Validar todos los inputs
5. **✅ OBLIGATORIO**: Sanitizar logs (no logear secrets)

### Gestión de Secrets

```python
# ✅ BUENO

import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('ALPACA_API_KEY_ID')
api_secret = os.getenv('ALPACA_API_SECRET_KEY')


# ❌ MALO

api_key = "PK1234567890"  # ❌ Hardcoded
api_secret = "secret123"  # ❌ Hardcoded
```

### Validación de Inputs

```python
# ✅ OBLIGATORIO validar inputs

def execute_order(symbol: str, qty: int, side: str):
    """Ejecuta orden con validación."""
    # Validar símbolo
    if not symbol or not symbol.isalpha():
        raise ValueError(f"Símbolo inválido: {symbol}")
    
    # Validar cantidad
    if qty <= 0:
        raise ValueError(f"Cantidad debe ser positiva: {qty}")
    
    # Validar side
    if side not in ['buy', 'sell']:
        raise ValueError(f"Side inválido: {side}")
    
    # Ejecutar orden...
```

---

## ⚡ Performance

### Reglas de Performance

1. **✅ OBLIGATORIO**: Profiling antes de optimizar
2. **⚠️ RECOMENDADO**: Usar operaciones vectorizadas (pandas/numpy)
3. **⚠️ RECOMENDADO**: Cachear resultados costosos
4. **❌ EVITAR**: Loops innecesarios

### Optimización

```python
# ✅ BUENO - Vectorizado

def calculate_signals_fast(data: pd.DataFrame) -> pd.DataFrame:
    """Cálculo vectorizado de señales."""
    data['SMA_20'] = data['close'].rolling(20).mean()
    data['SMA_50'] = data['close'].rolling(50).mean()
    
    data['buy'] = data['SMA_20'] > data['SMA_50']
    data['sell'] = data['SMA_20'] < data['SMA_50']
    
    return data


# ❌ MALO - Loop lento

def calculate_signals_slow(data: pd.DataFrame) -> pd.DataFrame:
    """Cálculo con loops (lento)."""
    signals = []
    for i in range(len(data)):
        # Cálculo manual lento...
        pass
    return pd.DataFrame(signals)
```

---

## 🚀 Deployment

### Reglas de Deployment

1. **✅ OBLIGATORIO**: Tests pasando en CI/CD
2. **✅ OBLIGATORIO**: Code review aprobado
3. **✅ OBLIGATORIO**: Documentación actualizada
4. **✅ OBLIGATORIO**: Backup antes de deploy
5. **⚠️ RECOMENDADO**: Deploy gradual (canary)

### Checklist de Deployment

- [ ] Todos los tests pasan
- [ ] Coverage > 80%
- [ ] Code review aprobado
- [ ] Documentación actualizada
- [ ] CHANGELOG.md actualizado
- [ ] Variables de entorno configuradas
- [ ] Backup de base de datos realizado
- [ ] Plan de rollback preparado
- [ ] Monitoreo configurado

---

## 📊 Métricas de Calidad

### Métricas Requeridas

| Métrica | Objetivo | Crítico |
|---------|----------|---------|
| **Test Coverage** | > 80% | > 70% |
| **Linting Score** | 10/10 | > 8/10 |
| **Type Coverage** | 100% | > 90% |
| **Cyclomatic Complexity** | < 10 | < 15 |
| **Code Duplication** | < 3% | < 5% |

---

## 🔄 Proceso de Desarrollo

### Workflow Completo

```bash
# 1. Seleccionar tarea de TASK_LIST.md
# Marcar como [/] en progreso

# 2. Crear rama
git checkout -b feat/TASK-032-rsi-strategy

# 3. Desarrollar con TDD
# - Escribir test
# - Implementar código
# - Refactorizar

# 4. Validar calidad
black src/ tests/
isort src/ tests/
flake8 src/
mypy src/
pytest --cov=src

# 5. Commit
git add .
git commit -m "feat(strategies): implementar estrategia RSI"

# 6. Push y PR
git push origin feat/TASK-032-rsi-strategy
# Crear Pull Request

# 7. Code Review
# Esperar aprobación

# 8. Merge
# Squash and merge

# 9. Actualizar docs
# Marcar tarea como [x] en TASK_LIST.md
```

---

## ⚠️ Violaciones y Consecuencias

### Violaciones Críticas

❌ **Commitear credenciales** → Revertir inmediatamente, rotar keys  
❌ **Push a main sin PR** → Revertir, crear PR apropiado  
❌ **Merge sin tests** → Revertir hasta que tests pasen  
❌ **Código sin type hints** → Rechazar en code review  

### Violaciones Menores

⚠️ **Commit message incorrecto** → Corregir con `git commit --amend`  
⚠️ **Falta documentación** → Añadir antes de merge  
⚠️ **Coverage < 80%** → Añadir tests antes de merge  

---

## 📝 Resumen de Comandos

```bash
# Setup inicial
git clone <repo-url>
cd trading-bot
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
pre-commit install

# Desarrollo diario
git checkout develop
git pull origin develop
git checkout -b feat/TASK-XXX-descripcion
# ... desarrollar ...
black src/ tests/
isort src/ tests/
flake8 src/
mypy src/
pytest --cov=src
git add .
git commit -m "feat(scope): descripción"
git push origin feat/TASK-XXX-descripcion

# Antes de merge
git fetch origin
git rebase origin/develop
git push --force-with-lease
```

---

**Última actualización**: 2024-12-07  
**Versión**: 1.0.0  
**Aplicable desde**: Fase 1 (Core Infrastructure)

---

## 📚 Referencias

- [Conventional Commits](https://www.conventionalcommits.org/)
- [PEP 8](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
