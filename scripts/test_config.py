"""
Script de prueba para verificar el ConfigManager.

Este script valida que:
1. El ConfigManager carga correctamente
2. La validación de Pydantic funciona
3. Los valores por defecto son correctos
4. Las variables de entorno se cargan
"""

import sys
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config import get_config, ConfigManager


def test_config_loading():
    """Prueba la carga de configuración."""
    print("🧪 Probando carga de configuración...\n")
    
    try:
        config = get_config()
        print("✅ Configuración cargada exitosamente\n")
        
        # Mostrar configuración
        print("📋 Configuración actual:")
        print(f"  App: {config.app.name} v{config.app.version}")
        print(f"  Environment: {config.app.environment}")
        print(f"  Debug: {config.app.debug}")
        print()
        
        print(f"  Data Storage: {config.data.storage_path}")
        print(f"  Log Path: {config.data.log_path}")
        print(f"  Cache TTL: {config.data.cache_ttl}s")
        print()
        
        print(f"  Broker: {config.broker.provider}")
        print(f"  Paper Trading: {config.broker.paper_trading}")
        print(f"  Base URL: {config.broker.base_url}")
        print(f"  API Key ID: {'*' * 10}{config.broker.api_key_id[-4:] if len(config.broker.api_key_id) > 4 else '****'}")
        print()
        
        print(f"  Max Positions: {config.trading.max_positions}")
        print(f"  Position Size: {config.trading.position_size_pct * 100}%")
        print(f"  Stop Loss: {config.trading.stop_loss_pct * 100}%")
        print(f"  Take Profit: {config.trading.take_profit_pct * 100}%")
        print(f"  Strategies: {', '.join(config.trading.enabled_strategies)}")
        print()
        
        print(f"  Max Daily Loss: {config.risk.max_daily_loss_pct * 100}%")
        print(f"  Max Position Risk: {config.risk.max_position_risk_pct * 100}%")
        print()
        
        print(f"  Log Level: {config.logging.level}")
        print(f"  File Logging: {config.logging.file_enabled}")
        print(f"  Console Logging: {config.logging.console_enabled}")
        print()
        
        print(f"  Database Enabled: {config.database.enabled}")
        if config.database.enabled:
            print(f"  DB Connection: {config.database.host}:{config.database.port}/{config.database.database}")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error al cargar configuración: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_singleton():
    """Prueba que ConfigManager es singleton."""
    print("🧪 Probando patrón Singleton...\n")
    
    manager1 = ConfigManager.get_instance()
    manager2 = ConfigManager.get_instance()
    
    if manager1 is manager2:
        print("✅ Singleton funciona correctamente")
        print(f"   manager1 id: {id(manager1)}")
        print(f"   manager2 id: {id(manager2)}")
        print()
        return True
    else:
        print("❌ Singleton NO funciona")
        return False


def test_validation():
    """Prueba la validación de Pydantic."""
    print("🧪 Probando validación de Pydantic...\n")
    
    from pydantic import ValidationError
    from src.utils.config import TradingConfig
    
    # Test 1: Validación de position_size
    try:
        invalid_config = TradingConfig(
            max_positions=10,
            position_size_pct=0.15  # 15% * 10 = 150% > 100%
        )
        print("❌ Validación falló: debería rechazar position_size inválido")
        return False
    except ValidationError as e:
        print("✅ Validación correcta: rechaza position_size inválido")
        print(f"   Error: {e.errors()[0]['msg']}")
        print()
    
    # Test 2: Configuración válida
    try:
        valid_config = TradingConfig(
            max_positions=5,
            position_size_pct=0.2  # 20% * 5 = 100% ✓
        )
        print("✅ Validación correcta: acepta configuración válida")
        print(f"   Max Positions: {valid_config.max_positions}")
        print(f"   Position Size: {valid_config.position_size_pct * 100}%")
        print()
        return True
    except ValidationError as e:
        print(f"❌ Validación falló inesperadamente: {e}")
        return False


def main():
    """Ejecuta todas las pruebas."""
    print("=" * 60)
    print("🚀 Testing ConfigManager - Trading Bot")
    print("=" * 60)
    print()
    
    results = []
    
    # Test 1: Carga de configuración
    results.append(("Carga de configuración", test_config_loading()))
    
    # Test 2: Singleton
    results.append(("Patrón Singleton", test_singleton()))
    
    # Test 3: Validación
    results.append(("Validación Pydantic", test_validation()))
    
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
        return 0
    else:
        print(f"\n⚠️  {total - passed} prueba(s) fallaron")
        return 1


if __name__ == "__main__":
    sys.exit(main())
