import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

# --- Colores institucionales UMG ---
# (Definidos aquí para que el módulo sea independiente)
color_fondo = "#EAF0FB"
color_marco = "#FFFFFF"
color_titulo = "#0A2472"
color_boton = "#2C5BA8"
color_boton_hover = "#1E4382"
color_texto = "#333333"
color_dorado = "#CFAF33"

def abrir_manual(parent):
    """
    Crea y muestra la ventana del manual de usuario como un Toplevel modal.
    'parent' es la ventana principal (root) que será bloqueada.
    """
    manual_win = tk.Toplevel(parent)
    manual_win.title("Manual de Usuario")
    manual_win.geometry("700x550")
    manual_win.resizable(False, False)
    manual_win.config(bg=color_marco)
    
    # Hacer que la ventana sea "modal" (bloquea la ventana principal)
    manual_win.grab_set()
    manual_win.transient(parent)

    # --- Estilo para el Notebook (Pestañas) ---
    style_manual = ttk.Style()
    # Asegurarse de que el tema 'clam' se usa si no está ya cargado
    style_manual.theme_use("clam") 
    
    style_manual.configure("TFrame", background=color_marco) # Fondo para los frames dentro del notebook
    style_manual.configure("TNotebook", background=color_marco)
    style_manual.configure("TNotebook.Tab", 
                    font=("Segoe UI", 10, "bold"), 
                    padding=[10, 5],
                    background=color_fondo,
                    foreground=color_titulo)
    style_manual.map("TNotebook.Tab", 
              background=[("selected", color_marco)],
              foreground=[("selected", color_boton)])
    
    # Estilo para el botón de cierre dentro del manual
    style_manual.configure("Manual.TButton",
                    font=("Segoe UI", 11, "bold"),
                    foreground="white",
                    background=color_boton,
                    padding=10)
    style_manual.map("Manual.TButton", background=[("active", color_boton_hover)])


    # --- Título de la ventana ---
    ttk.Label(manual_win, text="Manual de Usuario", 
              font=("Segoe UI", 16, "bold"), 
              background=color_marco, 
              foreground=color_titulo).pack(pady=15)

    # --- Notebook (Contenedor de Pestañas) ---
    notebook = ttk.Notebook(manual_win, style="TNotebook")
    
    # --- Pestaña 1: Algoritmo de Euclides ---
    tab_euclides = ttk.Frame(notebook, style="TFrame", padding=10)
    notebook.add(tab_euclides, text="Algoritmo de Euclides")
    
    txt_euclides = scrolledtext.ScrolledText(tab_euclides, wrap=tk.WORD, 
                                             width=80, height=25, 
                                             font=("Segoe UI", 10),
                                             bg=color_marco, fg=color_texto,
                                             relief="flat", borderwidth=0)
    txt_euclides.pack(expand=True, fill="both", padx=5, pady=5)

    # --- Pestaña 2: Visualizador de Dijkstra ---
    tab_dijkstra = ttk.Frame(notebook, style="TFrame", padding=10)
    notebook.add(tab_dijkstra, text="Visualizador de Dijkstra")
    
    txt_dijkstra = scrolledtext.ScrolledText(tab_dijkstra, wrap=tk.WORD, 
                                             width=80, height=25, 
                                             font=("Segoe UI", 10),
                                             bg=color_marco, fg=color_texto,
                                             relief="flat", borderwidth=0)
    txt_dijkstra.pack(expand=True, fill="both", padx=5, pady=5)
    
    notebook.pack(pady=10, padx=15, expand=True, fill="both")

    # --- Configurar tags de estilo para el texto (fuentes y colores) ---
    for txt_widget in [txt_euclides, txt_dijkstra]:
        txt_widget.tag_configure("h1", font=("Segoe UI", 14, "bold"), 
                                 foreground=color_titulo, spacing1=10, spacing3=5)
        txt_widget.tag_configure("h2", font=("Segoe UI", 11, "bold"), 
                                 foreground=color_boton, spacing1=8, spacing3=3)
        txt_widget.tag_configure("bold", font=("Segoe UI", 10, "bold"), foreground=color_texto)
        txt_widget.tag_configure("normal", font=("Segoe UI", 10), foreground=color_texto)

    # --- Insertar contenido: Euclides ---
    txt_euclides.insert(tk.END, "Algoritmo de Euclides\n", "h1")
    txt_euclides.insert(tk.END, "Este programa calcula el Máximo Común Divisor (MCD) de un conjunto de números.\n\n", "normal")
    
    txt_euclides.insert(tk.END, "Instrucciones de Uso:\n", "h2")
    txt_euclides.insert(tk.END, "1. ", "bold")
    txt_euclides.insert(tk.END, "En el campo de texto, ingresa los números de los que deseas calcular el MCD.\n", "normal")
    txt_euclides.insert(tk.END, "2. ", "bold")
    txt_euclides.insert(tk.END, "Debes separar cada número con una coma (,). (Ejemplo: 112, 35, 21)\n", "normal")
    txt_euclides.insert(tk.END, "3. ", "bold")
    txt_euclides.insert(tk.END, "Presiona el botón ", "normal")
    txt_euclides.insert(tk.END, "Calcular MCD", "bold")
    txt_euclides.insert(tk.END, ".\n", "normal")
    txt_euclides.insert(tk.END, "4. ", "bold")
    txt_euclides.insert(tk.END, "El resultado se mostrará en una ventana emergente.\n", "normal")
    txt_euclides.insert(tk.END, "5. ", "bold")
    txt_euclides.insert(tk.END, "Presiona ", "normal")
    txt_euclides.insert(tk.END, "Cerrar", "bold")
    txt_euclides.insert(tk.END, " para salir de la calculadora de Euclides.\n", "normal")
    
    # Deshabilitar edición
    txt_euclides.config(state="disabled")

    # --- Insertar contenido: Dijkstra ---
    txt_dijkstra.insert(tk.END, "Visualizador de Algoritmo de Dijkstra\n", "h1")
    txt_dijkstra.insert(tk.END, "Esta herramienta permite crear un grafo y calcular la ruta más corta entre dos nodos.\n\n", "normal")

    txt_dijkstra.insert(tk.END, "Panel de Herramientas:\n", "h2")
    txt_dijkstra.insert(tk.END, "• Mover/Crear Nodo: ", "bold")
    txt_dijkstra.insert(tk.END, "Haz clic en el lienzo (cuadrícula) para crear un nuevo nodo. Haz clic y arrastra un nodo existente para moverlo.\n", "normal")
    txt_dijkstra.insert(tk.END, "• Crear Arista: ", "bold")
    txt_dijkstra.insert(tk.END, "Selecciona esta opción, luego haz clic en un nodo de inicio y después en un nodo de destino. Se te pedirá ingresar el 'costo' (peso) de la arista.\n", "normal")
    txt_dijkstra.insert(tk.END, "• Editar Costo: ", "bold")
    txt_dijkstra.insert(tk.END, "Selecciona esto y haz clic sobre una arista existente para cambiar su costo.\n", "normal")
    txt_dijkstra.insert(tk.END, "• Renombrar Nodo: ", "bold")
    txt_dijkstra.insert(tk.END, "Haz clic sobre un nodo para cambiar su nombre.\n", "normal")
    txt_dijkstra.insert(tk.END, "• Eliminar: ", "bold")
    txt_dijkstra.insert(tk.END, "Haz clic sobre cualquier nodo o arista para borrarlo del lienzo.\n", "normal")
    txt_dijkstra.insert(tk.END, "• Buscar Ruta: ", "bold")
    txt_dijkstra.insert(tk.END, "La función principal. Haz clic en el nodo de inicio y luego en el nodo final. El algoritmo se ejecutará.\n", "normal")
    txt_dijkstra.insert(tk.END, "• Limpiar Todo: ", "bold")
    txt_dijkstra.insert(tk.END, "Borra todos los nodos y aristas del lienzo.\n\n", "normal")

    txt_dijkstra.insert(tk.END, "Panel de Archivo:\n", "h2")
    txt_dijkstra.insert(tk.END, "• Guardar Grafo: ", "bold")
    txt_dijkstra.insert(tk.END, "Guarda tu grafo actual (nodos, posiciones y aristas) en un archivo para usarlo más tarde.\n", "normal")
    txt_dijkstra.insert(tk.END, "• Cargar Grafo: ", "bold")
    txt_dijkstra.insert(tk.END, "Abre un archivo de grafo guardado previamente.\n\n", "normal")

    txt_dijkstra.insert(tk.END, "Panel de Resultados:\n", "h2")
    txt_dijkstra.insert(tk.END, "• Resultados: ", "bold")
    txt_dijkstra.insert(tk.END, "Este cuadro de texto mostrará los pasos del algoritmo y, al finalizar, la ruta más corta encontrada y su costo total.\n", "normal")

    # Deshabilitar edición
    txt_dijkstra.config(state="disabled")

    # --- Botón de salida del manual ---
    btn_cerrar_manual = ttk.Button(manual_win, text="Cerrar Manual", 
                                   command=manual_win.destroy, style="Manual.TButton")
    btn_cerrar_manual.pack(pady=15)
    
    # Esperar hasta que la ventana del manual se cierre
    manual_win.wait_window()


# --- Bloque para probar este módulo de forma independiente ---
if __name__ == "__main__":
    # Si ejecutas este archivo directamente, se abrirá una ventana de prueba
    # con solo el manual.
    
    root = tk.Tk()
    root.title("Prueba del Manual")
    root.geometry("300x200")
    
    # Estilo para el botón de prueba
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton",
                    font=("Segoe UI", 11, "bold"),
                    foreground="white",
                    background=color_boton,
                    padding=10)
    style.map("TButton", background=[("active", color_boton_hover)])
    
    label = ttk.Label(root, text="Ventana principal de prueba")
    label.pack(pady=20)
    
    # Botón para abrir el manual
    btn_abrir = ttk.Button(root, text="Abrir Manual", command=lambda: abrir_manual(root))
    btn_abrir.pack(pady=20)
    
    root.mainloop()