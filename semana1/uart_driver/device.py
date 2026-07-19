from typing import List
from config import UartConfig 
from parsers import MessageParser

class UARTDevice:
    """Controlador central de la comunicación serial.
    Su única responsabilidad (SRP) es orquestar el flujo de datos: 
    recibir bytes y pasarlos al decodificador correcto."""

    def __init__(self, config: UartConfig, parsers: List[MessageParser]) -> None:
        """Inicializa el dispositivo inyectando sus dependencias (DIP).
        Recibe las reglas de configuración y una lista de módulos decodificadores compatibles."""
        # DIP: Inyectamos las dependencias en lugar de crearlas internamente
        # Esto permite cambiar la configuración y parsers sin modificar la clase
        self.config = config
        self.parsers = parsers
        self._is_connected = False

    def connect(self) -> None:
        """Simula la apertura del puerto serial utilizando la configuración inyectada."""
        # Usa la configuración que fue inyectada en __init__ (DIP en acción)
        self._is_connected = True
        print(f"UART conectado: {self.config.baudrate} baud, paridad {self.config.parity}, {self.config.stop_bits} stop bits")

    def receive_data(self, raw_data: bytes) -> dict:
        """Recibe los bytes crudos del hardware y busca entre sus decodificadores
        cuál es capaz de traducirlos. Retorna el diccionario con los datos.
        Levanta un ValueError si ningún decodificador reconoce la trama."""
        # Verificar que el puerto esté conectado antes de procesar datos
        if not self._is_connected:
            raise RuntimeError("UARTDevice no está conectado. Llame a connect() antes de receive_data().")

        # SRP: Solo orquesta, no implementa lógica de decodificación
        # Itera sobre los decodificadores inyectados (DIP)
        for parser in self.parsers:
            if parser.can_parse(raw_data):
                # LSP: Todos los parsers implementan la interfaz MessageParser
                return parser.parse(raw_data)
        
        # Si ningún decodificador reconoce el formato, rechazar
        raise ValueError(f"No parser encontrado para datos: {raw_data.hex()}")