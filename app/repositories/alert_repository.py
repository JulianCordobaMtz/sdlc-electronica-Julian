from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.alert import AlertModel

class AlertRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, alert: AlertModel) -> AlertModel:
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def get_by_id(self, alert_id: int) -> Optional[AlertModel]:
        stmt = select(AlertModel).where(AlertModel.id == alert_id)
        return self.db.scalars(stmt).first()

    def get_all(
        self, status: Optional[str] = None, limit: int = 50, offset: int = 0
    ) -> List[AlertModel]:
        stmt = select(AlertModel)
        if status is not None:
            stmt = stmt.where(AlertModel.status == status)
        stmt = stmt.offset(offset).limit(limit)
        return list(self.db.scalars(stmt).all())

    def update(self, alert: AlertModel, update_data: dict) -> AlertModel:
        for key, value in update_data.items():
            setattr(alert, key, value)
        self.db.commit()
        self.db.refresh(alert)
        return alert