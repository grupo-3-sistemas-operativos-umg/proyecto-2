from Estrategias.ProcesoEstrategiaBase import ProcesoEstrategiaBase

"""
Ordena por el tiempo restante de ejecución.

Si llega un proceso más corto, puede interrumpir al actual (preemptive=True).
"""
class SRTFEstrategia(ProcesoEstrategiaBase):
    preemptive = True
    rr = False

    def planificar(self, procesos, tiempo_actual):
        # Shortest Remaining Time First (expropiativo): por restante
        return sorted(procesos, key=lambda p: p.restante)
