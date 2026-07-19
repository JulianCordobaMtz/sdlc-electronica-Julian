import json
from pathlib import Path

class DataRecorder:
    """Componente dedicado a persistir (guardar) los datos decodificados.
    Su única responsabilidad (SRP) es manejar el sistema de archivos
    sin interferir con la comunicación UART."""

    def __init__(self, log_directory: str) -> None:
        """Inicializa el módulo de almacenamiento.
        Recibe la ruta de la carpeta donde se guardarán los archivos."""
        # Convertir la ruta a objeto Path para manipulación multiplataforma
        self.log_directory = Path(log_directory)
        
        # Crear la carpeta si no existe (SRP: solo manejar sistema de archivos)
        self.log_directory.mkdir(parents=True, exist_ok=True)

    def record(self, data: dict, filename: str = "uart_log.json") -> None:
        """Toma el diccionario de datos ya procesado y lo anexa a un archivo JSON."""
        # Construir la ruta completa del archivo
        file_path = self.log_directory / filename
        
        # Lista para almacenar todos los registros
        records = []
        
        # Si el archivo ya existe, cargar los datos existentes
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    records = json.load(f)
            except (json.JSONDecodeError, IOError):
                # Si el archivo está vacío o corrupto, comenzar con lista vacía
                records = []
        
        # Anexar el nuevo registro (SRP: solo escribir datos, no procesarlos)
        records.append(data)
        
        # Guardar la lista actualizada en JSON
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False)