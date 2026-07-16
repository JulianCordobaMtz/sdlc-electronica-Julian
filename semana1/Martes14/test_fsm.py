#IMPORTACIONES
import pytest
from fsm_demo import TrafficLightFSM, TrafficLightState

@pytest.fixture #Crea un semáforo nuevo y limpio para cada prueba, para que no se mezclen
def fsm():
    return TrafficLightFSM()

# Se empieza a trabajar la prueba del estado de fábrica
def test_estado_inicial(fsm):
    assert fsm.state == TrafficLightState.RED #Comprueba que al encender, el color sea ROJO obligatoriamente

# Prueba para verificar el primer cambio de color
def test_transicion_red_a_green(fsm):
    nuevo_estado = fsm.transition() #Le da la orden de cambiar y guarda el resultado
    
    assert nuevo_estado == TrafficLightState.GREEN #Verifica que el color que devolvió la promesa sea VERDE
    assert fsm.state == TrafficLightState.GREEN #Verifica que la caja fuerte interna también guardó el VERDE

# Prueba para someter al semáforo a un ciclo completo
def test_ciclo_completo_a_red(fsm):
    fsm.transition() #Pasa de ROJO a VERDE
    assert fsm.state == TrafficLightState.GREEN
    
    fsm.transition() #Pasa de VERDE a AMARILLO
    assert fsm.state == TrafficLightState.YELLOW
    
    fsm.transition() #Pasa de AMARILLO a ROJO
    assert fsm.state == TrafficLightState.RED

# Prueba para verificar que la memoria del contador sume correctamente
def test_conteo_de_ciclos(fsm):
    assert fsm._cycle_count == 0 #Al iniciar, el contador de la máquina debe estar en cero
    
    fsm.transition() 
    assert fsm._cycle_count == 1 #Al hacer el primer cambio, el contador debe subir a 1
    
    fsm.transition() 
    assert fsm._cycle_count == 2 #Al hacer el segundo cambio, el contador debe subir a 2
    
    fsm.transition() 
    assert fsm._cycle_count == 3 #Al hacer el tercer cambio, el contador debe subir a 3
    
    assert fsm.state == TrafficLightState.RED #Comprueba que en este punto el semáforo volvió a ROJO