#IMPORTACIONES
from enum import Enum, auto

#Se crea la clase TrafficLightState haciendo uso de Enum para la asignación de los estados de los colores
class TrafficLightState (Enum):
    RED = auto()
    YELLOW = auto()
    GREEN = auto()

# Se empieza a trabajar la clase TrafficLightFSM 
class TrafficLightFSM:
    def __init__(self) -> None: #Se usa para iniciar el semáforo
        self._state = TrafficLightState.RED
        self._cycle_count = 0

    @property #Bloquea el estado del semáforo para que no pueda ser modificado desde fuera
    def state(self): #Se usa para obtener el estado del semáforo    
         return self._state
    
    def transition(self) -> TrafficLightState: #Hace una promesa con la flechita para devolver un color nada más
        # 1. El diccionario de rutas 
        transitions = {
            TrafficLightState.RED: TrafficLightState.GREEN,
            TrafficLightState.GREEN: TrafficLightState.YELLOW,
            TrafficLightState.YELLOW: TrafficLightState.RED,
        }
        self._state = transitions[self._state] #Mete la variable actual en los corchetes, en el diccionario viene la acción ante ese color, procede a guardar el estado.
        self._cycle_count += 1 #Crea un contador de ciclos para saber cuántas veces ha cambiado de color el semáforo
        return self._state #Devuelve el estado actual del semáforo

