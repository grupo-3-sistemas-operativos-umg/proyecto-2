import tkinter as tk
from tkinter import messagebox
import threading
import traceback

from Proceso import Proceso
from ServicioEmulador import ServicioEmulador
from Estrategias.FCFSEstrategia import FCFSEstrategia
from Estrategias.RoundRobinEstrategia import RoundRobinEstrategia
from Estrategias.SJFEstrategia import SJFEstrategia
from Estrategias.SRTFEstrategia import SRTFEstrategia


class ControladorEmulador:
    """
    Controlador principal que conecta la GUI (Tkinter) con la lógica de simulación (ServicioEmulador).
    - Permite agregar procesos a la tabla.
    - Lanza la simulación en un hilo aparte.
    - Recibe las actualizaciones de simulación (tiempo, CPU, cola, historial) y las refleja en la UI.
    """

    # ---------- agregar proceso ----------
    def agregar_proceso(self):
        """
        Lee los datos de los Entry, valida, crea un Proceso y lo agrega a la lista interna y a la tabla.
        """
        try:
            nombre = self.nombre_entry.get().strip() or None
            tiempo_text = self.tiempo_entry.get().strip()
            llegada_text = self.llegada_entry.get().strip()
            quantum_text = self.quantum_entry.get().strip()

            # validaciones básicas
            if not tiempo_text or not llegada_text:
                raise ValueError("Tiempo CPU y Llegada son obligatorios")

            tiempo = int(tiempo_text)
            llegada = int(llegada_text)
            quantum = int(quantum_text) if quantum_text else 0

            if tiempo <= 0 or llegada < 0 or quantum < 0:
                raise ValueError("Valores negativos o cero inválidos para tiempos")

            # si no se dio nombre, generamos uno automático
            nombre_final = nombre or f"Proceso{len(self.procesos)+1}"
            p = Proceso(nombre_final, tiempo, llegada, quantum)

            # almacenar y mostrar en Treeview
            self.procesos.append(p)
            self.tree.insert("", "end", values=(p.pid, p.nombre, p.tiempo_cpu, p.llegada, p.quantum))

            # limpiar entradas de texto
            self.nombre_entry.delete(0, tk.END)
            self.tiempo_entry.delete(0, tk.END)
            self.llegada_entry.delete(0, tk.END)
            self.quantum_entry.delete(0, tk.END)

        except ValueError as e:
            # errores de validación mostrados en cuadro de diálogo
            messagebox.showerror("Error", f"Valores inválidos: {e}")

    # ---------- iniciar simulación ----------
    def iniciar_simulacion(self):
        """
        Inicia la simulación:
        - Verifica que no haya otra en curso.
        - Clona los procesos (para no alterar los que están en la tabla).
        - Elige la estrategia según el Combobox.
        - Arranca el simulador en un hilo separado para no congelar la GUI.
        """
        if self.running:
            messagebox.showinfo("Simulación en curso", "Ya hay una simulación en ejecución.")
            return

        if not self.procesos:
            messagebox.showwarning("Aviso", "Agrega procesos primero")
            return

        # clonar procesos, así la simulación consume copias
        procesos_copia = [
            Proceso(p.nombre, p.tiempo_cpu, p.llegada, p.quantum)
            for p in self.procesos
        ]

        # elegir estrategia
        algoritmo = self.algoritmo.get()
        if algoritmo == "FCFS":
            plan = FCFSEstrategia()
        elif algoritmo == "SJF":
            plan = SJFEstrategia()
        elif algoritmo == "SRTF":
            plan = SRTFEstrategia()
        else:
            plan = RoundRobinEstrategia()

        # quantum global para la simulación (si RR). Por defecto = 1
        quantum = int(self.quantum_entry.get()) if self.quantum_entry.get() else 1
        sim = ServicioEmulador(plan, quantum)

        # actualizar estado UI
        self.running = True
        self.start_button.state(["disabled"])          # deshabilitar botón iniciar
        self.status_label.config(text="Estado: ejecutando...")

        # función que corre la simulación en hilo aparte
        def run():
            try:
                sim.ejecutar(procesos_copia, self.update_ui)
            except Exception:
                # cualquier error lo mostramos con traceback
                tb = traceback.format_exc()
                print(tb)
                self.root.after(0, lambda: messagebox.showerror("Error en simulación", tb))
            finally:
                # al terminar (con éxito o error), reactivar botón y actualizar estado
                def finish():
                    self.running = False
                    self.start_button.state(["!disabled"])
                    self.status_label.config(text="Estado: inactivo")
                self.root.after(0, finish)

        # lanzar en hilo daemon para no bloquear GUI
        threading.Thread(target=run, daemon=True).start()

    # ---------- actualización UI ----------
    def update_ui(self, actual, tiempo, cola, finalizados):
        """
        Callback invocada por el ServicioEmulador en cada tick de la simulación.
        Se encarga de mostrar en la GUI:
        - tiempo actual
        - proceso en CPU
        - cola de listos
        - historial de finalizados
        """
        def _update():
            # texto CPU actual
            cpu_text = actual.nombre if actual else "CPU ociosa"
            self.status_label.config(text=f"Tiempo: {tiempo} | Ejecutando: {cpu_text}")

            # mostrar cola (solo nombres)
            self.cola_label.config(text=f"Cola de procesos: {[p.nombre for p in cola]}")

            # historial formateado: lista de procesos y tiempo en que terminaron
            historial_text = ", ".join([f"{p.nombre}(fin t={t})" for p, t in finalizados])
            self.historial_label.config(text=f"Historial: [{historial_text}]")

        # aseguramos que la actualización ocurra en el hilo principal de Tkinter
        self.root.after(0, _update)
