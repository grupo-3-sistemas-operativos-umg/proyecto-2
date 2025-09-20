import time                      # time.sleep para pausar entre unidades de simulación
from collections import deque    # deque para administrar la ready queue de manera eficiente

from Estrategias.ProcesoEstrategiaBase import ProcesoEstrategiaBase

# ---------- Constantes ----------
TIME_UNIT = 5  # cada unidad de tiempo de la simulación dura 5 segundos reales

class ServicioEmulador:
    """
    Ejecuta la simulación de procesos siguiendo la estrategia pasada (planificador).
    - La responsabilidad del planificador (strategy) es decidir el orden/prioridad
      sobre la lista de procesos listos (ready queue).
    - El emulador se encarga de:
        * gestionar arribos (llegadas) en el tiempo,
        * ejecutar decrementando `restante`,
        * rotar la cola para Round Robin (si planificador.rr == True),
        * registrar historial (tiempo de finalización),
        * notificar la UI mediante `update_ui_callback`.
    """

    def __init__(self, planificador: ProcesoEstrategiaBase, quantum=1):
        # planificador: instancia que implementa planificar(procesos, tiempo_actual)
        # quantum: tamaño del time-slice para Round Robin (en unidades de tiempo)
        self.planificador = planificador
        self.quantum = int(quantum)
        self.historial = []  # historial local de la ejecución actual: lista de (Proceso, tiempo_fin)

    def ejecutar(self, procesos, update_ui_callback):
        """
        Ejecuta la simulación hasta finalizar todos los procesos.
        - procesos: iterable de objetos `Proceso` (con atributos: pid, llegada, restante, etc.)
        - update_ui_callback: función (current, tiempo, cola_para_ui, historial) usada para actualizar la GUI.
          **IMPORTANTE**: esta función se llamará desde el hilo de simulación; en la implementación de la GUI
        """

        # limpiar historial de la ejecución actual
        self.historial = []

        # Ordenamos todos los procesos por tiempo de llegada para poder ir consumiendo arrivals de manera secuencial.
        # 'todos' mantiene la lista completa en orden de llegada; index_arrival nos dice cuántos ya pasamos a ready.
        todos = sorted(list(procesos), key=lambda p: p.llegada)

        tiempo = 0               # reloj de la simulación (unidades discretas)
        index_arrival = 0        # índice para recorrer 'todos' y mover procesos a ready cuando su arrival <= tiempo
        ready = deque()          # ready queue: deque para operaciones O(1) en popleft/append (útil para RR)
        finalizados = []         # lista de tuplas (Proceso, tiempo_final)
        current = None           # proceso actualmente en CPU (None si CPU idle)
        rr_slice = 0             # contador de unidades consumidas por el proceso actual en un slice de RR

        # función auxiliar para mover procesos cuya llegada <= tiempo a la ready queue
        def add_arrivals():
            """Añade a ready todos los procesos cuya llegada <= tiempo actual."""
            nonlocal index_arrival
            while index_arrival < len(todos) and todos[index_arrival].llegada <= tiempo:
                proc = todos[index_arrival]
                ready.append(proc)
                index_arrival += 1
                # NOTA: no removemos de 'todos' para facilitar comparaciones posteriores; usamos index_arrival como cursor.

        total = len(todos)
        if total == 0:
            # no hay procesos; notificar UI y salir
            update_ui_callback(None, tiempo, list(ready), list(self.historial))
            return

        # -------------------------
        # BUCLE PRINCIPAL DE LA SIMULACIÓN
        # -------------------------
        while len(finalizados) < total:
            add_arrivals()  # primero, incorporar nuevos arribos al tiempo actual

            # -------------------------
            # Preparar la representación de la cola que se mostrará en la UI.
            # - Si es Round Robin, mostramos la ready queue en su orden actual.
            # - Si no es RR, pedimos al planificador que nos devuelva la lista ordenada
            #   según la política (por ejemplo por llegada, por tiempo total, por restante, etc.)
            # -------------------------
            if self.planificador.rr:
                # RR no reordena: la cola debe conservar su orden FIFO para rotaciones
                cola_para_ui = list(ready)
            else:
                # Para otros algoritmos, el planificador define el orden de prioridad sobre los procesos listos
                cola_para_ui = self.planificador.planificar(list(ready), tiempo)

            # -------------------------
            # SELECCIÓN DEL PROCESO A EJECUTAR
            # -------------------------
            selected = None
            if self.planificador.rr:
                # Round Robin: el proceso a ejecutar es el que está al frente de ready (si existe)
                if ready:
                    selected = ready[0]
            elif self.planificador.preemptive:
                # Algoritmos expropiativos (ej. SRTF): siempre reevaluamos la cola y cogemos el primero
                # (puede ser distinto del current)
                cand_list = self.planificador.planificar(list(ready), tiempo)
                selected = cand_list[0] if cand_list else None
            else:
                # Algoritmos no expropiativos (ej. FCFS, SJF no preemptive):
                # si hay un proceso en CPU que aún no ha terminado, lo mantenemos (no se expropia).
                # sólo si CPU está idle o el current terminó, elegimos el siguiente según el planificador.
                if current is not None and current.restante > 0:
                    selected = current
                else:
                    cand_list = self.planificador.planificar(list(ready), tiempo)
                    selected = cand_list[0] if cand_list else None

            # -------------------------
            # Si no hay ningún proceso listo (CPU idle): avanzamos tiempo una unidad.
            # -------------------------
            if selected is None:
                # Notificamos UI (CPU idle)
                update_ui_callback(None, tiempo, cola_para_ui, list(self.historial))
                # avanzar el reloj y dormir el tiempo real correspondiente
                time.sleep(TIME_UNIT)
                tiempo += 1
                continue

            # -------------------------
            # Preparación específica de RR: reiniciar contador de slice cuando cambia el proceso.
            # -------------------------
            if self.planificador.rr:
                # Si entramos a ejecutar un nuevo proceso (diferente al current), reiniciamos rr_slice.
                if current is None or selected.pid != current.pid:
                    rr_slice = 0
                current = selected
            else:
                current = selected

            # -------------------------
            # EJECUCIÓN: consumimos exactamente UNA unidad de tiempo de CPU del proceso seleccionado
            # (esto permite preempción y llegadas entre unidades).
            # -------------------------
            current.restante -= 1   # le restamos 1 unidad de tiempo al proceso en CPU
            rr_slice += 1           # incrementamos contador de slice (si aplica RR)
            tiempo += 1             # avanzamos el reloj por 1 unidad

            # Notificamos la UI del estado tras ejecutar esta unidad.
            # - current: proceso que se ejecutó esta unidad (o None si idle)
            # - tiempo: tiempo actual (ya incrementado)
            # - cola: si RR -> lista(ready) (para mostrar orden), si no RR -> cola_para_ui (ordenado por planificador)
            # - historial: copia del historial hasta ahora (procesos finalizados)
            update_ui_callback(current, tiempo, list(ready) if self.planificador.rr else cola_para_ui,
                               list(self.historial))

            # Esperamos el tiempo real correspondiente a una unidad (para simular tiempo de reloj)
            time.sleep(TIME_UNIT)

            # -------------------------
            # PROCESO TERMINADO: si su restante llegó a 0, lo movemos a finalizados y al historial
            # -------------------------
            if current.restante <= 0:
                finalizados.append((current, tiempo))
                self.historial.append((current, tiempo))
                # intentamos eliminar current de ready (puede no estar si la implementación de selección lo sacó)
                try:
                    ready.remove(current)
                except ValueError:
                    # si no está en ready no hacemos nada (ya fue ejecutado sin estar en la cola visible)
                    pass
                # dejamos la CPU libre
                current = None
                rr_slice = 0
                # volvemos al inicio del bucle (se añadirán arrivals si existieran)
                continue

            # -------------------------
            # ROTACIÓN EN ROUND ROBIN
            # - Si el slice alcanzó el quantum, rotamos el primer elemento de ready al final.
            # - rr_slice se reinicia tras la rotación.
            # -------------------------
            if self.planificador.rr and rr_slice >= self.quantum:
                try:
                    first = ready.popleft()
                    ready.append(first)
                except IndexError:
                    # ready vacía (raro, pero protegemos contra excepciones)
                    pass
                rr_slice = 0

            # -------------------------
            # Después de ejecutar una unidad (y posiblemente rotar), incorporamos nuevos arrivals
            # que tengan llegada == tiempo actual (llegadas ocurridas «durante» esta unidad).
            # -------------------------
            add_arrivals()

        # -------------------------
        # Terminó la simulación: notificamos una última vez la UI con el historial completo.
        # -------------------------
        update_ui_callback(None, tiempo, [], list(self.historial))