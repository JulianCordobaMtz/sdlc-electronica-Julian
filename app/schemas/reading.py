from pydantic import BaseModel, Field, field_validator

class SensorReadingIn(BaseModel):
    sensor_id: str = Field(..., examples=["TEMP-01"])
    value: float
    unit: str = "C"

    @field_validator('unit')
    @classmethod
    def validar_unidad(cls, v):
        if v not in ["C", "F"]:
            raise ValueError("Unidad desconocida. Solo se permite 'C' o 'F'")
        return v

    @field_validator('value')
    @classmethod
    def validar_cero_absoluto(cls, v, info):
        # info.data contiene los valores previamente validados (como 'unit')
        unidad = info.data.get('unit', 'C')
        
        # Validación física real
        if unidad == "C" and v < -273.15:
            raise ValueError("Temperatura por debajo del cero absoluto físicamente imposible (-273.15 C)")
        elif unidad == "F" and v < -459.67:
            raise ValueError("Temperatura por debajo del cero absoluto físicamente imposible (-459.67 F)")
            
        return v

class SensorReadingOut(SensorReadingIn):
    id: int