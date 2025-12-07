# Trading Bot Híbrido

Bot de trading híbrido para:
- Ejecución automática de acciones US (Alpaca)
- Análisis y alertas para acciones BVL (Perú)

## 🚀 Estado del Proyecto

**Versión Actual**: 0.1.0 (Documentación)  
**Versión Objetivo**: 1.0.0 (Producción)  
**Progreso**: 5% (Fase 0 completada)

## 📚 Documentación

### Documentación de Gestión
- **[📍 Roadmap](docs/project/ROADMAP.md)** - Plan completo del proyecto (8 fases)
- **[✅ Task List](docs/project/TASK_LIST.md)** - 150+ tareas detalladas
- **[⚡ Quick Reference](docs/project/QUICK_REFERENCE.md)** - Guía rápida

### Documentación Técnica
- **[Documentación Completa](docs/)** - Toda la documentación del proyecto
- **[Getting Started](docs/getting-started/)** - Guías de inicio
- **[Arquitectura](docs/architecture/)** - Diseño del sistema
- **[SDLC](docs/development/sdlc.md)** - Ciclo de vida del desarrollo
- **[Análisis de Arquitectura](docs/architecture/ARCHITECTURE_REVIEW.md)** - Revisión crítica

## 🎯 Próximos Pasos

**Fase 1 - Core Infrastructure** (2-3 semanas):
1. Sistema de configuración con validación
2. Manejo robusto de errores
3. Gestión de estado persistente
4. Data layer con rate limiting
5. Health checks y métricas

Ver [ROADMAP.md](docs/project/ROADMAP.md) para el plan completo.

## 🏗️ Tecnologías

- **Python** 3.10+
- **Docker** - Containerización
- **PostgreSQL/TimescaleDB** - Base de datos
- **Alpaca API** - Trading de acciones US
- **VectorBT** - Backtesting
- **Telegram Bot** - Alertas

## 📦 Instalación

```bash
# Clonar repositorio
git clone <repo-url>
cd trading-bot

# Crear entorno virtual
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash

# Instalar dependencias
pip install -r requirements.txt

# Configurar
cp configs/.env.example configs/.env
# Editar .env con tus credenciales
```

Ver [Guía de Instalación](docs/getting-started/installation.md) para más detalles.

## 🔧 Uso

```bash
# Ejecutar bot
python src/main.py

# Ejecutar backtest
python scripts/backtest.py

# Verificar configuración
python scripts/verify_config.py
```

Ver [Quick Start](docs/getting-started/quick-start.md) para ejemplos.

## 🧪 Testing

```bash
# Todos los tests
pytest

# Con coverage
pytest --cov=src --cov-report=html

# Solo unit tests
pytest -m unit
```

Ver [Guía de Testing](docs/development/testing.md).

## 🤝 Contribuir

Seguimos **Conventional Commits** y un proceso de desarrollo estructurado:

```bash
# Tipos de commits
feat:     Nueva funcionalidad
fix:      Corrección de bug
docs:     Actualización documentación
test:     Tests
chore:    Tareas de mantenimiento
```

Ver [Guía de Contribución](docs/development/contributing.md) para más detalles.

## 📊 Estructura del Proyecto

```
trading-bot/
├── docs/                   # Documentación completa
│   ├── project/           # Gestión del proyecto
│   │   ├── ROADMAP.md
│   │   ├── TASK_LIST.md
│   │   └── QUICK_REFERENCE.md
│   ├── getting-started/   # Guías de inicio
│   ├── architecture/      # Arquitectura
│   ├── development/       # Desarrollo
│   └── examples/          # Ejemplos
├── src/                   # Código fuente
│   ├── strategies/        # Estrategias de trading
│   ├── data/             # Gestión de datos
│   ├── brokers/          # Integraciones
│   ├── execution/        # Ejecución de órdenes
│   └── utils/            # Utilidades
├── tests/                # Tests
├── configs/              # Configuración
├── docker/               # Docker
└── scripts/              # Scripts útiles
```

## ⚠️ Advertencias

- **NO DEPLOYAR A PRODUCCIÓN** hasta completar Fase 1-4 y testing exhaustivo
- Siempre usar **paper trading** primero
- Nunca commitear archivos `.env`
- Validar toda configuración antes de ejecutar

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles.

## 📞 Contacto

- **Issues**: [GitHub Issues](https://github.com/tu-usuario/trading-bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tu-usuario/trading-bot/discussions)

---

**Última actualización**: 2024-12-07  
**Versión**: 0.1.0
