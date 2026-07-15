import pytest
from fsm_demo import TrafficLightFSM, TrafficLightState


@pytest.fixture
def fsm():
    """Fixture que proporciona una instancia fresh del FSM para cada test"""
    return TrafficLightFSM()


def test_estado_inicial(fsm):
    """Test 1: Verifica que el estado inicial es RED"""
    assert fsm.state == TrafficLightState.RED


def test_transicion_red_a_green(fsm):
    """Test 2: Verifica la transición de RED a GREEN"""
    # Ejecutar la transición
    nuevo_estado = fsm.transition()
    
    # Verificar que el nuevo estado es GREEN
    assert nuevo_estado == TrafficLightState.GREEN
    assert fsm.state == TrafficLightState.GREEN


def test_ciclo_completo_a_red(fsm):
    """Test 3: Verifica que un ciclo completo regresa a RED"""
    # Ciclo: RED -> GREEN -> YELLOW -> RED
    fsm.transition()  # RED -> GREEN
    assert fsm.state == TrafficLightState.GREEN
    
    fsm.transition()  # GREEN -> YELLOW
    assert fsm.state == TrafficLightState.YELLOW
    
    fsm.transition()  # YELLOW -> RED
    assert fsm.state == TrafficLightState.RED


def test_conteo_de_ciclos(fsm):
    """Test 4: Verifica que el contador de ciclos se incrementa correctamente"""
    # Inicialmente debe ser 0
    assert fsm._cycle_count == 0
    
    # Primer ciclo: RED -> GREEN -> YELLOW -> RED
    fsm.transition()  # Ciclo 1
    assert fsm._cycle_count == 1
    
    fsm.transition()  # Ciclo 2
    assert fsm._cycle_count == 2
    
    fsm.transition()  # Ciclo 3
    assert fsm._cycle_count == 3
    
    # Después de 3 transiciones debe estar de nuevo en RED
    assert fsm.state == TrafficLightState.RED
