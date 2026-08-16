
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.alert_repository import AlertRepository
from app.schemas.alert import AlertOut, AlertUpdate

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("/", response_model=list[AlertOut])
def listar_alertas(
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    repo = AlertRepository(db)
    return repo.get_all(status=status, limit=limit, offset=offset)

@router.patch("/{alert_id}", response_model=AlertOut)
def actualizar_estado_alerta(
    alert_id: int,
    alert_update: AlertUpdate,
    db: Session = Depends(get_db)
):
    repo = AlertRepository(db)
    alert = repo.get_by_id(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return repo.update(alert, alert_update.model_dump(exclude_unset=True))