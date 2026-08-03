import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# 1. Leemos la URL de la base de datos desde el entorno, o usamos SQLite por defecto
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///sensorhub.db")

# 2. Configuración específica para SQLite (necesaria para FastAPI en modo local)
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# 3. Creamos el motor de base de datos (Engine)
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# 4. Creamos la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Clase base para nuestros modelos ORM (Sintaxis SQLAlchemy 2.0)
class Base(DeclarativeBase):
    pass

# 6. Función generadora de dependencias para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()