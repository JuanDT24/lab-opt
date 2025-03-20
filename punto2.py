import tkinter as tk
from tkinter import ttk
import numpy as np
import random
import time
from scipy.sparse import csr_matrix, dok_matrix

# Nuestra Implementación de listas enlazadas
class Node:
    def __init__(self, data, row, col):
        self.data = data
        self.row = row
        self.col = col
        self.next = None

class Sparse:
    def __init__(self):
        self.head = None

    def insert(self, data, row, col):
        new_node = Node(data, row, col)
        new_node.next = self.head
        self.head = new_node

    def to_dict(self):
        sparse_dict = {}
        current = self.head
        while current:
            sparse_dict[(current.row, current.col)] = current.data
            current = current.next
        return sparse_dict

# Generar matriz dispersa
def generate_matrix(rows, cols, density):
    matrix = np.zeros((rows, cols))
    for i in range(rows):
        for j in range(cols):
            if random.random() < density:
                matrix[i][j] = random.randint(1, 100)
    return matrix

# Convertir matriz dispersa
def convert_to_sparse(matrix, method):
    if method == "Linked List":
        sparse = Sparse()
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if matrix[i][j] != 0:
                    sparse.insert(matrix[i][j], i, j)
        return sparse
    elif method == "CSR":
        return csr_matrix(matrix)
    elif method == "DOK":
        return dok_matrix(matrix)

# Sumar matrices dispersas
def add_matrices(mat1, mat2, method):
    start_time = time.time()
    if method == "Linked List":
        result = Sparse()
        dict1, dict2 = mat1.to_dict(), mat2.to_dict()
        for key in set(dict1.keys()).union(dict2.keys()):
            result.insert(dict1.get(key, 0) + dict2.get(key, 0), key[0], key[1])
    else:
        result = mat1 + mat2
    return result, time.time() - start_time

# Función para calcular
def calculate(method):
    rows, cols = int(entry_rows.get()), int(entry_cols.get())
    density = float(entry_density.get())

    mat1 = generate_matrix(rows, cols, density)
    mat2 = generate_matrix(rows, cols, density)
    sparse1 = convert_to_sparse(mat1, method)
    sparse2 = convert_to_sparse(mat2, method)

    _, elapsed_time = add_matrices(sparse1, sparse2, method)
    label_time.config(text=f"Tiempo: {elapsed_time:.6f} s")

# Interfaz gráfica
root = tk.Tk()
root.title("SPARSED")
root.geometry("600x400")
root.configure(bg='white')
root.option_add("*Font", "Roboto 12")

# Banner
banner = tk.Label(root, text="SPARSED", bg="#008080", fg="white", font=("Roboto", 20, "bold"))
banner.pack(fill=tk.X)

# Contenedor principal
main_frame = tk.Frame(root, bg="white")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Sidebar
sidebar = tk.Frame(main_frame, bg="#008080", width=150)
sidebar.pack(side=tk.LEFT, fill=tk.Y)

# Botones de métodos
methods = ["Linked List", "CSR", "DOK"]
for method in methods:
    btn = tk.Button(sidebar, text=method, font=("Roboto", 12), bg="#ffffff", fg="#008080",
                    command=lambda m=method: calculate(m))
    btn.pack(pady=10, padx=10, fill=tk.X)

# Contenedor derecho
right_frame = tk.Frame(main_frame, bg="white")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Inputs
entry_rows = ttk.Entry(right_frame)
entry_cols = ttk.Entry(right_frame)
entry_density = ttk.Entry(right_frame)

# Labels
tk.Label(right_frame, text="Filas:", bg="white").pack()
entry_rows.pack()
tk.Label(right_frame, text="Columnas:", bg="white").pack()
entry_cols.pack()
tk.Label(right_frame, text="Densidad:", bg="white").pack()
entry_density.pack()

# Resultado del tiempo
label_time = tk.Label(right_frame, text="Tiempo: 0.000000 s", bg="white", font=("Roboto", 14))
label_time.pack(pady=20)

root.mainloop()
