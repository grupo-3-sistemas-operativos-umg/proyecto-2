class Proceso:
    def __init__(self, pid, nombre, tiempo_cpu, llegada, quantum=0):
        self.pid = pid  # identificador único
        self.nombre = nombre  # etiqueta (ej. "p1")
        self.tiempo_cpu = tiempo_cpu  # tiempo total requerido
        self.restante = tiempo_cpu  # tiempo restante por ejecutar
        self.llegada = llegada  # instante de llegada
        self.quantum = quantum  # quantum asignado (si aplica)
        self.estado = 'Nuevo'  # estado inicial

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado

    def __str__(self):
        return (f"PID: {self.pid}, Nombre: {self.nombre}, Estado: {self.estado}, "
                f"Tiempo CPU: {self.tiempo_cpu}, Restante: {self.restante}, "
                f"Llegada:{self.llegada}, Quantum: {self.quantum}")