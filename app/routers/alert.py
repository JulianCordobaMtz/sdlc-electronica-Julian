from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies import get_alert_service
from app.domain.alert import AlertStatus
from app.schemas.alert import AlertOut, AlertUpdate
from app.services.alert_service import AlertService

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/", response_model=list[AlertOut])
def listar_alertas(
    status: AlertStatus | None = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: AlertService = Depends(get_alert_service),
):
    return service.list_alerts(status=status, limit=limit, offset=offset)


@router.patch("/{alert_id}", response_model=AlertOut)
def actualizar_estado_alerta(
    alert_id: int,
    alert_update: AlertUpdate,
    service: AlertService = Depends(get_alert_service),
):
    try:
        return service.change_status(alert_id, alert_update.status)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
