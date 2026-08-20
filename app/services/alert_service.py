from typing import Any, Protocol

from app.domain.alert import AlertStatus


class AlertRepositoryProtocol(Protocol):
    def get_by_id(self, alert_id: int) -> Any: ...
    def get_all(
        self,
        status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Any]: ...
    def update(self, alert: Any, update_data: dict[str, Any]) -> Any: ...


class AlertService:
    _allowed_transitions = {
        AlertStatus.OPEN: AlertStatus.ACKNOWLEDGED,
        AlertStatus.ACKNOWLEDGED: AlertStatus.RESOLVED,
    }

    def __init__(self, repo: AlertRepositoryProtocol) -> None:
        self.repo = repo

    def list_alerts(
        self,
        status: AlertStatus | None,
        limit: int,
        offset: int,
    ) -> list[Any]:
        return self.repo.get_all(
            status=status.value if status else None,
            limit=limit,
            offset=offset,
        )

    def change_status(self, alert_id: int, new_status: AlertStatus) -> Any:
        alert = self.repo.get_by_id(alert_id)
        if alert is None:
            raise LookupError("Alerta no encontrada")

        current_status = AlertStatus(alert.status)
        expected_status = self._allowed_transitions.get(current_status)
        if new_status != expected_status:
            raise ValueError(
                f"Transición inválida: {current_status.value} -> {new_status.value}"
            )

        return self.repo.update(alert, {"status": new_status.value})
