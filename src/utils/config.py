"""
Sistema de configuración del Trading Bot con validación Pydantic.

Este módulo proporciona un sistema robusto de configuración que:
- Valida automáticamente tipos y valores
- Carga desde múltiples fuentes (.env, YAML, variables de entorno)
- Implementa Singleton pattern para acceso global
- Proporciona type hints completos

Example:
    >>> from src.utils.config import get_config
    >>> config = get_config()
    >>> print(config.app.name)
    'Trading Bot Híbrido'
"""

import os
from pathlib import Path
from typing import Optional, List
from enum import Enum

import yaml
from pydantic import BaseModel, Field, validator, ValidationError
from dotenv import load_dotenv


class Environment(str, Enum):
    """Entornos de ejecución disponibles."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class AppConfig(BaseModel):
    """Configuración general de la aplicación."""
    
    name: str = Field(default="Trading Bot Híbrido", description="Nombre de la aplicación")
    version: str = Field(default="0.1.0", description="Versión de la aplicación")
    environment: Environment = Field(default=Environment.DEVELOPMENT, description="Entorno de ejecución")
    debug: bool = Field(default=False, description="Modo debug")
    
    class Config:
        use_enum_values = True


class DataConfig(BaseModel):
    """Configuración de almacenamiento de datos."""
    
    storage_path: Path = Field(default=Path("data/"), description="Ruta de almacenamiento")
    log_path: Path = Field(default=Path("logs/"), description="Ruta de logs")
    cache_ttl: int = Field(default=300, ge=0, description="TTL del cache en segundos")
    
    @validator('storage_path', 'log_path')
    def create_directories(cls, v: Path) -> Path:
        """Crea directorios si no existen."""
        v.mkdir(parents=True, exist_ok=True)
        return v


class BrokerConfig(BaseModel):
    """Configuración del broker (Alpaca)."""
    
    provider: str = Field(default="alpaca", description="Proveedor del broker")
    paper_trading: bool = Field(default=True, description="Usar paper trading")
    api_key_id: str = Field(..., description="API Key ID", env="ALPACA_API_KEY_ID")
    api_secret_key: str = Field(..., description="API Secret Key", env="ALPACA_API_SECRET_KEY")
    base_url: str = Field(
        default="https://paper-api.alpaca.markets",
        description="URL base de la API",
        env="ALPACA_BASE_URL"
    )
    
    @validator('api_key_id', 'api_secret_key')
    def validate_not_empty(cls, v: str) -> str:
        """Valida que las API keys no estén vacías."""
        if not v or v.startswith('tu_'):
            raise ValueError("API key no configurada. Revisa tu archivo .env")
        return v
    
    @validator('base_url')
    def validate_url(cls, v: str) -> str:
        """Valida que la URL use HTTPS."""
        if not v.startswith('https://'):
            raise ValueError("La URL debe usar HTTPS")
        return v


class TradingConfig(BaseModel):
    """Configuración de trading."""
    
    max_positions: int = Field(default=5, ge=1, le=20, description="Máximo de posiciones concurrentes")
    position_size_pct: float = Field(
        default=0.2,
        gt=0,
        le=1,
        description="Tamaño de posición como % del capital"
    )
    stop_loss_pct: float = Field(default=0.02, gt=0, lt=1, description="Stop loss %")
    take_profit_pct: float = Field(default=0.05, gt=0, description="Take profit %")
    enabled_strategies: List[str] = Field(
        default=["rsi", "ma_crossover"],
        description="Estrategias habilitadas"
    )
    
    @validator('position_size_pct')
    def validate_position_size(cls, v: float, values: dict) -> float:
        """Valida que position_size * max_positions <= 100%."""
        max_positions = values.get('max_positions', 5)
        if v * max_positions > 1.0:
            raise ValueError(
                f"position_size_pct ({v}) * max_positions ({max_positions}) > 100%"
            )
        return v


class RiskConfig(BaseModel):
    """Configuración de gestión de riesgo."""
    
    max_daily_loss_pct: float = Field(
        default=0.05,
        gt=0,
        le=0.2,
        description="Máxima pérdida diaria %"
    )
    max_position_risk_pct: float = Field(
        default=0.02,
        gt=0,
        le=0.1,
        description="Máximo riesgo por posición %"
    )
    max_portfolio_risk_pct: float = Field(
        default=0.1,
        gt=0,
        le=0.3,
        description="Máximo riesgo del portfolio %"
    )


class LoggingConfig(BaseModel):
    """Configuración de logging."""
    
    level: str = Field(default="INFO", description="Nivel de logging")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Formato de logs"
    )
    file_enabled: bool = Field(default=True, description="Habilitar logs a archivo")
    console_enabled: bool = Field(default=True, description="Habilitar logs a consola")
    rotation_size_mb: int = Field(default=10, ge=1, description="Tamaño de rotación en MB")
    backup_count: int = Field(default=5, ge=1, description="Número de backups")
    
    @validator('level')
    def validate_level(cls, v: str) -> str:
        """Valida que el nivel de logging sea válido."""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"Nivel debe ser uno de: {valid_levels}")
        return v_upper


class DatabaseConfig(BaseModel):
    """Configuración de base de datos."""
    
    enabled: bool = Field(default=False, description="Habilitar base de datos")
    host: str = Field(default="localhost", env="DB_HOST")
    port: int = Field(default=5432, ge=1, le=65535, env="DB_PORT")
    user: str = Field(default="user", env="DB_USER")
    password: str = Field(default="password", env="DB_PASS")
    database: str = Field(default="trading_bot", env="DB_NAME")
    
    @property
    def connection_string(self) -> str:
        """Genera string de conexión PostgreSQL."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class TradingBotConfig(BaseModel):
    """Configuración principal del Trading Bot."""
    
    app: AppConfig = Field(default_factory=AppConfig)
    data: DataConfig = Field(default_factory=DataConfig)
    broker: BrokerConfig
    trading: TradingConfig = Field(default_factory=TradingConfig)
    risk: RiskConfig = Field(default_factory=RiskConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    
    class Config:
        env_prefix = 'TRADING_'
        case_sensitive = False


class ConfigManager:
    """
    Gestor de configuración con patrón Singleton.
    
    Carga configuración desde múltiples fuentes en orden de prioridad:
    1. Variables de entorno
    2. Archivo .env
    3. Archivo config.yaml
    4. Valores por defecto
    
    Example:
        >>> config = ConfigManager.get_instance()
        >>> print(config.app.name)
        'Trading Bot Híbrido'
    """
    
    _instance: Optional['ConfigManager'] = None
    _config: Optional[TradingBotConfig] = None
    
    def __new__(cls) -> 'ConfigManager':
        """Implementa Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializa el gestor de configuración."""
        if self._config is None:
            self._config = self._load_config()
    
    @classmethod
    def get_instance(cls) -> 'ConfigManager':
        """
        Obtiene la instancia singleton del ConfigManager.
        
        Returns:
            Instancia única de ConfigManager
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def _load_config(self) -> TradingBotConfig:
        """
        Carga configuración desde múltiples fuentes.
        
        Returns:
            Configuración validada
            
        Raises:
            ValidationError: Si la configuración es inválida
        """
        # 1. Cargar variables de entorno desde .env
        env_path = Path(__file__).parent.parent.parent / 'configs' / '.env'
        if env_path.exists():
            load_dotenv(env_path)
        
        # 2. Cargar configuración desde YAML
        yaml_config = self._load_yaml_config()
        
        # 3. Combinar con variables de entorno
        config_dict = self._merge_config(yaml_config)
        
        # 4. Validar y crear configuración
        try:
            config = TradingBotConfig(**config_dict)
            return config
        except ValidationError as e:
            print(f"❌ Error de validación en configuración:")
            print(e)
            raise
    
    def _load_yaml_config(self) -> dict:
        """
        Carga configuración desde archivo YAML.
        
        Returns:
            Diccionario con configuración del YAML
        """
        yaml_path = Path(__file__).parent.parent.parent / 'configs' / 'config.yaml'
        
        if not yaml_path.exists():
            return {}
        
        with open(yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    
    def _merge_config(self, yaml_config: dict) -> dict:
        """
        Combina configuración YAML con variables de entorno.
        
        Args:
            yaml_config: Configuración desde YAML
            
        Returns:
            Configuración combinada
        """
        config = yaml_config.copy()
        
        # Añadir configuración del broker desde env
        if 'broker' not in config:
            config['broker'] = {}
        
        config['broker']['api_key_id'] = os.getenv('ALPACA_API_KEY_ID', '')
        config['broker']['api_secret_key'] = os.getenv('ALPACA_API_SECRET_KEY', '')
        config['broker']['base_url'] = os.getenv(
            'ALPACA_BASE_URL',
            'https://paper-api.alpaca.markets'
        )
        
        # Añadir configuración de base de datos desde env
        if 'database' not in config:
            config['database'] = {}
        
        config['database']['host'] = os.getenv('DB_HOST', 'localhost')
        config['database']['port'] = int(os.getenv('DB_PORT', '5432'))
        config['database']['user'] = os.getenv('DB_USER', 'user')
        config['database']['password'] = os.getenv('DB_PASS', 'password')
        config['database']['database'] = os.getenv('DB_NAME', 'trading_bot')
        
        return config
    
    @property
    def config(self) -> TradingBotConfig:
        """
        Obtiene la configuración actual.
        
        Returns:
            Configuración validada
        """
        if self._config is None:
            self._config = self._load_config()
        return self._config
    
    def reload(self) -> None:
        """Recarga la configuración desde las fuentes."""
        self._config = self._load_config()
    
    def __repr__(self) -> str:
        """Representación string del ConfigManager."""
        return f"ConfigManager(app={self.config.app.name}, env={self.config.app.environment})"


def get_config() -> TradingBotConfig:
    """
    Función helper para obtener la configuración.
    
    Returns:
        Configuración validada del Trading Bot
        
    Example:
        >>> from src.utils.config import get_config
        >>> config = get_config()
        >>> print(config.app.name)
    """
    return ConfigManager.get_instance().config


# Exportar para uso externo
__all__ = [
    'TradingBotConfig',
    'AppConfig',
    'DataConfig',
    'BrokerConfig',
    'TradingConfig',
    'RiskConfig',
    'LoggingConfig',
    'DatabaseConfig',
    'ConfigManager',
    'get_config',
    'Environment',
]
