# 🐳 Docker Deployment

Guía para deployar el Trading Bot usando Docker.

## 📦 Dockerfile

El proyecto incluye un Dockerfile optimizado:

```dockerfile
# docker/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar código
COPY src/ /app/src
COPY configs/ /app/configs

# Variables de entorno
ENV PYTHONUNBUFFERED=1

# Comando por defecto
CMD ["python", "src/main.py"]
```

## 🚀 Build y Run

### Build de la Imagen

```bash
# Desde el directorio raíz del proyecto
docker build -t trading-bot:latest -f docker/Dockerfile .

# Con tag específico
docker build -t trading-bot:v1.0.0 -f docker/Dockerfile .
```

### Ejecutar Contenedor

```bash
# Ejecución básica
docker run --rm trading-bot:latest

# Con variables de entorno
docker run --rm \
  -e ALPACA_API_KEY_ID=tu_key \
  -e ALPACA_API_SECRET_KEY=tu_secret \
  -e ALPACA_BASE_URL=https://paper-api.alpaca.markets \
  trading-bot:latest

# Con archivo .env
docker run --rm \
  --env-file configs/.env \
  trading-bot:latest

# En modo interactivo
docker run -it --rm trading-bot:latest /bin/bash
```

## 🔧 Docker Compose

### docker-compose.yml

```yaml
version: '3.8'

services:
  trading-bot:
    build:
      context: .
      dockerfile: docker/Dockerfile
    container_name: trading-bot
    env_file:
      - configs/.env
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    networks:
      - trading-network
  
  postgres:
    image: timescale/timescaledb:latest-pg14
    container_name: trading-db
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASS}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - trading-network
    restart: unless-stopped

volumes:
  postgres-data:

networks:
  trading-network:
    driver: bridge
```

### Comandos Docker Compose

```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f trading-bot

# Detener servicios
docker-compose down

# Rebuild y restart
docker-compose up -d --build

# Ver estado
docker-compose ps
```

## 🔄 Multi-Stage Build

Para optimizar el tamaño de la imagen:

```dockerfile
# docker/Dockerfile.optimized
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Copiar dependencias del builder
COPY --from=builder /root/.local /root/.local

# Copiar código
COPY src/ /app/src
COPY configs/ /app/configs

# Asegurar que scripts en .local están en PATH
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

CMD ["python", "src/main.py"]
```

Build:
```bash
docker build -t trading-bot:optimized -f docker/Dockerfile.optimized .
```

## 📊 Monitoreo

### Health Check

```dockerfile
# Agregar al Dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import sys; sys.exit(0)"
```

### Logs

```bash
# Ver logs en tiempo real
docker logs -f trading-bot

# Últimas 100 líneas
docker logs --tail 100 trading-bot

# Logs con timestamps
docker logs -t trading-bot
```

## 🔐 Secrets Management

### Usando Docker Secrets

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  trading-bot:
    image: trading-bot:latest
    secrets:
      - alpaca_api_key
      - alpaca_secret_key
    environment:
      ALPACA_API_KEY_ID_FILE: /run/secrets/alpaca_api_key
      ALPACA_API_SECRET_KEY_FILE: /run/secrets/alpaca_secret_key

secrets:
  alpaca_api_key:
    external: true
  alpaca_secret_key:
    external: true
```

Crear secrets:
```bash
echo "tu_api_key" | docker secret create alpaca_api_key -
echo "tu_secret_key" | docker secret create alpaca_secret_key -
```

## 🚢 Production Deployment

### docker-compose.prod.yml

```yaml
version: '3.8'

services:
  trading-bot:
    image: registry.example.com/trading-bot:${VERSION}
    container_name: trading-bot-prod
    env_file:
      - configs/.env.production
    volumes:
      - /var/trading-bot/data:/app/data
      - /var/trading-bot/logs:/app/logs
    restart: always
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    networks:
      - trading-network
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M

  postgres:
    image: timescale/timescaledb:latest-pg14
    container_name: trading-db-prod
    env_file:
      - configs/.env.production
    volumes:
      - /var/trading-bot/postgres:/var/lib/postgresql/data
    restart: always
    networks:
      - trading-network

networks:
  trading-network:
    driver: bridge
```

### Deploy Script

```bash
#!/bin/bash
# scripts/deploy.sh

set -e

VERSION=${1:-latest}

echo "🚀 Deploying Trading Bot v${VERSION}..."

# Pull latest image
docker pull registry.example.com/trading-bot:${VERSION}

# Stop current container
docker-compose -f docker-compose.prod.yml down

# Start new version
VERSION=${VERSION} docker-compose -f docker-compose.prod.yml up -d

# Verify deployment
docker-compose -f docker-compose.prod.yml ps

echo "✅ Deployment complete!"
```

## 📚 Best Practices

### 1. Use .dockerignore

```
# .dockerignore
venv/
__pycache__/
*.pyc
.git/
.env
*.log
data/
logs/
tests/
docs/
.gitignore
README.md
```

### 2. Non-Root User

```dockerfile
# Crear usuario no-root
RUN useradd -m -u 1000 botuser && \
    chown -R botuser:botuser /app

USER botuser

CMD ["python", "src/main.py"]
```

### 3. Layer Caching

```dockerfile
# Copiar requirements primero (cambia menos frecuentemente)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Luego copiar código (cambia más frecuentemente)
COPY src/ /app/src
```

## 🔍 Troubleshooting

### Container no inicia

```bash
# Ver logs
docker logs trading-bot

# Ejecutar en modo interactivo
docker run -it --rm trading-bot:latest /bin/bash

# Verificar variables de entorno
docker exec trading-bot env
```

### Problemas de red

```bash
# Inspeccionar red
docker network inspect trading-network

# Verificar conectividad
docker exec trading-bot ping postgres
```

### Problemas de volúmenes

```bash
# Listar volúmenes
docker volume ls

# Inspeccionar volumen
docker volume inspect postgres-data

# Limpiar volúmenes no usados
docker volume prune
```

---

**Próximo paso**: [Production](production.md) para configuración de producción
