# Trading Bot Híbrido

## Descripción
Bot de trading híbrido para:
- Ejecución automática de acciones US (Alpaca)
- Análisis y alertas para acciones BVL (Perú)

## Tecnologías
- Python 3.10+
- Docker
- PostgreSQL / TimescaleDB
- Alpaca API
- VectorBT para backtesting
- Telegram Bot para alertas

## Instalación
1. Clonar repositorio
```bash
git clone <repo-url>
cd trading-bot
```
2. Crear entorno virtual y activar
```bash
python -m venv venv
source venv/Scripts/activate
```

3. Instalar dependencias
```bash
pip install -r requirements.txt
```

## Uso

- Ejecutar scripts de backtest

```bash
python scripts/backtest.py
```

- Ingesta de datos BVL

```bash
python scripts/ingest_bvl.py
```

## Contributing

- Seguimos Conventional Commits:

```bash
feat: nueva funcionalidad
fix: corrección de bug
docs: actualización documentación
chore: tareas de mantenimiento
```

## Licencia
MIT
