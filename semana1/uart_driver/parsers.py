from abc import ABC, abstractmethod

# EL MOLDE PRINCIPAL (Clase Abstracta)
class MessageParser(ABC):
    """Clase base abstracta para los decodificadores de protocolo.
    Define un contrato estricto: cualquier decodificador nuevo debe 
    tener la capacidad de identificar si el mensaje es suyo y de traducirlo."""
    

    @abstractmethod
    def can_parse(self, raw_data: bytes) -> bool:
        """Analiza los bytes crudos para determinar si corresponden a este protocolo.
        Retorna True si el mensaje tiene el formato correcto, False en caso contrario."""
        pass

    @abstractmethod
    def parse(self, raw_data: bytes) -> dict:
        """Toma los bytes crudos y los decodifica en un formato estructurado.
        Retorna un diccionario de Python con los datos extraídos."""
        pass

# LOS DECODIFICADORES ESPECÍFICOS (Implementaciones)
class ModbusParser(MessageParser):
    """Decodificador específico para tramas Modbus RTU.
    Identifica mensajes que inician con la dirección del esclavo y una función."""
    
    def can_parse(self, raw_data: bytes) -> bool:
        # Mínimo: dirección (1) + función (1) + CRC (2)
        if len(raw_data) < 4:
            return False
        
        # La dirección del esclavo debe estar en rango válido (1-247)
        slave_addr = raw_data[0]
        if not (1 <= slave_addr <= 247):
            return False
        
        # La función debe estar en rango válido (1-127, 129-245)
        func_code = raw_data[1]
        valid_functions = set(range(1, 128)) | set(range(129, 246))
        return func_code in valid_functions

    def parse(self, raw_data: bytes) -> dict:
        return {
            'slave_address': raw_data[0],
            'function_code': raw_data[1],
            'data': raw_data[2:-2].hex() if len(raw_data) > 4 else '',
            'crc': f"{raw_data[-2]:02x}{raw_data[-1]:02x}",
            'length': len(raw_data)
        }


class NMEAParser(MessageParser):
    """Decodificador específico para sentencias NMEA.
    Identifica mensajes de texto que inician con '$' y terminan con salto de línea."""
    
    def can_parse(self, raw_data: bytes) -> bool:
        # Debe comenzar con '$' y terminar con salto de línea
        if len(raw_data) < 6:
            return False
        
        if raw_data[0:1] != b'$':
            return False
        
        # Termina con \n o \r\n
        return raw_data.endswith(b'\n') or raw_data.endswith(b'\r\n')

    def parse(self, raw_data: bytes) -> dict:
        try:
            # Decodificar bytes a string y limpiar
            sentence = raw_data.decode('ascii').strip()
            
            # Remover el '$' inicial
            if sentence.startswith('$'):
                sentence = sentence[1:]
            
            # Dividir por comas
            parts = sentence.split(',')
            
            return {
                'type': parts[0][:5],
                'fields': parts[1:],
                'raw': sentence,
                'valid': len(parts) > 1
            }
        except (UnicodeDecodeError, IndexError):
            return {'valid': False, 'error': 'Invalid NMEA sentence'}