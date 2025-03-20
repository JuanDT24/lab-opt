import numpy as np
from scipy.optimize import linprog
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys

# Colores
COLOR_SIDEBAR = "#2E8B8B"  # Verde azulado
COLOR_SIDEBAR_BUTTON = "#39A0A0"  # Verde azulado más claro para botones
COLOR_SIDEBAR_BUTTON_HOVER = "#1D6363"  # Verde azulado más oscuro para hover
COLOR_FONDO = "#f0f0f0"
COLOR_BOTON = "#3ca3a3"
COLOR_TEXT_LIGHT = "#ffffff"
COLOR_TEXT_DARK = "#333333"

class OptimizacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Optimización Lineal - CONSTRUDTT")
        self.root.geometry("1200x700")
        self.root.configure(bg=COLOR_FONDO)

        # Intentar cargar la fuente Roboto
        self.cargar_fuente()

        # Variables para resultados y entradas
        self.punto_var = tk.StringVar()
        self.resultado_var = tk.StringVar()
        self.entrada_x = None
        self.entrada_y = None
        self.restriccion1_var = tk.StringVar(value="8")
        self.restriccion2_var = tk.StringVar(value="10")

        # Crear la interfaz
        self.crear_interfaz()

        # Mostrar la primera pantalla al inicio
        self.mostrar_problema()

    def cargar_fuente(self):
        # Intentar usar Roboto si está instalada en el sistema
        self.fuente_normal = "Roboto"
        self.fuente_negrita = "Roboto Bold"

        # Verificar disponibilidad de la fuente y usar alternativa si no está disponible
        if "roboto" not in tk.font.families(root=self.root):
            if sys.platform == "win32":  # Windows
                self.fuente_normal = "Segoe UI"
                self.fuente_negrita = "Segoe UI Bold"
            elif sys.platform == "darwin":  # macOS
                self.fuente_normal = "SF Pro Text"
                self.fuente_negrita = "SF Pro Text Bold"
            else:  # Linux y otros
                self.fuente_normal = "DejaVu Sans"
                self.fuente_negrita = "DejaVu Sans Bold"

    def crear_interfaz(self):
        # Crear un panel principal dividido en sidebar y contenido
        self.panel_principal = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashwidth=1, sashpad=0)
        self.panel_principal.pack(fill=tk.BOTH, expand=1)

        # Sidebar
        self.sidebar = tk.Frame(self.panel_principal, bg=COLOR_SIDEBAR, width=200)
        self.panel_principal.add(self.sidebar, width=200)

        # Contenido principal
        self.contenido = tk.Frame(self.panel_principal, bg=COLOR_FONDO)
        self.panel_principal.add(self.contenido, width=1000)

        # Elementos del sidebar
        titulo_sidebar = tk.Label(self.sidebar, text="CONSTRUDTT", font=(self.fuente_negrita, 16),
                                 bg=COLOR_SIDEBAR, fg=COLOR_TEXT_LIGHT, pady=20)
        titulo_sidebar.pack(fill=tk.X)

        # Frame para botones del sidebar (para poder agregar sombras y efectos)
        frame_btn_problema = tk.Frame(self.sidebar, bg=COLOR_SIDEBAR_BUTTON,
                                      highlightbackground="#1D6363", highlightthickness=1)
        frame_btn_problema.pack(fill=tk.X, pady=5, padx=10)

        # Botones del sidebar con efecto de sombreado
        btn_problema = tk.Button(frame_btn_problema, text="Problema", font=(self.fuente_normal, 12),
                                bg=COLOR_SIDEBAR_BUTTON, fg=COLOR_TEXT_LIGHT, bd=0,
                                activebackground=COLOR_SIDEBAR_BUTTON_HOVER, activeforeground=COLOR_TEXT_LIGHT,
                                command=self.mostrar_problema, pady=10, relief=tk.RAISED)
        btn_problema.pack(fill=tk.X)

        frame_btn_solucion = tk.Frame(self.sidebar, bg=COLOR_SIDEBAR_BUTTON,
                                     highlightbackground="#1D6363", highlightthickness=1)
        frame_btn_solucion.pack(fill=tk.X, pady=5, padx=10)

        btn_solucion = tk.Button(frame_btn_solucion, text="Solución", font=(self.fuente_normal, 12),
                                bg=COLOR_SIDEBAR_BUTTON, fg=COLOR_TEXT_LIGHT, bd=0,
                                activebackground=COLOR_SIDEBAR_BUTTON_HOVER, activeforeground=COLOR_TEXT_LIGHT,
                                command=self.mostrar_solucion, pady=10, relief=tk.RAISED)
        btn_solucion.pack(fill=tk.X)

        # Crear frames para cada vista (problema y solución)
        self.frame_problema = tk.Frame(self.contenido, bg=COLOR_FONDO)
        self.frame_solucion = tk.Frame(self.contenido, bg=COLOR_FONDO)

        # Preparar el contenido de cada vista
        self.preparar_vista_problema()
        self.preparar_vista_solucion()

    def preparar_vista_problema(self):
        # Título del problema
        titulo = tk.Label(self.frame_problema, text="Problema de Optimización",
                       font=(self.fuente_negrita, 20), bg=COLOR_FONDO, fg=COLOR_TEXT_DARK, pady=15)
        titulo.pack(fill=tk.X)

        # Frame con scroll para el texto del problema
        frame_scroll = tk.Frame(self.frame_problema, bg=COLOR_FONDO)
        frame_scroll.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Scrollbar
        scrollbar = tk.Scrollbar(frame_scroll)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Canvas para el scrolling
        canvas = tk.Canvas(frame_scroll, bg="white", yscrollcommand=scrollbar.set,
                          highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=canvas.yview)

        # Frame para el texto del problema dentro del canvas
        frame_texto = tk.Frame(canvas, bg="white", padx=20, pady=20)

        # Configuración del canvas para hacer scroll
        canvas.create_window((0, 0), window=frame_texto, anchor=tk.NW)

        # Descripción del problema con estilos
        tk.Label(frame_texto, text="Problema", font=(self.fuente_negrita, 16),
               bg="white", fg=COLOR_TEXT_DARK).pack(anchor=tk.W, pady=(0, 10))

        descripcion = """Una fábrica produce 2 tipos de materiales: cemento (litros) y ladrillos. La fábrica cuenta con 2 departamentos A y B los cuales producen los materiales que la empresa necesita. La empresa CONSTRUDTT desea encontrar el costo mínimo de producción de los materiales."""

        tk.Label(frame_texto, text=descripcion, font=(self.fuente_normal, 12), bg="white",
               fg=COLOR_TEXT_DARK, justify=tk.LEFT, wraplength=700).pack(anchor=tk.W, pady=(0, 15))

        tk.Label(frame_texto, text="Función objetivo", font=(self.fuente_negrita, 14),
               bg="white", fg=COLOR_TEXT_DARK).pack(anchor=tk.W, pady=(10, 5))

        tk.Label(frame_texto, text="f(x,y) = 5x + 4y", font=(self.fuente_normal, 12),
               bg="white", fg=COLOR_TEXT_DARK).pack(anchor=tk.W, pady=(0, 10))

        tk.Label(frame_texto, text="Donde:", font=(self.fuente_negrita, 12),
               bg="white", fg=COLOR_TEXT_DARK).pack(anchor=tk.W, pady=(0, 5))

        tk.Label(frame_texto, text="x = costo de producción por unidad de litros de cemento (miles de pesos)",
               font=(self.fuente_normal, 12), bg="white", fg=COLOR_TEXT_DARK, justify=tk.LEFT).pack(anchor=tk.W)

        tk.Label(frame_texto, text="y = costo de producción por unidad de kilo de ladrillo (miles de pesos)",
               font=(self.fuente_normal, 12), bg="white", fg=COLOR_TEXT_DARK, justify=tk.LEFT).pack(anchor=tk.W, pady=(0, 15))

        tk.Label(frame_texto, text="Restricciones", font=(self.fuente_negrita, 14),
               bg="white", fg=COLOR_TEXT_DARK).pack(anchor=tk.W, pady=(10, 5))

        restricciones = """Los departamentos realizan un análisis e informan a la empresa las siguientes condiciones de producción de los materiales:

1. El departamento A trabajará máximo 8 horas diarias, cada unidad de litros de cemento necesita 1 hora y cada unidad de ladrillo 1 hora.
   x + y ≤ 8

2. El departamento B trabajará máximo 10 horas diarias, con cada unidad de cemento tardando 2 horas y cada unidad de ladrillo tomando 1 hora.
   2x + y ≤ 10

3. Ambas variables deben ser al menos 1.
   x ≥ 1, y ≥ 1"""

        tk.Label(frame_texto, text=restricciones, font=(self.fuente_normal, 12), bg="white",
               fg=COLOR_TEXT_DARK, justify=tk.LEFT, wraplength=700).pack(anchor=tk.W, pady=(0, 10))

        # Botón para ir a la solución
        btn_ver_solucion = tk.Button(frame_texto, text="Ver Solución", font=(self.fuente_negrita, 12),
                                   bg=COLOR_BOTON, fg=COLOR_TEXT_LIGHT, padx=20, pady=10,
                                   command=self.mostrar_solucion)
        btn_ver_solucion.pack(pady=20)

        # Actualizar las dimensiones del canvas después de añadir todos los widgets
        frame_texto.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def preparar_vista_solucion(self):
        # Título de la solución
        titulo = tk.Label(self.frame_solucion, text="Solución del Problema",
                       font=(self.fuente_negrita, 20), bg=COLOR_FONDO, fg=COLOR_TEXT_DARK, pady=15)
        titulo.pack(fill=tk.X)

        # Frame para gráfica
        self.frame_grafica = tk.Frame(self.frame_solucion, bg="white", highlightbackground="#cccccc",
                                    highlightthickness=1)
        self.frame_grafica.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Frame para controles y resultados
        frame_controles = tk.Frame(self.frame_solucion, bg=COLOR_FONDO, pady=10)
        frame_controles.pack(fill=tk.X, padx=20, pady=(0, 10))

        # Configuración de columnas
        for i in range(5):
            frame_controles.columnconfigure(i, weight=1)

        # Etiquetas y entradas para punto (x,y)
        tk.Label(frame_controles, text="x:", font=(self.fuente_normal, 12), bg=COLOR_FONDO).grid(row=0, column=0, padx=5, pady=5)
        self.entrada_x = tk.Entry(frame_controles, width=8, font=(self.fuente_normal, 12))
        self.entrada_x.grid(row=0, column=1, padx=5, pady=5)
        self.entrada_x.insert(0, "3")

        tk.Label(frame_controles, text="y:", font=(self.fuente_normal, 12), bg=COLOR_FONDO).grid(row=0, column=2, padx=5, pady=5)
        self.entrada_y = tk.Entry(frame_controles, width=8, font=(self.fuente_normal, 12))
        self.entrada_y.grid(row=0, column=3, padx=5, pady=5)
        self.entrada_y.insert(0, "4")

        # Botón para calcular el valor en punto
        btn_calcular = tk.Button(frame_controles, text="Calcular valor en punto", font=(self.fuente_normal, 10),
                              bg=COLOR_BOTON, fg=COLOR_TEXT_LIGHT, relief=tk.RAISED,
                              command=self.calcular_punto)
        btn_calcular.grid(row=0, column=4, padx=10, pady=5)

        # Nuevos campos para modificar restricciones
        tk.Label(frame_controles, text="Restricción 1 (x + y ≤):", font=(self.fuente_normal, 12), bg=COLOR_FONDO).grid(row=1, column=0, padx=5, pady=5, columnspan=2, sticky="e")
        entrada_restriccion1 = tk.Entry(frame_controles, width=8, font=(self.fuente_normal, 12), textvariable=self.restriccion1_var)
        entrada_restriccion1.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        tk.Label(frame_controles, text="Restricción 2 (2x + y ≤):", font=(self.fuente_normal, 12), bg=COLOR_FONDO).grid(row=2, column=0, padx=5, pady=5, columnspan=2, sticky="e")
        entrada_restriccion2 = tk.Entry(frame_controles, width=8, font=(self.fuente_normal, 12), textvariable=self.restriccion2_var)
        entrada_restriccion2.grid(row=2, column=2, padx=5, pady=5, sticky="w")

        # Botón para actualizar restricciones
        btn_actualizar = tk.Button(frame_controles, text="Actualizar restricciones", font=(self.fuente_normal, 10),
                                bg=COLOR_BOTON, fg=COLOR_TEXT_LIGHT, relief=tk.RAISED,
                                command=self.resolver_optimizacion)
        btn_actualizar.grid(row=1, column=4, rowspan=2, padx=10, pady=5)

        # Frame para resultados
        frame_resultados = tk.Frame(self.frame_solucion, bg="white", padx=20, pady=15,
                                  highlightbackground="#cccccc", highlightthickness=1)
        frame_resultados.pack(fill=tk.X, padx=20, pady=(0, 10))

        # Etiquetas para mostrar resultados
        tk.Label(frame_resultados, textvariable=self.punto_var, font=(self.fuente_normal, 12),
               bg="white", fg=COLOR_TEXT_DARK).pack(side=tk.TOP, anchor="w", pady=5)

        tk.Label(frame_resultados, textvariable=self.resultado_var, font=(self.fuente_negrita, 12),
               bg="white", fg=COLOR_TEXT_DARK).pack(side=tk.TOP, anchor="w", pady=5)

        # Botón para resolver con efecto de sombreado
        frame_btn_resolver = tk.Frame(self.frame_solucion, bg=COLOR_BOTON,
                                    highlightbackground="#2a7070", highlightthickness=1)
        frame_btn_resolver.pack(pady=10)

        btn_resolver = tk.Button(frame_btn_resolver, text="Resolver Optimización", font=(self.fuente_negrita, 12),
                               bg=COLOR_BOTON, fg=COLOR_TEXT_LIGHT, padx=20, pady=10, bd=0,
                               activebackground="#2a7070", activeforeground=COLOR_TEXT_LIGHT,
                               relief=tk.RAISED, command=self.resolver_optimizacion)
        btn_resolver.pack()

    def mostrar_problema(self):
        # Ocultar la vista de solución y mostrar la vista de problema
        self.frame_solucion.pack_forget()
        self.frame_problema.pack(fill=tk.BOTH, expand=True)

    def mostrar_solucion(self):
        # Ocultar la vista de problema y mostrar la vista de solución
        self.frame_problema.pack_forget()
        self.frame_solucion.pack(fill=tk.BOTH, expand=True)

        # Resolver optimización al mostrar la solución por primera vez
        if not self.resultado_var.get():
            self.resolver_optimizacion()

    def resolver_optimizacion(self):
        try:
            # Obtener valores de restricciones
            restriccion1 = float(self.restriccion1_var.get())
            restriccion2 = float(self.restriccion2_var.get())

            c = [-5, -4]  # Negativos porque linprog minimiza por defecto
            A = [[1, 1], [2, 1]]  # Restricciones
            b = [restriccion1, restriccion2]
            x_bounds = (1, None)
            y_bounds = (1, None)

            result = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

            if result.success:
                x_opt, y_opt = result.x
                valor_optimo = -result.fun

                # Actualizar los resultados en la interfaz
                self.resultado_var.set(f"Solución óptima: x = {x_opt:.2f}, y = {y_opt:.2f}, Valor óptimo: {valor_optimo:.2f}")

                # Graficar con la solución óptima
                self.graficar_region_factible(x_opt, y_opt, restriccion1, restriccion2)
            else:
                self.resultado_var.set("Error: No se encontró una solución óptima.")
        except ValueError:
            self.resultado_var.set("Error: Ingrese valores numéricos válidos para las restricciones")

    def calcular_punto(self):
        try:
            x = float(self.entrada_x.get())
            y = float(self.entrada_y.get())

            # Ya no verificamos si el punto está en la región factible
            valor = 5*x + 4*y
            self.punto_var.set(f"Valor en el punto (x={x:.2f}, y={y:.2f}): {valor:.2f}")

            # Actualizar la gráfica para mostrar el punto ingresado
            self.graficar_region_factible_con_punto(x, y)
        except ValueError:
            self.punto_var.set("Error: Ingrese valores numéricos válidos")

    def graficar_region_factible_con_punto(self, x_usuario=None, y_usuario=None):
        try:
            # Obtener valores de restricciones
            restriccion1 = float(self.restriccion1_var.get())
            restriccion2 = float(self.restriccion2_var.get())

            # Resolver para obtener el punto óptimo
            c = [-5, -4]
            A = [[1, 1], [2, 1]]
            b = [restriccion1, restriccion2]
            x_bounds = (1, None)
            y_bounds = (1, None)

            result = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

            if result.success:
                x_opt, y_opt = result.x
                self.graficar_region_factible(x_opt, y_opt, restriccion1, restriccion2, x_usuario, y_usuario)
        except ValueError:
            self.punto_var.set("Error: Ingrese valores numéricos válidos para las restricciones")

    def graficar_region_factible(self, x_opt, y_opt, restriccion1=8, restriccion2=10, x_usuario=None, y_usuario=None):
        # Limpiar el área de la gráfica anterior
        for widget in self.frame_grafica.winfo_children():
            widget.destroy()

        # Crear una figura de matplotlib
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Definir los datos para la gráfica con las restricciones actualizadas
        x = np.linspace(1, max(5, restriccion1, restriccion2/2), 400)
        y1 = restriccion1 - x  # x + y <= restriccion1
        y2 = restriccion2 - 2*x  # 2x + y <= restriccion2

        # Graficar las restricciones
        ax.plot(x, y1, label=f'$x + y \leq {restriccion1}$')
        ax.plot(x, y2, label=f'$2x + y \leq {restriccion2}$')
        ax.fill_between(x, np.maximum(1, np.minimum(y1, y2)), 1, where=(x >= 1) & (np.minimum(y1, y2) >= 1), color='#a8d0d0', alpha=0.5)

        # Marcar la solución óptima
        ax.plot(x_opt, y_opt, 'ro', label='Solución óptima')

        # Marcar el punto del usuario si existe
        if x_usuario is not None and y_usuario is not None:
            ax.plot(x_usuario, y_usuario, 'go', label='Punto usuario')

        # Ajustar límites de la gráfica basados en las restricciones
        max_x = max(5, restriccion1, restriccion2/2) + 1
        max_y = max(5, restriccion1, restriccion2) + 1

        # Configuraciones de la gráfica
        ax.set_xlim((1, max_x))
        ax.set_ylim((1, max_y))
        ax.set_xlabel('x (costo unidad cemento)', fontsize=10)
        ax.set_ylabel('y (costo unidad ladrillo)', fontsize=10)
        ax.legend()
        ax.set_title('Región factible y solución óptima')
        ax.grid(True, linestyle='--', alpha=0.7)

        # Incrustar la gráfica en el frame de Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafica)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


root = tk.Tk()
app = OptimizacionApp(root)
root.mainloop()
def on_closing():
    root.quit()
    root.destroy()
    exit()

root.protocol("WM_DELETE_WINDOW", on_closing)
