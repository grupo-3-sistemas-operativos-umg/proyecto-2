from abc import ABC, abstractmethod

# ---------- Estrategias (Interfaz + Implementaciones) ----------
class ProcesoEstrategiaBase(ABC):
    """
    Base para las estrategias.
    - preemptive: True si la estrategia puede quitar CPU a un proceso en ejecución
    - rr: True si es Round Robin (lo tratamos diferentemente en Simulador)
    """
    preemptive = False
    rr = False

    @abstractmethod
    def planificar(self, procesos, tiempo_actual):
        """Recibe una lista de procesos (ready) y devuelve una lista ordenada según la política."""
        pass