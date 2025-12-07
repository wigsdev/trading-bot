# ⚙️ Configuración

Guía completa para configurar el Trading Bot Híbrido.

## 📁 Archivos de Configuración

El bot utiliza dos archivos principales de configuración:

1. **`configs/config.yaml`** - Configuración general de la aplicación
2. **`configs/.env`** - Variables de entorno y credenciales (sensible)

## 🔐 Configuración de Variables de Entorno

### 1. Crear archivo .env

```bash
cp configs/.env.example configs/.env
```

### 2. Editar configs/.env

```bash
# Claves del broker Alpaca
ALPACA_API_KEY_ID=tu_api_key_aqui
ALPACA_API_SECRET_KEY=tu_secret_key_aqui
ALPACA_BASE_URL=https://paper-api.alpaca.markets

# Configuración base de datos (futuro)
DB_USER=trading_user
DB_PASS=tu_password_seguro
DB_HOST=localhost
DB_PORT=5432
DB_NAME=trading_bot

# Telegram Bot (opcional)
TELEGRAM_BOT_TOKEN=tu_token_de_telegram
TELEGRAM_CHAT_ID=tu_chat_id
```

### 3. Obtener Credenciales de Alpaca

1. Inicia sesión en [Alpaca Markets](https://alpaca.markets)
2. Ve a **Paper Trading** → **API Keys**
3. Genera nuevas claves (Key ID y Secret Key)
4. Copia las claves a tu archivo `.env`

> ⚠️ **IMPORTANTE**: Nunca compartas tus claves API ni las subas a Git

### 4. Configurar Bot de Telegram (Opcional)

1. Abre Telegram y busca **@BotFather**
2. Envía `/newbot` y sigue las instrucciones
3. Copia el token que te proporciona
4. Para obtener tu Chat ID:
   - Busca **@userinfobot**
   - Envía `/start`
   - Copia tu ID

## 📝 Configuración de config.yaml

Edita `configs/config.yaml`:

```yaml
# Configuración principal del bot
app:
  name: "Trading Bot Híbrido"
  version: "0.1.0"
  environment: "development"  # development, staging, production

# Configuración de datos
data:
  storage_path: "data/"
  log_path: "logs/"
  cache_enabled: true
  cache_ttl: 3600  # segundos

# Configuración del broker
broker:
  provider: "alpaca"
  paper_trading: true  # true para paper trading, false para live
  
# Configuración de trading
trading:
  max_positions: 5
  position_size: 0.2  # 20% del capital por posición
  stop_loss: 0.02     # 2% stop loss
  take_profit: 0.05   # 5% take profit

# Configuración de backtesting
backtesting:
  initial_capital: 10000
  commission: 0.001  # 0.1%
  slippage: 0.0005   # 0.05%

# Configuración de alertas
alerts:
  telegram_enabled: true
  email_enabled: false
  
# Configuración de logging
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file_enabled: true
  console_enabled: true
```

## 🎯 Configuraciones por Entorno

### Development (Desarrollo)

```yaml
app:
  environment: "development"

broker:
  paper_trading: true

logging:
  level: "DEBUG"
```

### Production (Producción)

```yaml
app:
  environment: "production"

broker:
  paper_trading: false  # ⚠️ CUIDADO: Trading real

logging:
  level: "INFO"
  
trading:
  max_positions: 3
  position_size: 0.1  # Más conservador
```

## 🔒 Seguridad

### Buenas Prácticas

1. **Nunca commitear .env**
   - Verificar que `.env` está en `.gitignore`
   
2. **Usar paper trading primero**
   - Probar todas las estrategias en paper trading
   
3. **Rotar claves regularmente**
   - Cambiar API keys cada 3-6 meses
   
4. **Permisos de archivos**
   ```bash
   chmod 600 configs/.env  # Solo lectura/escritura para el usuario
   ```

## ✅ Verificar Configuración

Crea un script de verificación `scripts/verify_config.py`:

```python
import os
from dotenv import load_dotenv
import yaml

def verify_config():
    # Cargar .env
    load_dotenv('configs/.env')
    
    # Verificar variables requeridas
    required_vars = [
        'ALPACA_API_KEY_ID',
        'ALPACA_API_SECRET_KEY',
        'ALPACA_BASE_URL'
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"❌ Variables faltantes: {', '.join(missing)}")
        return False
    
    # Cargar config.yaml
    with open('configs/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    print("✅ Configuración válida")
    print(f"   Entorno: {config['app']['environment']}")
    print(f"   Paper Trading: {config['broker']['paper_trading']}")
    return True

if __name__ == "__main__":
    verify_config()
```

Ejecutar:
```bash
python scripts/verify_config.py
```

## ➡️ Siguiente Paso

Continúa con la [**Guía de Inicio Rápido**](quick-start.md) para empezar a usar el bot.

## 📚 Referencias

- [Alpaca API Documentation](https://alpaca.markets/docs/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [YAML Syntax](https://yaml.org/spec/1.2/spec.html)
