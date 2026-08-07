import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# 1. Leemos la URL de la base de datos desde el entorno,
# usando SQLite como respaldo local [1]
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///sensorhub.db")

# 2. Normalizamos la URL si viene con el formato viejo de Render
# (postgres:// -> postgresql://) [2]
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Configuración especial para SQLite (evita bloqueos de hilos
# en pruebas de desarrollo local)
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
# 4. Creamos el motor de base de datos
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# 5. Fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()