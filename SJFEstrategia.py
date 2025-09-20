from Estrategias.ProcesoEstrategiaBase import ProcesoEstrategiaBase

class SJFEstrategia(ProcesoEstrategiaBase):
    preemptive = False
    rr = False

    def planificar(self, procesos, tiempo_actual):
        # Ordena por tiempo de CPU (menor primero)
        return sorted(procesos, key=lambda p: p.tiempo_cpu)