from fastapi import Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.repositories.reading_repo import ReadingRepository
from app.repositories.alert_repository import AlertRepository
from app.services.reading_service import ReadingService
from app.services.anomaly_detector import AnomalyDetector, DatabaseAlertStrategy

def get_reading_service(db: Session = Depends(get_db)) -> ReadingService:
    """Inyecta una instancia fresca de ReadingService con su repositorio
    y el detector de anomalías configurado para persistir alertas en base de datos.
    """
    repo = ReadingRepository(db)
    alert_repo = AlertRepository(db)
    strategy = DatabaseAlertStrategy(alert_repo)
    detector = AnomalyDetector(strategy)

    return ReadingService(repo, detector=detector)