import tkinter as tk
from tkinter import ttk, messagebox

def mcd(a, b):
    if b > a:
        a, b = b, a
    pasos = []
    while b != 0:
        cociente = a // b
        residuo = a % b
        pasos.append((a, b, cociente, residuo))
        a, b = b, residuo
    return a, pasos


def calcular_mcd(numeros_entry, resultado_text):
    try:
        numeros = [int(x.strip()) for x in numeros_entry.get().split(",") if x.strip()]
        if len(numeros) < 2:
            messagebox.showwarning("Error", "Debes ingresar al menos dos números separados por comas.")
            return

        resultado = numeros[0]
        resultado_text.config(state="normal")
        resultado_text.delete("1.0", tk.END)
        resultado_text.insert(tk.END, f"🔹 Cálculo del MCD para: {numeros}\n\n")

        for i in range(1, len(numeros)):
            a, b = resultado, numeros[i]
            mcd_actual, pasos = mcd(a, b)
            resultado_text.insert(tk.END, f"Calculando MCD({a}, {b})\n")
            resultado_text.insert(tk.END, f"{'Dividendo':<12}{'Divisor':<12}{'Cociente':<12}{'Residuo':<12}\n")
            resultado_text.insert(tk.END, "-"*48 + "\n")
            for fila in pasos:
                resultado_text.insert(tk.END, f"{fila[0]:<12}{fila[1]:<12}{fila[2]:<12}{fila[3]:<12}\n")
            resultado_text.insert(tk.END, f"mcd({a}, {b}) = {mcd_actual}\n\n")
            resultado = mcd_actual

        resultado_text.insert(tk.END, f"El MCD de todos los números es: {resultado}")
        resultado_text.config(state="disabled")

    except ValueError:
        messagebox.showerror("Error", "Asegúrate de ingresar solo números separados por comas.")


def ventana_euclides():
    # Hereda colores del menú
    color_fondo = "#EAF0FB"
    color_marco = "#FFFFFF"
    color_titulo = "#0A2472"
    color_boton = "#2C5BA8"
    color_boton_hover = "#1E4382"
    color_texto = "#333333"
    color_dorado = "#CFAF33"

    ventana = tk.Toplevel()
    ventana.title("Algoritmo de Euclides - UMG")
    ventana.geometry("750x600")
    ventana.config(bg=color_fondo)

    # Encabezado principal
    header = tk.Frame(ventana, bg=color_titulo)
    header.pack(fill="x")
    tk.Label(header, text="⚙️ Algoritmo de Euclides ⚙️",
             font=("Segoe UI", 16, "bold"), fg="white", bg=color_titulo, pady=10).pack()

    # Contenedor principal
    container = tk.Frame(ventana, bg=color_marco)
    container.pack(expand=True, fill="both", padx=20, pady=20)

    tk.Label(container, text="Ingresa los números separados por comas:",
             bg=color_marco, fg=color_texto, font=("Segoe UI", 11)).pack(pady=5)
    numeros_entry = tk.Entry(container, width=60, justify="center", font=("Segoe UI", 11),
                             bg="white", fg=color_texto, relief="solid", bd=1)
    numeros_entry.pack(pady=5)
    numeros_entry.insert(0, "112, 35, 21")

    # Área de resultados
    frame_text = tk.Frame(container, bg=color_marco)
    frame_text.pack(pady=15, fill="both", expand=True)

    resultado_text = tk.Text(frame_text, height=18, wrap="none",
                             bg=color_fondo, fg=color_texto,
                             font=("Consolas", 10), relief="flat", bd=5)
    resultado_text.pack(side=tk.LEFT, fill="both", expand=True)
    resultado_text.config(state="disabled")

    scrollbar = tk.Scrollbar(frame_text, command=resultado_text.yview, bg=color_fondo)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    resultado_text.config(yscrollcommand=scrollbar.set)

    # Botones inferiores
    botones = tk.Frame(container, bg=color_marco)
    botones.pack(pady=10)

    def on_enter(e): e.widget.config(bg=color_boton_hover)
    def on_leave(e): e.widget.config(bg=color_boton)

    btn_calcular = tk.Button(botones, text="Calcular MCD", bg=color_boton, fg="white",
                             font=("Segoe UI", 11, "bold"),
                             command=lambda: calcular_mcd(numeros_entry, resultado_text),
                             relief="flat", padx=20, pady=5)
    btn_calcular.grid(row=0, column=0, padx=10)
    btn_calcular.bind("<Enter>", on_enter)
    btn_calcular.bind("<Leave>", on_leave)

    btn_cerrar = tk.Button(botones, text="Cerrar", bg=color_boton, fg="white",
                           font=("Segoe UI", 11, "bold"),
                           command=ventana.destroy,
                           relief="flat", padx=20, pady=5)
    btn_cerrar.grid(row=0, column=1, padx=10)
    btn_cerrar.bind("<Enter>", on_enter)
    btn_cerrar.bind("<Leave>", on_leave)

    # Footer decorativo
    tk.Label(ventana,
             text="Proyecto Matemáticas Discretas - Universidad Mariano Gálvez",
             bg=color_fondo, fg=color_dorado, font=("Segoe UI", 9, "italic")).pack(side="bottom", pady=5)
