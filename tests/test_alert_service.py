from types import SimpleNamespace

import pytest

from app.domain.alert import AlertStatus
from app.services.alert_service import AlertService


class FakeAlertRepository:
    def __init__(self, status: str = "open") -> None:
        self.alert = SimpleNamespace(id=1, status=status)
        self.last_list_arguments = None

    def get_by_id(self, alert_id: int):
        return self.alert if alert_id == self.alert.id else None

    def get_all(self, status=None, limit=50, offset=0):
        self.last_list_arguments = (status, limit, offset)
        return [self.alert]

    def update(self, alert, update_data):
        alert.status = update_data["status"]
        return alert


def test_alert_follows_valid_status_flow():
    service = AlertService(FakeAlertRepository())

    acknowledged = service.change_status(1, AlertStatus.ACKNOWLEDGED)
    resolved = service.change_status(1, AlertStatus.RESOLVED)

    assert acknowledged is resolved
    assert resolved.status == "resolved"


def test_alert_rejects_skipping_acknowledged_state():
    service = AlertService(FakeAlertRepository())

    with pytest.raises(ValueError, match="open -> resolved"):
        service.change_status(1, AlertStatus.RESOLVED)


def test_alert_rejects_changes_after_resolved():
    service = AlertService(FakeAlertRepository(status="resolved"))

    with pytest.raises(ValueError, match="resolved -> acknowledged"):
        service.change_status(1, AlertStatus.ACKNOWLEDGED)


def test_alert_reports_missing_id():
    service = AlertService(FakeAlertRepository())

    with pytest.raises(LookupError, match="Alerta no encontrada"):
        service.change_status(999, AlertStatus.ACKNOWLEDGED)


def test_alert_list_passes_filters_to_repository():
    repository = FakeAlertRepository()
    service = AlertService(repository)

    result = service.list_alerts(AlertStatus.OPEN, limit=20, offset=5)

    assert result == [repository.alert]
    assert repository.last_list_arguments == ("open", 20, 5)
