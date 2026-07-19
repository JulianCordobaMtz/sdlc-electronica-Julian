from dataclasses import dataclass
from typing import Literal

@dataclass(frozen=True)
class UartConfig:
    """Configuración inmutable para el puerto UART.
    Garantiza que parámetros críticos de hardware no sean modificados
    accidentalmente durante el tiempo de ejecución.

    Se proporcionan valores por defecto comunes para facilitar pruebas y uso
    por defecto: `baudrate=9600`, `parity='N'`, `stop_bits=1`, `timeout=1.0`.
    """
    baudrate: int = 9600
    parity: Literal['N', 'E', 'O'] = 'N'  # N: None, E: Even, O: Odd
    stop_bits: int = 1
    timeout: float = 1.0

    def __post_init__(self) -> None:
        """
        Valida las reglas de negocio justo después de instanciar la clase.
        - El baudrate debe ser un valor mayor a 0.
        - Los stop_bits deben ser 1 o 2.
        - La paridad debe ser 'N', 'E' u 'O'.
        Si los valores son inválidos, se lanza ValueError.
        """
        if self.baudrate <= 0:
            raise ValueError(f"El baudrate debe ser mayor a 0. Recibido: {self.baudrate}")

        if self.stop_bits not in (1, 2):
            raise ValueError(f"Los bits de parada deben ser 1 o 2. Recibido: {self.stop_bits}")

        if self.parity not in ('N', 'E', 'O'):
            raise ValueError(f"Paridad inválida. Use 'N', 'E' u 'O'. Recibido: {self.parity}")