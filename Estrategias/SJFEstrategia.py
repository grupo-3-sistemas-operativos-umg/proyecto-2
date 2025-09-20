from Estrategias.ProcesoEstrategiaBase import ProcesoEstrategiaBase

"""
Ordena por el tiempo total de CPU que necesita cada proceso.

Siempre va primero el proceso más corto.

Tampoco interrumpe (preemptive=False).
"""
class SJFEstrategia(ProcesoEstrategiaBase):
    preemptive = False
    rr = False

    def planificar(self, procesos, tiempo_actual):
        # Shortest Job First (no expropiativo): por tiempo total requerido
        return sorted(procesos, key=lambda p: p.tiempo_cpu)
