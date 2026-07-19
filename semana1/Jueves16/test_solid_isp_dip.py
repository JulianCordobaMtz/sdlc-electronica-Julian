import pytest

# MOCKS SIMULADOS PARA PRUEBAS
# --- Mocks para ISP (Segregación de Interfaces) ---
class SensorMultifuncionMalo:
    """Simula un hardware obligado a tener métodos que no usa."""
    def leer_temperatura(self):
        return 25.5
    
    def leer_humedad(self):
        raise NotImplementedError("Hardware de temperatura no soporta humedad")

class SensorSoloTemperaturaBueno:
    """Simula un hardware con una interfaz limpia y segregada."""
    def leer_temperatura(self):
        return 25.5


# --- Mocks para DIP (Inversión de Dependencias) ---
class AbstraccionSensor:
    """Interfaz abstracta que los módulos de bajo nivel deben respetar."""
    def leer_dato(self):
        pass

class SensorHumedadI2C(AbstraccionSensor):
    """Módulo de bajo nivel (Detalle)."""
    def leer_dato(self):
        return 60.0

class ControladorCentralBueno:
    """Módulo de alto nivel que depende de la abstracción, no del hardware."""
    def __init__(self, sensor: AbstraccionSensor):
        self.sensor = sensor

    def obtener_reporte(self):
        return f"Lectura obtenida: {self.sensor.leer_dato()}"


# ==========================================
# TESTS: SEGREGACIÓN DE INTERFACES (ISP)
# ==========================================

def test_isp_mal_diseno_lanza_error():
    """
    Prueba 1: Demuestra que al tener una interfaz sobrecargada, 
    intentar acceder a una función que el sensor físico no soporta 
    hace colapsar el programa.
    """
    sensor_rigido = SensorMultifuncionMalo()
    
    # Verificamos que el mal diseño genera un error crítico
    with pytest.raises(NotImplementedError):
        sensor_rigido.leer_humedad()

def test_isp_buen_diseno_lectura_limpia():
    """
    Prueba 2: Demuestra que un sensor con una interfaz segregada 
    (solo lo que necesita) funciona de manera predecible y segura.
    """
    sensor_limpio = SensorSoloTemperaturaBueno()
    
    assert sensor_limpio.leer_temperatura() == 25.5

# TESTS: INVERSIÓN DE DEPENDENCIAS (DIP)
def test_dip_mal_diseno_acoplamiento():
    """
    Prueba 3: En un mal diseño, el controlador crearía el sensor 
    directamente en su interior (ej. self.sensor = SensorI2C()).
    Esto hace imposible inyectar simulaciones para pruebas.
    """
    # Al no poder inyectar dependencias, un controlador mal diseñado
    # fallaría al intentar probarse sin el hardware real conectado.
    pass

def test_dip_buen_diseno_inyeccion_exitosa():
    """
    Prueba 4: Demuestra cómo el principio DIP permite inyectar 
    cualquier sensor (incluso simulado) al controlador central,
    siempre que respete la interfaz 'AbstraccionSensor'.
    """
    # Inyectamos nuestra simulación al controlador
    sensor_mock = SensorHumedadI2C()
    microcontrolador = ControladorCentralBueno(sensor=sensor_mock)
    
    # El microcontrolador lee el dato sin saber qué hardware físico hay detrás
    reporte = microcontrolador.obtener_reporte()
    
    assert reporte == "Lectura obtenida: 60.0"