# 1. Usamos una versión oficial de Python delgada (slim) para minimizar el peso, como exige tu rúbrica
FROM python:3.12-slim

# 2. Evitamos que Python escriba archivos compilados .pyc en el disco del contenedor
ENV PYTHONDONTWRITEBYTECODE=1

# 3. Forzamos a que los logs de Python se impriman de inmediato en la terminal sin quedarse en el búfer
ENV PYTHONUNBUFFERED=1

# 4. Establecemos el directorio de trabajo dentro del sistema de archivos virtual del contenedor
WORKDIR /workspace

# 5. Instalamos las dependencias del sistema necesarias para PostgreSQL (para la base psycopg que usaremos después)
# y limpiamos la caché del gestor de paquetes para mantener la imagen lo más ligera posible
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 6. Copiamos ÚNICAMENTE el archivo de dependencias primero.
# ¡ESTO ES CLAVE PARA LA CACHÉ DE CAPAS! Si tu requirements.txt no cambia, 
# Docker no volverá a instalar las librerías al reconstruir, ahorrándote minutos valiosos.
COPY requirements.txt /workspace/

# 7. Instalamos las librerías de Python especificadas en tu requirements
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 8. Copiamos el código fuente de tu aplicación a la carpeta /workspace/app dentro del contenedor
COPY ./app /workspace/app

# 9. Declaramos el "pin físico" de red que utilizará el contenedor para recibir peticiones
EXPOSE 8000

# 10. Comando de ejecución que arranca tu servidor web Uvicorn escuchando en todas las interfaces de red (0.0.0.0)
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]