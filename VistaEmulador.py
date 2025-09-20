from tkinter import ttk

from ControladorEmulador import ControladorEmulador

# ---------- Interfaz gráfica (App) ----------
class VistaEmulador(ControladorEmulador):

    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Planificación de Procesos")
        self.root.configure(bg="#1e1e1e")

        # lista de procesos (model)
        self.procesos = []
        # bandera para evitar ejecuciones concurrentes
        self.running = False

        # estilo ttk
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#1e1e1e", foreground="white")
        style.configure("TFrame", background="#1e1e1e")
        style.configure("TButton", background="#2d2d2d", foreground="white")
        style.map("TButton", background=[("active", "#444444")])
        style.configure("TEntry", fieldbackground="#2d2d2d", foreground="white")
        style.configure("TCombobox", fieldbackground="#2d2d2d", background="#2d2d2d", foreground="white")
        style.configure("Treeview", background="#2d2d2d", fieldbackground="#2d2d2d", foreground="white")
        style.map("Treeview", background=[("selected", "#444444")], foreground=[("selected", "white")])

        # ------------ Widgets ------------
        frame = ttk.Frame(root)
        frame.pack(pady=10)

        ttk.Label(frame, text="Nombre").grid(row=0, column=0, sticky="w")
        self.nombre_entry = ttk.Entry(frame)
        self.nombre_entry.grid(row=0, column=1)

        ttk.Label(frame, text="Tiempo CPU (unidades)").grid(row=1, column=0, sticky="w")
        self.tiempo_entry = ttk.Entry(frame)
        self.tiempo_entry.grid(row=1, column=1)

        ttk.Label(frame, text="Llegada (unidad)").grid(row=2, column=0, sticky="w")
        self.llegada_entry = ttk.Entry(frame)
        self.llegada_entry.grid(row=2, column=1)

        ttk.Label(frame, text="Quantum (RR)").grid(row=3, column=0, sticky="w")
        self.quantum_entry = ttk.Entry(frame)
        self.quantum_entry.grid(row=3, column=1)

        ttk.Button(frame, text="Agregar Proceso", command=self.agregar_proceso).grid(
            row=4, column=0, columnspan=2, pady=5
        )

        # tabla de procesos
        self.tree = ttk.Treeview(root, columns=("PID", "Nombre", "CPU", "Llegada", "Quantum"), show="headings", height=6)
        for col in ("PID", "Nombre", "CPU", "Llegada", "Quantum"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(pady=10, fill="x", padx=10)

        # algoritmo
        ttk.Label(root, text="Algoritmo:").pack()
        self.algoritmo = ttk.Combobox(root, values=["FCFS", "SJF", "SRTF", "Round Robin"], state="readonly")
        self.algoritmo.current(0)
        self.algoritmo.pack()

        # iniciar botón
        self.start_button = ttk.Button(root, text="Iniciar Simulación", command=self.iniciar_simulacion)
        self.start_button.pack(pady=5)

        # etiquetas de salida
        self.status_label = ttk.Label(root, text="Estado: inactivo")
        self.status_label.pack(pady=(8, 0))

        self.cola_label = ttk.Label(root, text="Cola de procesos:")
        self.cola_label.pack(pady=(10, 0))

        self.historial_label = ttk.Label(root, text="Historial:")
        self.historial_label.pack()