FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN addgroup --system sensorhub \
    && adduser --system --ingroup sensorhub sensorhub

COPY alembic.ini .
COPY alembic/ ./alembic
COPY app/ ./app

RUN chown -R sensorhub:sensorhub /workspace
USER sensorhub

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && exec uvicorn app.main:app --host 0.0.0.0 --port 8000"]
