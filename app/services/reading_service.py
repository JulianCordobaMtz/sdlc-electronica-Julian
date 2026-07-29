from sqlalchemy.orm import Session
from app.schemas.reading import SensorReadingIn

class ReadingService:
    # AHORA: El servicio recibe el repositorio como parámetro
    def __init__(self, repo):
        self.repo = repo

    def registrar_lectura(self, db: Session, reading_in: SensorReadingIn):
        return self.repo.create(db, reading_in)