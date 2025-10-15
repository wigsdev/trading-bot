# Usamos Python 3.11 slim para ser ligero y moderno
FROM python:3.11-slim

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivo de dependencias
COPY requirements.txt .

# Actualizar pip e instalar dependencias
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copiar código fuente
COPY src/ /app/src

# Evitar buffering de salida para ver logs en tiempo real
ENV PYTHONUNBUFFERED=1

# Comando por defecto al iniciar el contenedor
CMD ["python", "src/main.py"]
