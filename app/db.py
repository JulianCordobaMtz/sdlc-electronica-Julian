from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

# 1. Creamos el motor conectando a un archivo local SQLite
engine = create_engine(
    "sqlite:///sensorhub.db", 
    connect_args={"check_same_thread": False}
)

# 2. Clase base de la que heredarán todos tus modelos
class Base(DeclarativeBase):
    pass