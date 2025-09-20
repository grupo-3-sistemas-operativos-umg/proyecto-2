from Estrategias.ProcesoEstrategiaBase import ProcesoEstrategiaBase

"""
Devuelve la lista tal cual, porque Round Robin no prioriza.

El simulador se encarga de rotar la cola cada quantum.

Marca preemptive=True (sí puede interrumpir) y rr=True (usa quantum).
"""
class RoundRobinEstrategia(ProcesoEstrategiaBase):
    preemptive = True
    rr = True

    def planificar(self, procesos, tiempo_actual):
        # RR usa el orden actual de la ready queue; la simulación usará deque para rotar.
        return list(procesos)
