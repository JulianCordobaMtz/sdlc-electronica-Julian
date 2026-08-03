from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# 1. Creamos el motor conectando a un archivo local SQLite
engine = create_engine(
    "sqlite:///sensorhub.db",
    connect_args={"check_same_thread": False},
)

# 2. Factory de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Clase base de la que heredarán todos tus modelos
class Base(DeclarativeBase):
    pass


# 4. Generador de dependencias para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
