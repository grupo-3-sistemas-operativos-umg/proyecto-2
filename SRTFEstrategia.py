from Estrategias.ProcesoEstrategiaBase import ProcesoEstrategiaBase

class SRTFEstrategia(ProcesoEstrategiaBase):
    preemptive = True
    rr = False

    def planificar(self, procesos, tiempo_actual):
        # Ordena por tiempo restante (menor primero)
        return sorted(procesos, key=lambda p: p.restante)