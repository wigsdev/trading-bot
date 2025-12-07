"""
Sistema de logging estructurado para el Trading Bot.

Este módulo proporciona un logger configurable que:
- Soporta múltiples niveles de logging
- Formatea logs en JSON para fácil parsing
- Rota archivos automáticamente
- Integra con ConfigManager
- Soporta logging a consola y archivo simultáneamente

Example:
    >>> from src.utils.logger import get_logger
    >>> logger = get_logger(__name__)
    >>> logger.info("Bot iniciado", extra={"version": "0.1.0"})
"""

import logging
import logging.handlers
import sys
import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from .config import get_config


class JsonFormatter(logging.Formatter):
    """
    Formateador de logs en JSON.
    
    Convierte los registros de log a formato JSON estructurado
    para facilitar el parsing y análisis.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Formatea un registro de log como JSON.
        
        Args:
            record: Registro de log a formatear
            
        Returns:
            String JSON con el log formateado
        """
        log_data: Dict[str, Any] = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Añadir información de excepción si existe
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Añadir campos extra si existen
        if hasattr(record, 'extra_fields'):
            log_data.update(record.extra_fields)
        
        return json.dumps(log_data, ensure_ascii=False)


class StructuredLogger:
    """
    Logger estructurado con soporte para JSON y rotación de archivos.
    
    Proporciona un logger configurado con:
    - Formato JSON para archivos
    - Formato legible para consola
    - Rotación automática de archivos
    - Múltiples niveles de logging
    
    Example:
        >>> logger = StructuredLogger.get_logger("trading_bot")
        >>> logger.info("Operación completada", extra={"symbol": "AAPL"})
    """
    
    _loggers: Dict[str, logging.Logger] = {}
    _initialized: bool = False
    
    @classmethod
    def initialize(cls) -> None:
        """
        Inicializa el sistema de logging con la configuración.
        
        Debe llamarse una vez al inicio de la aplicación.
        """
        if cls._initialized:
            return
        
        config = get_config()
        log_config = config.logging
        
        # Crear directorio de logs si no existe
        log_path = config.data.log_path
        log_path.mkdir(parents=True, exist_ok=True)
        
        # Configurar nivel de logging raíz
        logging.root.setLevel(getattr(logging, log_config.level))
        
        cls._initialized = True
    
    @classmethod
    def get_logger(
        cls,
        name: str,
        enable_json: bool = False
    ) -> logging.Logger:
        """
        Obtiene o crea un logger con la configuración especificada.
        
        Args:
            name: Nombre del logger (generalmente __name__)
            enable_json: Si True, usa formato JSON en consola también
            
        Returns:
            Logger configurado
            
        Example:
            >>> logger = StructuredLogger.get_logger(__name__)
            >>> logger.info("Mensaje de prueba")
        """
        # Inicializar si es necesario
        if not cls._initialized:
            cls.initialize()
        
        # Retornar logger existente si ya fue creado
        if name in cls._loggers:
            return cls._loggers[name]
        
        # Crear nuevo logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)  # Capturar todo, filtrar en handlers
        
        # Evitar propagación para no duplicar logs
        logger.propagate = False
        
        # Limpiar handlers existentes
        logger.handlers.clear()
        
        # Obtener configuración
        config = get_config()
        log_config = config.logging
        
        # Handler de consola
        if log_config.console_enabled:
            console_handler = cls._create_console_handler(
                log_config.level,
                enable_json
            )
            logger.addHandler(console_handler)
        
        # Handler de archivo
        if log_config.file_enabled:
            file_handler = cls._create_file_handler(
                name,
                log_config.level,
                config.data.log_path,
                log_config.rotation_size_mb,
                log_config.backup_count
            )
            logger.addHandler(file_handler)
        
        # Guardar logger
        cls._loggers[name] = logger
        
        return logger
    
    @classmethod
    def _create_console_handler(
        cls,
        level: str,
        use_json: bool = False
    ) -> logging.Handler:
        """
        Crea handler para logging a consola.
        
        Args:
            level: Nivel de logging
            use_json: Si True, usa formato JSON
            
        Returns:
            Handler configurado para consola
        """
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, level))
        
        if use_json:
            formatter = JsonFormatter()
        else:
            # Formato legible para consola
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        
        handler.setFormatter(formatter)
        return handler
    
    @classmethod
    def _create_file_handler(
        cls,
        logger_name: str,
        level: str,
        log_path: Path,
        max_size_mb: int,
        backup_count: int
    ) -> logging.Handler:
        """
        Crea handler para logging a archivo con rotación.
        
        Args:
            logger_name: Nombre del logger
            level: Nivel de logging
            log_path: Ruta donde guardar logs
            max_size_mb: Tamaño máximo en MB antes de rotar
            backup_count: Número de archivos de backup a mantener
            
        Returns:
            Handler configurado para archivo
        """
        # Nombre de archivo basado en el logger
        log_file = log_path / f"{logger_name.replace('.', '_')}.log"
        
        # Handler con rotación por tamaño
        handler = logging.handlers.RotatingFileHandler(
            filename=log_file,
            maxBytes=max_size_mb * 1024 * 1024,  # Convertir MB a bytes
            backupCount=backup_count,
            encoding='utf-8'
        )
        
        handler.setLevel(getattr(logging, level))
        
        # Usar JSON para archivos
        formatter = JsonFormatter()
        handler.setFormatter(formatter)
        
        return handler
    
    @classmethod
    def shutdown(cls) -> None:
        """
        Cierra todos los handlers y limpia recursos.
        
        Debe llamarse al finalizar la aplicación.
        """
        for logger in cls._loggers.values():
            for handler in logger.handlers[:]:
                handler.close()
                logger.removeHandler(handler)
        
        cls._loggers.clear()
        cls._initialized = False


def get_logger(
    name: str,
    enable_json_console: bool = False
) -> logging.Logger:
    """
    Función helper para obtener un logger.
    
    Args:
        name: Nombre del logger (usar __name__)
        enable_json_console: Si True, usa JSON en consola
        
    Returns:
        Logger configurado
        
    Example:
        >>> from src.utils.logger import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Bot iniciado")
        >>> logger.error("Error crítico", exc_info=True)
    """
    return StructuredLogger.get_logger(name, enable_json_console)


def log_with_context(
    logger: logging.Logger,
    level: str,
    message: str,
    **context: Any
) -> None:
    """
    Registra un mensaje con contexto adicional.
    
    Args:
        logger: Logger a usar
        level: Nivel de logging (INFO, ERROR, etc.)
        message: Mensaje a registrar
        **context: Campos adicionales para el log
        
    Example:
        >>> logger = get_logger(__name__)
        >>> log_with_context(
        ...     logger, 'INFO', 'Orden ejecutada',
        ...     symbol='AAPL', qty=10, price=150.50
        ... )
    """
    log_method = getattr(logger, level.lower())
    
    # Crear un LogRecord con campos extra
    extra = {'extra_fields': context}
    log_method(message, extra=extra)


# Exportar para uso externo
__all__ = [
    'StructuredLogger',
    'JsonFormatter',
    'get_logger',
    'log_with_context',
]
