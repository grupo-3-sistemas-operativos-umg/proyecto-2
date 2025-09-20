from Estrategias.ProcesoEstrategiaBase import ProcesoEstrategiaBase

"""
Devuelve los procesos ordenados por el instante de llegada.

Así se asegura que siempre vaya primero el que entró antes.

preemptive=False, porque nunca interrumpe.
"""
class FCFSEstrategia(ProcesoEstrategiaBase):
    preemptive = False
    rr = False

    def planificar(self, procesos, tiempo_actual):
        # Shortest Job First (no expropiativo): por tiempo total requerido
        return sorted(procesos, key=lambda p: p.tiempo_cpu)