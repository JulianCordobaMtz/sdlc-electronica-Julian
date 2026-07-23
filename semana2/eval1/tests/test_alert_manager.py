from alert_manager import AlertManager

def test_alert_manager_envia_alerta():
    manager = AlertManager()
    resultado = manager.enviar_alerta("T1", "Alta temperatura")
    
    assert resultado is True
    assert "ALERTA" in manager.ultima_alerta