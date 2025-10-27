import tkinter as tk
from tkinter import ttk
# IMPORTAMOS las funciones específicas que abren las ventanas secundarias
from euclides import ventana_euclides
from dijkstra import ventana_dijkstra

def menu():
    app = tk.Tk()
    app.title("App de Algoritmos - Universidad Mariano Gálvez")
    app.geometry("650x600")  # Ventana más grande
    app.resizable(False, False)

    # --- Colores institucionales UMG ---
    color_fondo = "#EAF0FB"
    color_marco = "#FFFFFF"
    color_titulo = "#0A2472"
    color_boton = "#2C5BA8"
    color_boton_hover = "#1E4382"
    color_texto = "#333333"
    color_dorado = "#CFAF33"

    app.config(bg=color_fondo)

    # --- Estilos personalizados ttk ---
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TLabel", background=color_marco, foreground=color_texto, font=("Segoe UI", 10))
    style.configure("Header.TLabel", background=color_marco, foreground=color_titulo, font=("Segoe UI", 16, "bold"))
    style.configure("Footer.TLabel", background=color_fondo, foreground=color_titulo, font=("Segoe UI", 9, "italic"))

    style.configure("TButton",
                    font=("Segoe UI", 11, "bold"),
                    foreground="white",
                    background=color_boton,
                    padding=10)
    style.map("TButton", background=[("active", color_boton_hover)])

    # --- Marco principal ---
    marco = tk.Frame(app, bg=color_marco, bd=2, relief="ridge")
    marco.place(relx=0.5, rely=0.5, anchor="center", width=580, height=520)  # Marco más grande







    # --- Encabezado ---
    ttk.Label(marco, text="Universidad Mariano Gálvez de Guatemala", style="Header.TLabel").pack(pady=(20, 5))
    ttk.Label(marco, text="Facultad de Ingeniería", font=("Segoe UI", 11, "italic"),
              background=color_marco, foreground=color_dorado).pack()
    ttk.Label(marco, text="Aplicación de Algoritmos", font=("Segoe UI", 13, "bold"),
              background=color_marco, foreground=color_titulo).pack(pady=10)

    # --- Botones ---
    ttk.Button(marco, text="⚙️  Algoritmo de Euclides", width=38, command=ventana_euclides).pack(pady=8)
    ttk.Button(marco, text="🔍  Algoritmo de Dijkstra", width=38, command=ventana_dijkstra).pack(pady=8)
    ttk.Button(marco, text="❌  Salir", width=38, command=app.destroy).pack(pady=12)

    # --- Separador dorado ---
    tk.Frame(marco, bg=color_dorado, height=2, width=360).pack(pady=10)

    # --- Integrantes ---
    ttk.Label(marco, text="Integrantes del grupo:", font=("Segoe UI", 10, "bold"),
              background=color_marco, foreground=color_titulo).pack(pady=(10, 0))
    
    ttk.Label(
        marco,
        text="• David Santos\n• Edwin Gonzales\n• Roberto Batzin\n• Elena Sánchez\n* Sección B-Plan Diario\n",
        background=color_marco,
        foreground=color_texto,
        font=("Segoe UI", 10),
        justify="center"
    ).pack(pady=8)

    # --- Pie de página ---
    ttk.Label(app, text="Proyecto académico - 2025", style="Footer.TLabel").pack(side="bottom", pady=5)

    app.mainloop()

if __name__ == "__main__":
    menu()
