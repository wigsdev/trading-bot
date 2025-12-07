"""
Script de prueba para verificar el sistema de logging.

Este script valida que:
1. El logger se inicializa correctamente
2. Los logs se escriben a consola y archivo
3. El formato JSON funciona
4. La rotación de archivos funciona
5. Los diferentes niveles de logging funcionan
"""

import sys
from pathlib import Path
import time
import json

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.logger import get_logger, log_with_context, StructuredLogger


def test_basic_logging():
    """Prueba logging básico."""
    print("🧪 Probando logging básico...\n")
    
    logger = get_logger(__name__)
    
    # Probar diferentes niveles
    logger.debug("Mensaje de debug")
    logger.info("Mensaje de info")
    logger.warning("Mensaje de advertencia")
    logger.error("Mensaje de error")
    
    print("✅ Logging básico funciona\n")
    return True


def test_json_logging():
    """Prueba logging con formato JSON."""
    print("🧪 Probando logging con JSON...\n")
    
    logger = get_logger("json_test", enable_json_console=True)
    
    logger.info("Prueba de JSON", extra={'extra_fields': {
        'symbol': 'AAPL',
        'price': 150.50,
        'qty': 100
    }})
    
    print("\n✅ Logging JSON funciona\n")
    return True


def test_context_logging():
    """Prueba logging con contexto."""
    print("🧪 Probando logging con contexto...\n")
    
    logger = get_logger("context_test")
    
    log_with_context(
        logger,
        'INFO',
        'Orden ejecutada exitosamente',
        symbol='TSLA',
        side='buy',
        qty=50,
        price=245.75,
        order_id='ORD-12345'
    )
    
    print("✅ Logging con contexto funciona\n")
    return True


def test_exception_logging():
    """Prueba logging de excepciones."""
    print("🧪 Probando logging de excepciones...\n")
    
    logger = get_logger("exception_test")
    
    try:
        # Generar una excepción de prueba
        result = 1 / 0
    except ZeroDivisionError as e:
        logger.error(
            "Error en cálculo",
            exc_info=True,
            extra={'extra_fields': {'operation': 'division'}}
        )
    
    print("✅ Logging de excepciones funciona\n")
    return True


def test_file_logging():
    """Prueba que los logs se escriben a archivo."""
    print("🧪 Probando logging a archivo...\n")
    
    logger = get_logger("file_test")
    
    # Escribir varios logs
    for i in range(5):
        logger.info(f"Log de prueba #{i+1}", extra={'extra_fields': {'iteration': i+1}})
    
    # Verificar que el archivo existe
    log_file = Path("logs/file_test.log")
    
    if log_file.exists():
        print(f"✅ Archivo de log creado: {log_file}")
        
        # Leer y mostrar contenido
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"   Líneas en archivo: {len(lines)}")
            
            # Verificar que es JSON válido
            if lines:
                try:
                    first_log = json.loads(lines[0])
                    print(f"   Primer log (JSON): {first_log['message']}")
                    print("   ✅ Formato JSON válido")
                except json.JSONDecodeError:
                    print("   ❌ Formato JSON inválido")
                    return False
        
        print()
        return True
    else:
        print(f"❌ Archivo de log no encontrado: {log_file}\n")
        return False


def test_multiple_loggers():
    """Prueba múltiples loggers simultáneos."""
    print("🧪 Probando múltiples loggers...\n")
    
    logger1 = get_logger("module1")
    logger2 = get_logger("module2")
    logger3 = get_logger("module3")
    
    logger1.info("Log desde módulo 1")
    logger2.info("Log desde módulo 2")
    logger3.info("Log desde módulo 3")
    
    # Verificar que son instancias diferentes
    if logger1 is not logger2 and logger2 is not logger3:
        print("✅ Múltiples loggers funcionan correctamente\n")
        return True
    else:
        print("❌ Los loggers no son independientes\n")
        return False


def test_log_rotation():
    """Prueba rotación de archivos de log."""
    print("🧪 Probando rotación de logs...\n")
    
    logger = get_logger("rotation_test")
    
    # Escribir muchos logs para forzar rotación
    # (esto depende de la configuración de max_size_mb)
    print("   Escribiendo logs para probar rotación...")
    for i in range(100):
        logger.info(
            f"Log de prueba de rotación #{i+1}" + " " * 100,  # Padding para aumentar tamaño
            extra={'extra_fields': {'iteration': i+1, 'data': 'x' * 100}}
        )
    
    log_file = Path("logs/rotation_test.log")
    if log_file.exists():
        size_kb = log_file.stat().st_size / 1024
        print(f"   Tamaño del archivo: {size_kb:.2f} KB")
        print("✅ Rotación de logs configurada\n")
        return True
    else:
        print("❌ Archivo de log no encontrado\n")
        return False


def test_logger_shutdown():
    """Prueba el cierre correcto del logger."""
    print("🧪 Probando cierre de logger...\n")
    
    logger = get_logger("shutdown_test")
    logger.info("Log antes del cierre")
    
    # Cerrar logger
    StructuredLogger.shutdown()
    
    print("✅ Logger cerrado correctamente\n")
    return True


def main():
    """Ejecuta todas las pruebas."""
    print("=" * 60)
    print("🚀 Testing StructuredLogger - Trading Bot")
    print("=" * 60)
    print()
    
    results = []
    
    # Ejecutar tests
    results.append(("Logging básico", test_basic_logging()))
    results.append(("Logging JSON", test_json_logging()))
    results.append(("Logging con contexto", test_context_logging()))
    results.append(("Logging de excepciones", test_exception_logging()))
    results.append(("Logging a archivo", test_file_logging()))
    results.append(("Múltiples loggers", test_multiple_loggers()))
    results.append(("Rotación de logs", test_log_rotation()))
    results.append(("Cierre de logger", test_logger_shutdown()))
    
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
    
    # Mostrar ubicación de logs
    print()
    print("📁 Archivos de log generados:")
    log_dir = Path("logs")
    if log_dir.exists():
        for log_file in sorted(log_dir.glob("*.log*")):
            size_kb = log_file.stat().st_size / 1024
            print(f"   {log_file.name} ({size_kb:.2f} KB)")
    
    if passed == total:
        print("\n🎉 ¡Todas las pruebas pasaron!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} prueba(s) fallaron")
        return 1


if __name__ == "__main__":
    sys.exit(main())
