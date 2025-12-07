"""
Script de prueba para verificar el módulo de validadores.

Este script valida que:
1. Los validadores de símbolos funcionan
2. Los validadores de órdenes funcionan
3. Los validadores de fechas funcionan
4. Los validadores de porcentajes funcionan
5. Los validadores de configuración funcionan
6. Las excepciones se lanzan correctamente
"""

import sys
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.validators import (
    # Excepciones
    ValidationError,
    SymbolValidationError,
    OrderValidationError,
    DateValidationError,
    PercentageValidationError,
    ConfigValidationError,
    # Validadores
    validate_symbol,
    validate_symbols_list,
    validate_order_side,
    validate_quantity,
    validate_price,
    validate_order_type,
    validate_date,
    validate_date_range,
    validate_timeframe,
    validate_percentage,
    validate_range,
    validate_api_key,
    validate_url,
    validate_positive_integer,
)


def test_symbol_validators():
    """Prueba validadores de símbolos."""
    print("🧪 Probando validadores de símbolos...\n")
    
    # Test 1: Símbolo válido
    try:
        result = validate_symbol("aapl")
        assert result == "AAPL", f"Esperado 'AAPL', recibido '{result}'"
        print("  ✅ validate_symbol('aapl') = 'AAPL'")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 2: Símbolo inválido
    try:
        validate_symbol("AAPL123")
        print("  ❌ Debería rechazar símbolos con números")
        return False
    except SymbolValidationError:
        print("  ✅ Rechaza símbolos inválidos correctamente")
    
    # Test 3: Lista de símbolos
    try:
        result = validate_symbols_list(["aapl", "TSLA", "aapl", "msft"])
        assert result == ["AAPL", "TSLA", "MSFT"], f"Resultado inesperado: {result}"
        print("  ✅ validate_symbols_list elimina duplicados")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    print("✅ Validadores de símbolos funcionan\n")
    return True


def test_order_validators():
    """Prueba validadores de órdenes."""
    print("🧪 Probando validadores de órdenes...\n")
    
    # Test 1: Lado de orden
    try:
        result = validate_order_side("BUY")
        assert result == "buy", f"Esperado 'buy', recibido '{result}'"
        print("  ✅ validate_order_side('BUY') = 'buy'")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 2: Cantidad
    try:
        result = validate_quantity(100)
        assert result == 100, f"Esperado 100, recibido {result}"
        print("  ✅ validate_quantity(100) = 100")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 3: Cantidad inválida
    try:
        validate_quantity(0)
        print("  ❌ Debería rechazar cantidad 0")
        return False
    except OrderValidationError:
        print("  ✅ Rechaza cantidad inválida")
    
    # Test 4: Precio
    try:
        result = validate_price(150.50)
        assert result == 150.50, f"Esperado 150.50, recibido {result}"
        print("  ✅ validate_price(150.50) = 150.50")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 5: Tipo de orden
    try:
        result = validate_order_type("MARKET")
        assert result == "market", f"Esperado 'market', recibido '{result}'"
        print("  ✅ validate_order_type('MARKET') = 'market'")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    print("✅ Validadores de órdenes funcionan\n")
    return True


def test_date_validators():
    """Prueba validadores de fechas."""
    print("🧪 Probando validadores de fechas...\n")
    
    # Test 1: Fecha válida
    try:
        result = validate_date("2024-12-07")
        print(f"  ✅ validate_date('2024-12-07') = {result}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 2: Fecha inválida
    try:
        validate_date("2024-13-01")  # Mes inválido
        print("  ❌ Debería rechazar fecha inválida")
        return False
    except DateValidationError:
        print("  ✅ Rechaza fecha inválida")
    
    # Test 3: Rango de fechas
    try:
        start, end = validate_date_range("2024-01-01", "2024-12-31")
        print(f"  ✅ validate_date_range funciona")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 4: Rango inválido
    try:
        validate_date_range("2024-12-31", "2024-01-01")  # Invertido
        print("  ❌ Debería rechazar rango invertido")
        return False
    except DateValidationError:
        print("  ✅ Rechaza rango de fechas inválido")
    
    # Test 5: Timeframe
    try:
        result = validate_timeframe("1Min")
        assert result == "1Min", f"Esperado '1Min', recibido '{result}'"
        print("  ✅ validate_timeframe('1Min') = '1Min'")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    print("✅ Validadores de fechas funcionan\n")
    return True


def test_percentage_validators():
    """Prueba validadores de porcentajes."""
    print("🧪 Probando validadores de porcentajes...\n")
    
    # Test 1: Porcentaje válido
    try:
        result = validate_percentage(0.05, name="stop_loss")
        assert result == 0.05, f"Esperado 0.05, recibido {result}"
        print("  ✅ validate_percentage(0.05) = 0.05")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 2: Porcentaje fuera de rango
    try:
        validate_percentage(1.5)  # > 100%
        print("  ❌ Debería rechazar porcentaje > 100%")
        return False
    except PercentageValidationError:
        print("  ✅ Rechaza porcentaje fuera de rango")
    
    # Test 3: Rango genérico
    try:
        result = validate_range(50, 0, 100, "temperatura")
        assert result == 50.0, f"Esperado 50.0, recibido {result}"
        print("  ✅ validate_range(50, 0, 100) = 50.0")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    print("✅ Validadores de porcentajes funcionan\n")
    return True


def test_config_validators():
    """Prueba validadores de configuración."""
    print("🧪 Probando validadores de configuración...\n")
    
    # Test 1: API key válida
    try:
        result = validate_api_key("PK1234567890ABCDEF")
        assert result == "PK1234567890ABCDEF"
        print("  ✅ validate_api_key acepta key válida")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 2: API key placeholder
    try:
        validate_api_key("tu_api_key")
        print("  ❌ Debería rechazar placeholder")
        return False
    except ConfigValidationError:
        print("  ✅ Rechaza API key placeholder")
    
    # Test 3: URL válida
    try:
        result = validate_url("https://api.alpaca.markets")
        assert result == "https://api.alpaca.markets"
        print("  ✅ validate_url acepta URL válida")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 4: URL sin HTTPS
    try:
        validate_url("http://api.example.com")
        print("  ❌ Debería rechazar HTTP")
        return False
    except ConfigValidationError:
        print("  ✅ Rechaza URL sin HTTPS")
    
    # Test 5: Entero positivo
    try:
        result = validate_positive_integer(5, "max_positions")
        assert result == 5
        print("  ✅ validate_positive_integer(5) = 5")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 6: Entero negativo
    try:
        validate_positive_integer(-1)
        print("  ❌ Debería rechazar entero negativo")
        return False
    except ValidationError:
        print("  ✅ Rechaza entero negativo")
    
    print("✅ Validadores de configuración funcionan\n")
    return True


def test_exception_hierarchy():
    """Prueba la jerarquía de excepciones."""
    print("🧪 Probando jerarquía de excepciones...\n")
    
    # Todas las excepciones deben heredar de ValidationError
    exceptions = [
        SymbolValidationError,
        OrderValidationError,
        DateValidationError,
        PercentageValidationError,
        ConfigValidationError,
    ]
    
    for exc_class in exceptions:
        if not issubclass(exc_class, ValidationError):
            print(f"  ❌ {exc_class.__name__} no hereda de ValidationError")
            return False
    
    print("  ✅ Todas las excepciones heredan de ValidationError")
    print("✅ Jerarquía de excepciones correcta\n")
    return True


def main():
    """Ejecuta todas las pruebas."""
    print("=" * 60)
    print("🚀 Testing Validators - Trading Bot")
    print("=" * 60)
    print()
    
    results = []
    
    # Ejecutar tests
    results.append(("Validadores de símbolos", test_symbol_validators()))
    results.append(("Validadores de órdenes", test_order_validators()))
    results.append(("Validadores de fechas", test_date_validators()))
    results.append(("Validadores de porcentajes", test_percentage_validators()))
    results.append(("Validadores de configuración", test_config_validators()))
    results.append(("Jerarquía de excepciones", test_exception_hierarchy()))
    
    # Resumen
    print("=" * 60)
    print("📊 Resumen de Pruebas")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print()
    print(f"Resultado: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("\n🎉 ¡Todas las pruebas pasaron!")
        print("\n📦 Validadores implementados:")
        print("  • 6 excepciones personalizadas")
        print("  • 3 validadores de símbolos")
        print("  • 4 validadores de órdenes")
        print("  • 3 validadores de fechas")
        print("  • 2 validadores de porcentajes")
        print("  • 3 validadores de configuración")
        print("  = 18 validadores totales")
        return 0
    else:
        print(f"\n⚠️  {total - passed} prueba(s) fallaron")
        return 1


if __name__ == "__main__":
    sys.exit(main())
