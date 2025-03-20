import numpy as np
import matplotlib.pyplot as plt
import time
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def function(x):
    """Nueva función: f(x) = x^2 - 4x + 4"""
    return x**2 - 4*x + 4

def derivative(x):
    """Derivada de la función."""
    return 2*x - 4

def second_derivative(x):
    """Segunda derivada de la función."""
    return 2

def unidirectional_search(f, x0, alpha=0.01, tol=1e-5, max_iter=20):
    x = x0
    history = [x]
    for i in range(max_iter):
        grad = derivative(x)
        x_new = x - alpha * np.sign(grad)
        if abs(x_new - x) < tol:
            break
        x = x_new
        history.append(x)
    return x, f(x), i+1, history

def newton_method(f, x0, tol=1e-5, max_iter=20):
    x = x0
    history = [x]
    for i in range(max_iter):
        d1 = derivative(x)
        d2 = second_derivative(x)
        if d2 == 0:
            break
        x = x - d1 / d2
        history.append(x)
    return x, f(x), i+1, history

def gradient_descent(f, x0, alpha=0.01, tol=1e-5, max_iter=20):
    x = x0
    history = [x]
    for i in range(max_iter):
        grad = derivative(x)
        if np.abs(grad) > 1e6:
            break
        x = x - alpha * grad
        history.append(x)
        if abs(grad) < tol:
            break
    return x, f(x), i+1, history

def show_graph(method, history, f_min):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(history, label=f"{method} (f(x) = {f_min:.5f})")
    ax.set_xlabel("Iteraciones")
    ax.set_ylabel("Valor de x")
    ax.set_title(f"Convergencia de {method}")
    ax.legend()
    plt.show()

def run_methods():
    x0 = float(entry_x0.get())
    alpha = float(entry_alpha.get())
    results = {
        'Unidirectional Search': unidirectional_search(function, x0, alpha),
        'Newton\'s Method': newton_method(function, x0),
        'Gradient Descent': gradient_descent(function, x0, alpha)
    }
    fig, ax = plt.subplots(figsize=(8, 5))
    for method, result in results.items():
        ax.plot(result[3], label=f"{method} (f(x) = {result[1]:.5f})")
    ax.set_xlabel("Iteraciones")
    ax.set_ylabel("Valor de x")
    ax.set_title("Convergencia de los métodos")
    ax.legend()
    global canvas
    for widget in frame_graph.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=frame_graph)
    canvas.draw()
    canvas.get_tk_widget().pack()
    result_label.config(text=f"Resultados:\nUnidirectional Search: f(x)={results['Unidirectional Search'][1]:.5f}\nNewton's Method: f(x)={results['Newton\'s Method'][1]:.5f}\nGradient Descent: f(x)={results['Gradient Descent'][1]:.5f}")
    plt.show()

def show_explanation():
    explanation_window = tk.Toplevel(root)
    explanation_window.title("Explicación de la función")
    explanation_window.geometry("400x200")
    tk.Label(explanation_window, text="Función a optimizar: f(x) = x^2 - 4x + 4", font=("Roboto", 12)).pack(pady=20)
    tk.Label(explanation_window, text="La función tiene un mínimo en x=2", font=("Roboto", 12)).pack(pady=10)

def run_single_method(method):
    x0 = float(entry_x0.get())
    alpha = float(entry_alpha.get())
    if method == 'Unidirectional Search':
        x_min, f_min, _, history = unidirectional_search(function, x0, alpha)
    elif method == 'Newton\'s Method':
        x_min, f_min, _, history = newton_method(function, x0)
    elif method == 'Gradient Descent':
        x_min, f_min, _, history = gradient_descent(function, x0, alpha)
    show_graph(method, history, f_min)

root = tk.Tk()
root.title("Optimización en Tkinter")
root.geometry("800x600")

sidebar = tk.Frame(root, bg="#008080", width=220, padx=10, pady=20)
sidebar.pack(side="left", fill="y")

title_label = tk.Label(sidebar, text="Métodos", font=("Roboto", 16), fg="white", bg="#008080")
title_label.pack(pady=20)

tk.Button(sidebar, text="Explicación", font=("Roboto", 12), command=show_explanation).pack(pady=10, fill='x')
tk.Button(sidebar, text="Ejecutar todos", font=("Roboto", 12), command=run_methods).pack(pady=10, fill='x')
tk.Button(sidebar, text="Unidirectional Search", font=("Roboto", 12), command=lambda: run_single_method("Unidirectional Search")).pack(pady=10, fill='x')
tk.Button(sidebar, text="Newton's Method", font=("Roboto", 12), command=lambda: run_single_method("Newton's Method")).pack(pady=10, fill='x')
tk.Button(sidebar, text="Gradient Descent", font=("Roboto", 12), command=lambda: run_single_method("Gradient Descent")).pack(pady=10, fill='x')

frame_main = tk.Frame(root)
frame_main.pack(expand=True, fill="both")

frame_controls = tk.Frame(frame_main)
frame_controls.pack(pady=20)

tk.Label(frame_controls, text="Punto Inicial:", font=("Roboto", 12)).grid(row=0, column=0)
entry_x0 = tk.Entry(frame_controls)
entry_x0.grid(row=0, column=1)

tk.Label(frame_controls, text="Learning Rate:", font=("Roboto", 12)).grid(row=1, column=0)
entry_alpha = tk.Entry(frame_controls)
entry_alpha.grid(row=1, column=1)

result_label = tk.Label(frame_main, text="", font=("Roboto", 12))
result_label.pack()

frame_graph = tk.Frame(frame_main)
frame_graph.pack(expand=True, fill="both")

def on_closing():
    root.quit()
    root.destroy()
    exit()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
