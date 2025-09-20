from Estrategias.ProcesoEstrategiaBase import ProcesoEstrategiaBase

class RoundRobinEstrategia(ProcesoEstrategiaBase):
    preemptive = True
    rr = True

    def planificar(self, procesos, tiempo_actual):
        # Round Robin no necesita ordenar, devuelve la lista tal cual
        return procesos