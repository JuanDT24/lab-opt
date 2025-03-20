import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp

# Inicialización del símbolo
x = sp.symbols('x')

# Diccionario de funciones disponibles (usando funciones de sympy)
FUNCIONES = {
    "sen(x)": sp.sin(x),
    "cos(x)": sp.cos(x),
    "exp(x)": sp.exp(x),
    "ln(1+x)": sp.log(1+x),
    "arctan(x)": sp.atan(x)
}

# Función para calcular el polinomio de Taylor de f en el punto a usando n términos
def calcular_taylor(f, a, n):
    taylor = 0
    for k in range(n):
        derivada = sp.diff(f, x, k)
        valor_derivada = derivada.subs(x, a)
        termino = (valor_derivada / sp.factorial(k)) * (x - a)**k
        taylor += termino
    return sp.simplify(taylor)

# Función para guardar el historial
def guardar_historial(funcion, terminos, punto, x_eval, valor_teorico, valor_experimental, err_abs, err_rel):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    registro = f"{ahora} | {funcion} | {terminos} términos | a={punto} | x={x_eval} | f(x)={valor_teorico} | T(x)={valor_experimental} | Error Abs={err_abs} | Error Rel={err_rel}\n"
    historial_text.insert(tk.END, registro)
    historial_text.see(tk.END)
    with open("historial.txt", "a", encoding="utf-8") as f_hist:
        f_hist.write(registro)

# Función para graficar y evaluar la serie de Taylor
def graficar():
    ax.clear()
    funcion_seleccionada = combo_funcion.get()
    num_terminos_str = entry_terminos.get()
    punto_expansion_str = entry_punto.get()

    try:
        n_terminos = int(num_terminos_str)
        if n_terminos < 1:
            raise ValueError("El número de términos debe ser mayor o igual a 1.")
    except ValueError:
        messagebox.showerror("Error", "Número de términos inválido.")
        return

    try:
        a = float(punto_expansion_str)
    except ValueError:
        messagebox.showerror("Error", "Punto de expansión inválido.")
        return

    f = FUNCIONES.get(funcion_seleccionada)
    f_taylor = calcular_taylor(f, a, n_terminos)
    f_lambdified = sp.lambdify(x, f, modules=["numpy"])
    taylor_lambdified = sp.lambdify(x, f_taylor, modules=["numpy"])

    x_vals = np.linspace(a - 5, a + 5, 400)
    y_original = f_lambdified(x_vals)
    y_taylor = taylor_lambdified(x_vals)

    ax.plot(x_vals, y_original, label=f"Función: {funcion_seleccionada}")
    ax.plot(x_vals, y_taylor, linestyle="--", label=f"Taylor ({n_terminos} términos, a={a})")
    ax.legend()
    canvas.draw()

    x_eval = a + 1
    valor_teorico = f_lambdified(x_eval)
    valor_experimental = taylor_lambdified(x_eval)
    error_absoluto = abs(valor_teorico - valor_experimental)
    error_relativo = (error_absoluto / abs(valor_teorico)) * 100 if valor_teorico != 0 else float('inf')

    label_valor_teorico.config(text=f"Valor Teórico f({x_eval}) = {valor_teorico}")
    label_valor_experimental.config(text=f"Valor Experimental T({x_eval}) = {valor_experimental}")
    label_error_absoluto.config(text=f"Error Absoluto: {error_absoluto}")
    label_error_relativo.config(text=f"Error Relativo: {error_relativo:.5f}%")

    guardar_historial(funcion_seleccionada, n_terminos, a, x_eval, valor_teorico, valor_experimental, error_absoluto, error_relativo)

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Expansión en Series de Taylor")
root.geometry("900x770")

frame_controls = tk.Frame(root)
frame_controls.pack(pady=10)

ttk.Label(frame_controls, text="Función:").grid(row=0, column=0, padx=5)
combo_funcion = ttk.Combobox(frame_controls, values=list(FUNCIONES.keys()), state="readonly")
combo_funcion.grid(row=0, column=1)
combo_funcion.current(0)

ttk.Label(frame_controls, text="Cantidad de términos:").grid(row=0, column=2, padx=5)
entry_terminos = tk.Entry(frame_controls, width=10)
entry_terminos.grid(row=0, column=3)
entry_terminos.insert(0, "5")

ttk.Label(frame_controls, text="Punto de expansión:").grid(row=0, column=4, padx=5)
entry_punto = tk.Entry(frame_controls, width=10)
entry_punto.grid(row=0, column=5)
entry_punto.insert(0, "0")

btn_graficar = tk.Button(frame_controls, text="Graficar", command=graficar)
btn_graficar.grid(row=0, column=6, padx=10)

frame_grafico = tk.Frame(root)
frame_grafico.pack()
fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
canvas.get_tk_widget().pack()

frame_resultados = tk.Frame(root)
frame_resultados.pack()
label_valor_teorico = tk.Label(frame_resultados, text="Valor Teórico: ")
label_valor_teorico.pack()
label_valor_experimental = tk.Label(frame_resultados, text="Valor Experimental: ")
label_valor_experimental.pack()
label_error_absoluto = tk.Label(frame_resultados, text="Error Absoluto: ")
label_error_absoluto.pack()
label_error_relativo = tk.Label(frame_resultados, text="Error Relativo: ")
label_error_relativo.pack()

frame_historial = tk.Frame(root)
frame_historial.pack()
label_historial = tk.Label(frame_historial, text="Historial:")
label_historial.pack()
historial_text = tk.Text(frame_historial, width=50, height=10)
historial_text.pack()


def on_closing():
    root.quit()
    root.destroy()
    exit()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
