
# Instrucciones

1. Clonar este repositorio
2. Ejecutar el archivo main.py (usando el comando python main.py o python3 main.py)

# Demostración de uso


# Manual de usuario

Este proyecto simula cómo un sistema operativo gestiona varios procesos usando distintos algoritmos de planificación:

* FCFS (First Come, First Served) → El primero que llega es el primero en ejecutarse.

* SJF (Shortest Job First) → El proceso con menor tiempo requerido se ejecuta primero.

* SRTF (Shortest Remaining Time First) → Variante expropiativa de SJF, siempre se ejecuta el que tenga menos tiempo restante.

* Round Robin → Cada proceso obtiene un turno de CPU con duración igual al quantum. Cuando se le acaba, si aún no terminó, vuelve a la cola.

El programa automatiza el trabajo del planificador: recibe procesos como entrada, aplica el algoritmo elegido y  muestra cómo se van ejecutando hasta que todos terminan.

## ¿Cómo interpretar la interfaz gráfica (UI)?

### Formulario de entrada (Nombre, Tiempo CPU, Llegada, Quantum)

Aquí se define los procesos:

* Nombre: identificador que eliges (ej. “P1”).

* Tiempo CPU: cuántas unidades de tiempo necesita.

* Llegada: en qué instante “entra” al sistema.

* Quantum: solo relevante si se usa Round Robin.

### Tabla de procesos

Lista todos los procesos que agregaste, mostrando su PID, nombre, tiempo, llegada y quantum.

### Selector de Algoritmo

Permite elegir qué estrategia de planificación aplicar.

### Botón “Iniciar Simulación”
Lanza la simulación en tiempo real. Cada unidad de tiempo equivale a 5 segundos reales, por lo que verás la ejecución avanzar poco a poco.

### Cola de procesos
Muestra qué procesos están esperando en la cola listos para ejecutarse (ordenados según el algoritmo).

### Historial
Registra los procesos que ya terminaron, indicando el instante en el que finalizaron.

## ¿Cómo interpretar los resultados?

* Si se elige FCFS, la cola se respeta según el orden de llegada.

* Si se elige SJF, los procesos cortos terminan antes que los largos.

* Si se elige SRTF, un proceso corto puede interrumpir a otro más largo en ejecución.

* Si se elige Round Robin, los procesos se “reparten” la CPU en turnos.

## Estructura / Arquitectura

📂 main.py

Rol: Es el punto de entrada del programa.

Crea la ventana principal de Tkinter (root) e inicializa la clase VistaEmulador.

Únicamente arranca la aplicación, no contiene lógica de simulación.

👉 Es el “encendedor” que enciende todo el simulador.

📂 VistaEmulador.py

Rol: Es la interfaz gráfica (UI) de la aplicación.

Aquí se crean los widgets:

Entradas de texto (para nombre, tiempo de CPU, llegada, quantum).

Tabla (Treeview) para mostrar los procesos.

Combobox para elegir el algoritmo.

Botón para iniciar la simulación.

Labels que muestran el estado, la cola de procesos y el historial.

Hereda de ControladorEmulador, lo que le da acceso a la lógica de control (agregar procesos, iniciar simulación, actualizar UI).

👉 Es la cara visible del simulador.

📂 ControladorEmulador.py

Rol: Es el cerebro que conecta la vista con el motor de simulación.

Funciones principales:

agregar_proceso: valida los datos introducidos, crea un objeto Proceso y lo añade a la lista y a la tabla.

iniciar_simulacion: selecciona el algoritmo, crea una copia de los procesos y lanza la simulación en un hilo aparte para no congelar la interfaz.

update_ui: recibe las actualizaciones del motor (ServicioEmulador) y refresca la interfaz (proceso en ejecución, cola de listos, historial).

👉 Es el puente entre la interfaz gráfica y la lógica de planificación.

📂 Proceso.py

Rol: Define el modelo de datos Proceso.

Cada proceso tiene:

pid: identificador único.

nombre: etiqueta (ej. "p1").

tiempo_cpu: tiempo total requerido.

restante: tiempo restante por ejecutar.

llegada: instante de llegada.

quantum: quantum asignado (si aplica).

👉 Es el objeto que representa un proceso real en la simulación.

📂 ServicioEmulador.py

Rol: Es el motor de la simulación.

Ejecuta los procesos paso a paso y aplica el algoritmo de planificación.

Características:

Usa un bucle de tiempo discreto (tiempo que aumenta de 1 en 1).

Administra la cola de listos (ready).

Soporta algoritmos con o sin desalojo y Round Robin.

Llama a update_ui_callback para mantener sincronizada la interfaz.

Mantiene un historial de procesos terminados con su tiempo final.

👉 Es el núcleo que simula la CPU.

📂 Estrategias/

Este directorio contiene los algoritmos de planificación. Cada uno implementa cómo ordenar o elegir procesos de la cola.

ProcesoEstrategiaBase.py: clase base para todas las estrategias (define si son preventivas o usan RR).

FCFSEstrategia.py: primero en llegar, primero en ser atendido.

SJFEstrategia.py: selecciona el proceso más corto (sin desalojo).

SRTFEstrategia.py: selecciona el más corto restante (con desalojo).

RoundRobinEstrategia.py: rota procesos con quantum fijo.

👉 Aquí están las reglas del juego que decide cómo la CPU asigna el tiempo.

🔗 Resumen de conexiones:

main.py → inicia la interfaz (VistaEmulador).

VistaEmulador → muestra UI y hereda de ControladorEmulador.

ControladorEmulador → gestiona acciones de usuario y lanza ServicioEmulador.

ServicioEmulador → ejecuta la simulación aplicando una Estrategia sobre los Procesos.

Proceso.py → define los procesos que todos los módulos manipulan.

```text
                ┌─────────────┐
                │   main.py   │
                │ (punto de   │
                │   entrada)  │
                └──────┬──────┘
                       │
                       ▼
           ┌─────────────────────┐
           │  VistaEmulador.py   │
           │ (interfaz gráfica)  │
           └──────┬──────────────┘
                  │  hereda
                  ▼
    ┌──────────────────────────────┐
    │ ControladorEmulador.py       │
    │ (gestiona UI y lanza motor)  │
    └──────┬───────────────────────┘
           │ llama
           ▼
 ┌─────────────────────────┐
 │ ServicioEmulador.py     │
 │ (motor de simulación)   │
 └───────┬────────────────┘
         │ usa
         ▼
 ┌─────────────────────────┐
 │ Estrategias/            │
 │ (FCFS, SJF, SRTF, RR)   │
 └─────────────────────────┘

 ┌─────────────────────────┐
 │ Proceso.py      │
 │ (datos del proceso)     │
 └─────────────────────────┘


### Demostración:

