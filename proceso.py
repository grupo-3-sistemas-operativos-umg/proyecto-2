import itertools

# ---------- Modelo Proceso ----------
class Proceso:
    """Representa un proceso del sistema."""
    _id_counter = itertools.count(1)

    def __init__(self, nombre, tiempo_cpu, llegada, quantum=0):
        self.pid = next(self._id_counter)     # PID autogenerado
        self.nombre = str(nombre)
        self.tiempo_cpu = int(tiempo_cpu)     # tiempo total requerido (unidades)
        self.restante = int(tiempo_cpu)       # unidades restantes por ejecutar
        self.llegada = int(llegada)           # instante de llegada (unidad)
        self.quantum = int(quantum)           # campo informativo (si aplica)

    def __repr__(self):
        return f"P{self.pid}({self.nombre}, t={self.tiempo_cpu}, l={self.llegada})"