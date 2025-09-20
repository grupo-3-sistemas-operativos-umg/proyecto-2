from Estrategias.ProcesoEstrategiaBase import ProcesoEstrategiaBase

class FCFSEstrategia(ProcesoEstrategiaBase):
    preemptive = False
    rr = False

    def planificar(self, procesos, tiempo_actual):
        # Ordena por tiempo de llegada (menor primero)
        return sorted(procesos, key=lambda p: p.llegada)