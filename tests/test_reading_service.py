from app.schemas.reading import SensorReadingIn
from app.services.reading_service import ReadingService
# 1. EL REPOSITORIO FAKE EN MEMORIA (Sin tocar SQLAlchemy ni SQLite)
class FakeReadingRepository:
    def __init__(self):
        # Usamos una simple lista de Python como nuestra "base de datos"
        self.datos_en_memoria = []

    def create(self, db, reading_in: SensorReadingIn):
        # Guardamos los datos en la lista y les inventamos un ID
        lectura = reading_in.model_dump()
        lectura["id"] = len(self.datos_en_memoria) + 1
        self.datos_en_memoria.append(lectura)
        return lectura

# 2. EL TEST DEL SERVICIO
def test_registrar_lectura_con_fake_repo():
    # Instanciamos el repositorio falso
    fake_repo = FakeReadingRepository()
    
    # Inyectamos la dependencia falsa al servicio (¡Este es el pago del DIP!)
    service = ReadingService(repo=fake_repo)
    
    # Preparamos una lectura de prueba
    lectura_in = SensorReadingIn(sensor_id="TEMP-01", value=25.5, unit="C")
    
    # Ejecutamos el servicio (pasamos db=None porque el fake_repo no usa SQLAlchemy)
    resultado = service.registrar_lectura(db=None, reading_in=lectura_in)
    
    # Verificamos que el servicio haya procesado y guardado correctamente
    assert resultado["id"] == 1
    assert resultado["sensor_id"] == "TEMP-01"
    assert len(fake_repo.datos_en_memoria) == 1