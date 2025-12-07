"""
Módulo de validadores para el Trading Bot.

Este módulo proporciona validadores reutilizables para:
- Símbolos de acciones
- Parámetros de órdenes
- Fechas y timeframes
- Porcentajes y rangos
- Configuración y URLs

Example:
    >>> from src.utils.validators import validate_symbol, validate_quantity
    >>> symbol = validate_symbol("aapl")  # Returns "AAPL"
    >>> qty = validate_quantity(100)  # Returns 100
"""

import re
from typing import List, Tuple, Optional
from datetime import datetime, date
from urllib.parse import urlparse


class ValidationError(Exception):
    """Excepción base para errores de validación."""
    pass


class SymbolValidationError(ValidationError):
    """Error de validación de símbolo."""
    pass


class OrderValidationError(ValidationError):
    """Error de validación de orden."""
    pass


class DateValidationError(ValidationError):
    """Error de validación de fecha."""
    pass


class PercentageValidationError(ValidationError):
    """Error de validación de porcentaje."""
    pass


class ConfigValidationError(ValidationError):
    """Error de validación de configuración."""
    pass


# ============================================================================
# Validadores de Símbolos
# ============================================================================

def validate_symbol(symbol: str) -> str:
    """
    Valida un símbolo de acción.
    
    Args:
        symbol: Símbolo a validar
        
    Returns:
        Símbolo validado en mayúsculas
        
    Raises:
        SymbolValidationError: Si el símbolo es inválido
        
    Example:
        >>> validate_symbol("aapl")
        'AAPL'
        >>> validate_symbol("TSLA")
        'TSLA'
    """
    if not symbol:
        raise SymbolValidationError("El símbolo no puede estar vacío")
    
    # Convertir a mayúsculas y eliminar espacios
    symbol = symbol.strip().upper()
    
    # Validar formato: solo letras, 1-5 caracteres
    if not re.match(r'^[A-Z]{1,5}$', symbol):
        raise SymbolValidationError(
            f"Símbolo inválido: '{symbol}'. Debe contener solo letras (1-5 caracteres)"
        )
    
    return symbol


def validate_symbols_list(symbols: List[str]) -> List[str]:
    """
    Valida una lista de símbolos.
    
    Args:
        symbols: Lista de símbolos a validar
        
    Returns:
        Lista de símbolos validados (sin duplicados)
        
    Raises:
        SymbolValidationError: Si algún símbolo es inválido
        
    Example:
        >>> validate_symbols_list(["aapl", "TSLA", "aapl"])
        ['AAPL', 'TSLA']
    """
    if not symbols:
        raise SymbolValidationError("La lista de símbolos no puede estar vacía")
    
    validated = []
    seen = set()
    
    for symbol in symbols:
        validated_symbol = validate_symbol(symbol)
        
        # Evitar duplicados
        if validated_symbol not in seen:
            validated.append(validated_symbol)
            seen.add(validated_symbol)
    
    return validated


# ============================================================================
# Validadores de Órdenes
# ============================================================================

def validate_order_side(side: str) -> str:
    """
    Valida el lado de una orden (buy/sell).
    
    Args:
        side: Lado de la orden
        
    Returns:
        Lado validado en minúsculas
        
    Raises:
        OrderValidationError: Si el lado es inválido
        
    Example:
        >>> validate_order_side("BUY")
        'buy'
        >>> validate_order_side("sell")
        'sell'
    """
    if not side:
        raise OrderValidationError("El lado de la orden no puede estar vacío")
    
    side = side.strip().lower()
    
    if side not in ['buy', 'sell']:
        raise OrderValidationError(
            f"Lado de orden inválido: '{side}'. Debe ser 'buy' o 'sell'"
        )
    
    return side


def validate_quantity(qty: int, min_qty: int = 1) -> int:
    """
    Valida la cantidad de una orden.
    
    Args:
        qty: Cantidad a validar
        min_qty: Cantidad mínima permitida
        
    Returns:
        Cantidad validada
        
    Raises:
        OrderValidationError: Si la cantidad es inválida
        
    Example:
        >>> validate_quantity(100)
        100
        >>> validate_quantity(0)  # Raises error
    """
    if not isinstance(qty, int):
        raise OrderValidationError(
            f"La cantidad debe ser un entero, recibido: {type(qty).__name__}"
        )
    
    if qty < min_qty:
        raise OrderValidationError(
            f"La cantidad debe ser >= {min_qty}, recibido: {qty}"
        )
    
    return qty


def validate_price(price: float, min_price: float = 0.01) -> float:
    """
    Valida el precio de una orden.
    
    Args:
        price: Precio a validar
        min_price: Precio mínimo permitido
        
    Returns:
        Precio validado redondeado a 2 decimales
        
    Raises:
        OrderValidationError: Si el precio es inválido
        
    Example:
        >>> validate_price(150.50)
        150.5
        >>> validate_price(0.0)  # Raises error
    """
    if not isinstance(price, (int, float)):
        raise OrderValidationError(
            f"El precio debe ser numérico, recibido: {type(price).__name__}"
        )
    
    if price < min_price:
        raise OrderValidationError(
            f"El precio debe ser >= {min_price}, recibido: {price}"
        )
    
    # Redondear a 2 decimales
    return round(float(price), 2)


def validate_order_type(order_type: str) -> str:
    """
    Valida el tipo de orden.
    
    Args:
        order_type: Tipo de orden
        
    Returns:
        Tipo de orden validado en minúsculas
        
    Raises:
        OrderValidationError: Si el tipo es inválido
        
    Example:
        >>> validate_order_type("MARKET")
        'market'
        >>> validate_order_type("limit")
        'limit'
    """
    if not order_type:
        raise OrderValidationError("El tipo de orden no puede estar vacío")
    
    order_type = order_type.strip().lower()
    
    valid_types = ['market', 'limit', 'stop', 'stop_limit']
    
    if order_type not in valid_types:
        raise OrderValidationError(
            f"Tipo de orden inválido: '{order_type}'. "
            f"Debe ser uno de: {', '.join(valid_types)}"
        )
    
    return order_type


# ============================================================================
# Validadores de Fechas y Tiempo
# ============================================================================

def validate_date(date_str: str, date_format: str = "%Y-%m-%d") -> datetime:
    """
    Valida y convierte una fecha en string a datetime.
    
    Args:
        date_str: Fecha en formato string
        date_format: Formato esperado de la fecha
        
    Returns:
        Objeto datetime
        
    Raises:
        DateValidationError: Si la fecha es inválida
        
    Example:
        >>> validate_date("2024-12-07")
        datetime.datetime(2024, 12, 7, 0, 0)
    """
    if not date_str:
        raise DateValidationError("La fecha no puede estar vacía")
    
    try:
        return datetime.strptime(date_str, date_format)
    except ValueError as e:
        raise DateValidationError(
            f"Formato de fecha inválido: '{date_str}'. "
            f"Esperado: {date_format}. Error: {e}"
        )


def validate_date_range(
    start_date: str,
    end_date: str,
    date_format: str = "%Y-%m-%d"
) -> Tuple[datetime, datetime]:
    """
    Valida un rango de fechas.
    
    Args:
        start_date: Fecha de inicio
        end_date: Fecha de fin
        date_format: Formato de las fechas
        
    Returns:
        Tupla (fecha_inicio, fecha_fin)
        
    Raises:
        DateValidationError: Si el rango es inválido
        
    Example:
        >>> start, end = validate_date_range("2024-01-01", "2024-12-31")
    """
    start = validate_date(start_date, date_format)
    end = validate_date(end_date, date_format)
    
    if start > end:
        raise DateValidationError(
            f"La fecha de inicio ({start_date}) debe ser anterior "
            f"a la fecha de fin ({end_date})"
        )
    
    return start, end


def validate_timeframe(timeframe: str) -> str:
    """
    Valida un timeframe para datos de mercado.
    
    Args:
        timeframe: Timeframe a validar
        
    Returns:
        Timeframe validado
        
    Raises:
        DateValidationError: Si el timeframe es inválido
        
    Example:
        >>> validate_timeframe("1Min")
        '1Min'
        >>> validate_timeframe("1Day")
        '1Day'
    """
    if not timeframe:
        raise DateValidationError("El timeframe no puede estar vacío")
    
    valid_timeframes = [
        '1Min', '5Min', '15Min', '30Min',
        '1Hour', '4Hour',
        '1Day', '1Week', '1Month'
    ]
    
    if timeframe not in valid_timeframes:
        raise DateValidationError(
            f"Timeframe inválido: '{timeframe}'. "
            f"Debe ser uno de: {', '.join(valid_timeframes)}"
        )
    
    return timeframe


# ============================================================================
# Validadores de Porcentajes y Rangos
# ============================================================================

def validate_percentage(
    value: float,
    min_value: float = 0.0,
    max_value: float = 1.0,
    name: str = "porcentaje"
) -> float:
    """
    Valida un porcentaje dentro de un rango.
    
    Args:
        value: Valor a validar (0.0 - 1.0)
        min_value: Valor mínimo permitido
        max_value: Valor máximo permitido
        name: Nombre del campo para mensajes de error
        
    Returns:
        Valor validado
        
    Raises:
        PercentageValidationError: Si el valor está fuera de rango
        
    Example:
        >>> validate_percentage(0.05, name="stop_loss")
        0.05
        >>> validate_percentage(1.5)  # Raises error
    """
    if not isinstance(value, (int, float)):
        raise PercentageValidationError(
            f"{name} debe ser numérico, recibido: {type(value).__name__}"
        )
    
    if value < min_value or value > max_value:
        raise PercentageValidationError(
            f"{name} debe estar entre {min_value*100}% y {max_value*100}%, "
            f"recibido: {value*100}%"
        )
    
    return float(value)


def validate_range(
    value: float,
    min_value: float,
    max_value: float,
    name: str = "valor"
) -> float:
    """
    Valida que un valor esté dentro de un rango.
    
    Args:
        value: Valor a validar
        min_value: Valor mínimo
        max_value: Valor máximo
        name: Nombre del campo
        
    Returns:
        Valor validado
        
    Raises:
        ValidationError: Si el valor está fuera de rango
        
    Example:
        >>> validate_range(50, 0, 100, "temperatura")
        50.0
    """
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"{name} debe ser numérico, recibido: {type(value).__name__}"
        )
    
    if value < min_value or value > max_value:
        raise ValidationError(
            f"{name} debe estar entre {min_value} y {max_value}, "
            f"recibido: {value}"
        )
    
    return float(value)


# ============================================================================
# Validadores de Configuración
# ============================================================================

def validate_api_key(api_key: str, min_length: int = 10) -> str:
    """
    Valida una API key.
    
    Args:
        api_key: API key a validar
        min_length: Longitud mínima requerida
        
    Returns:
        API key validada
        
    Raises:
        ConfigValidationError: Si la API key es inválida
        
    Example:
        >>> validate_api_key("PK1234567890ABCDEF")
        'PK1234567890ABCDEF'
    """
    if not api_key:
        raise ConfigValidationError("La API key no puede estar vacía")
    
    api_key = api_key.strip()
    
    if len(api_key) < min_length:
        raise ConfigValidationError(
            f"La API key debe tener al menos {min_length} caracteres, "
            f"recibido: {len(api_key)}"
        )
    
    # Verificar que no sea un placeholder
    if api_key.startswith('tu_') or api_key.startswith('your_'):
        raise ConfigValidationError(
            "La API key parece ser un placeholder. "
            "Por favor configura tu API key real."
        )
    
    return api_key


def validate_url(url: str, require_https: bool = True) -> str:
    """
    Valida una URL.
    
    Args:
        url: URL a validar
        require_https: Si True, requiere protocolo HTTPS
        
    Returns:
        URL validada
        
    Raises:
        ConfigValidationError: Si la URL es inválida
        
    Example:
        >>> validate_url("https://api.alpaca.markets")
        'https://api.alpaca.markets'
    """
    if not url:
        raise ConfigValidationError("La URL no puede estar vacía")
    
    url = url.strip()
    
    try:
        parsed = urlparse(url)
        
        if not parsed.scheme:
            raise ConfigValidationError(f"URL sin protocolo: {url}")
        
        if not parsed.netloc:
            raise ConfigValidationError(f"URL sin dominio: {url}")
        
        if require_https and parsed.scheme != 'https':
            raise ConfigValidationError(
                f"La URL debe usar HTTPS, recibido: {parsed.scheme}"
            )
        
        return url
        
    except Exception as e:
        raise ConfigValidationError(f"URL inválida: {url}. Error: {e}")


def validate_positive_integer(value: int, name: str = "valor") -> int:
    """
    Valida que un valor sea un entero positivo.
    
    Args:
        value: Valor a validar
        name: Nombre del campo
        
    Returns:
        Valor validado
        
    Raises:
        ValidationError: Si el valor no es un entero positivo
        
    Example:
        >>> validate_positive_integer(5, "max_positions")
        5
    """
    if not isinstance(value, int):
        raise ValidationError(
            f"{name} debe ser un entero, recibido: {type(value).__name__}"
        )
    
    if value <= 0:
        raise ValidationError(
            f"{name} debe ser positivo, recibido: {value}"
        )
    
    return value


# Exportar para uso externo
__all__ = [
    # Excepciones
    'ValidationError',
    'SymbolValidationError',
    'OrderValidationError',
    'DateValidationError',
    'PercentageValidationError',
    'ConfigValidationError',
    # Validadores de símbolos
    'validate_symbol',
    'validate_symbols_list',
    # Validadores de órdenes
    'validate_order_side',
    'validate_quantity',
    'validate_price',
    'validate_order_type',
    # Validadores de fechas
    'validate_date',
    'validate_date_range',
    'validate_timeframe',
    # Validadores de porcentajes
    'validate_percentage',
    'validate_range',
    # Validadores de configuración
    'validate_api_key',
    'validate_url',
    'validate_positive_integer',
]
