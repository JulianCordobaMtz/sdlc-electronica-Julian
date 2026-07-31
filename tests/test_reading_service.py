from app.services.reading_service import ReadingService
from app.schemas.reading import SensorReadingIn

# 1. Actualizamos el repositorio Fake para que exija 'sensor_id' y los datos en formato diccionario, igual que tu repo real de hoy.
class FakeReadingRepository:
    def create(self, db, sensor_id: str, data: dict):
        class FakeReading:
            def __init__(self, sensor_id, data):
                self.id = 1
                self.sensor_id = sensor_id
                self.value = data["value"]
                self.unit = data.get("unit", "C")
        return FakeReading(sensor_id, data)

def test_registrar_lectura_con_fake_repo():
    fake_repo = FakeReadingRepository()
    servicio = ReadingService(repo=fake_repo)
    
    lectura_in = SensorReadingIn(value=25.5, unit="C")
    
    # 2. LA CORRECCIÓN: Ahora pasamos correctamente el ID del sensor ("TEMP-FAKE") como segundo argumento.
    resultado = servicio.registrar_lectura(None, "TEMP-FAKE", lectura_in)
    
    assert resultado.value == 25.5
    assert resultado.sensor_id == "TEMP-FAKE"