FROM python:3.12-slim

WORKDIR /workspace

# Copiamos e instalamos dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPIAMOS LOS ARCHIVOS DE ALEMBIC (Esto es lo que falta)
COPY alembic.ini .
COPY alembic/ ./alembic

# Copiamos el código de la aplicación
COPY app/ ./app

# Comando de arranque corregido en formato de terminal de Docker
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
