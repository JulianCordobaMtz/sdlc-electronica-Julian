import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# 1. Leemos la URL de la base de datos desde el entorno
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///sensorhub.db")

# 2. Normalizamos la URL si viene de Render para forzar el uso de psycopg v3
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://") and "+psycopg" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

# 3. Configuración especial para SQLite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# 4. Creación del motor de base de datos
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# 5. Configuración de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 6. Clase base para los modelos ORM
class Base(DeclarativeBase):
    pass


# 7. Dependencia para obtener la sesión de la base de datos (¡Restaurada!)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
