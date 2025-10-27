# IMPORTACIÓN DE LIBRERÍAS
import tkinter as tk  # Biblioteca principal para la interfaz gráfica.
from tkinter import simpledialog, messagebox, filedialog  # Módulos para diálogos, mensajes y seleccion de archivos.
from collections import defaultdict  # Para el diccionario del grafo.
import heapq  # Para la Cola de Prioridad en Dijkstra.
import math  # Para cálculos matemáticos (sqrt, inf).
import json  # Para trabajar con archivos JSON (guardar/cargar).

NODE_RADIUS = 15       # Radio de los circulos de nodo.
LABEL_OFFSET = 12      # Desplazamiento del texto del costo de arista.
GRID_SPACING = 50      # Espaciado de la cuadricula de fondo.
NODE_COLOR = "#4a90e2"       # Color de los nodos.
NODE_TEXT_COLOR = "white"    # Color del texto dentro de los nodos.
EDGE_COLOR = "#555555"       # Color de las aristas.
EDGE_TEXT_COLOR = "#333333"  # Color del texto del costo de arista.
PATH_COLOR = "#e67e22"       # Color de la ruta encontrada.
PATH_WIDTH = 3               # Grosor de la linea de la ruta.
STATUS_BAR_COLOR = "#f0f0f0" # Color de la barra de estado inferior.
HIGHLIGHT_COLOR = "#d35400"  # Color de resalte para nodos seleccionados/inicio/fin.
GRID_COLOR = "#e0e0e0"       # Color de la cuadricula de fondo.
PANEL_BG = "#243040"       # Color de fondo del panel izquierdo (tu color).
BTN_BG = "#506785"       # Color de fondo de los botones (tu color).
BTN_FG = "#F0E9E9"       # Color del texto de los botones (tu color).
BTN_RELIEF = tk.SOLID        # Relieve de los botones (borde sólido).
BTN_BORDER = 1               # Grosor del borde de los botones.
BTN_BORDER_COLOR = "#bbbbbb"  # Color del borde de los botones.
BTN_ACTIVE_BG = "#e0e0e0"     # Color del boton al presionarlo.
BTN_SUNKEN_BG = "#2C5C9B"   # Color del boton cuando el modo está activo (tu color).
BTN_SUNKEN_RELIEF = tk.SUNKEN # Relieve del boton activo.
RESULTS_BG = "#7DA3D4"       # Color de fondo del panel de resultados (tu color).

# CLASE PRINCIPAL DE LA APLICACIÓN
class DijkstraGUI:

    def __init__(self, root):
        self.root = root # Guarda la ventana principal.
        self.root.title("Visualizador de Algoritmo de Dijkstra") # titulo de la ventana.
        self.root.geometry("1000x700") # Tamaño inicial.

        self.graph = defaultdict(dict)           # Diccionario para el grafo.
        self.node_coords = {}                    
        self.node_display_names = {}            
        self.node_items = {}                     
        self.edge_items = {}                     
        self.path_items = []                     

        self.node_counter = 0                    # Contador para asignar IDs a nodos nuevos.
        self.mode = "nodes"                      # Modo actual de la aplicación.
        self.selected_node_1 = None              # Primer nodo seleccionado al crear arista.
        self.start_node = None                   # Nodo inicial para Dijkstra.
        self.end_node = None                     # Nodo final para Dijkstra.
        self.dragging_node = None                # ID del nodo que se está arrastrando.
        self.drag_start_x = 0                    # posicion X inicial del arrastre.
        self.drag_start_y = 0                    # posicion Y inicial del arrastre.
        self.bg_image_tk = None                  # Referencia a la imagen de fondo (Tkinter).
        self.bg_image_item = None                # ID del item de imagen en el canvas.

        self.status_label = tk.Label(root, text="Modo: Mover/Crear Nodo", anchor="w",
                                     bg=STATUS_BAR_COLOR, relief=tk.SUNKEN, padx=10)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Panel izquierdo
        panel_width = 180
        left_panel = tk.Frame(root, bg=PANEL_BG, width=panel_width, padx=10, pady=10)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        left_panel.pack_propagate(False) # evita que el panel se encoja
        # titulo del panel
        tk.Label(left_panel, text="Herramientas", font=("Arial", 14, "bold"), bg=PANEL_BG, fg=BTN_FG).pack(side=tk.TOP, pady=(0, 10))

        # Fuente común para botones
        btn_font = ("Arial", 10)

        # Creación de Botones
        # boton Mover/Crear Nodo
        self.btn_nodes = tk.Button(left_panel, text="Mover/Crear Nodo", command=self.modo_actual_nodes,
                                   font=btn_font, bg=BTN_BG, fg=BTN_FG, activebackground=BTN_ACTIVE_BG,
                                   relief=BTN_RELIEF, borderwidth=BTN_BORDER,
                                   highlightbackground=BTN_BORDER_COLOR, highlightthickness=BTN_BORDER)
        self.btn_nodes.pack(side=tk.TOP, fill=tk.X, pady=4)
        # boton Crear Arista
        self.btn_edges = tk.Button(left_panel, text="Crear Arista", command=self.modo_actual_edges,
                                   font=btn_font, bg=BTN_BG, fg=BTN_FG, activebackground=BTN_ACTIVE_BG,
                                   relief=BTN_RELIEF, borderwidth=BTN_BORDER,
                                   highlightbackground=BTN_BORDER_COLOR, highlightthickness=BTN_BORDER)
        self.btn_edges.pack(side=tk.TOP, fill=tk.X, pady=4)
        # boton Editar Costo
        self.btn_edit = tk.Button(left_panel, text="Editar Costo", command=self.modo_actual_edit,
                                  font=btn_font, bg=BTN_BG, fg=BTN_FG, activebackground=BTN_ACTIVE_BG,
                                  relief=BTN_RELIEF, borderwidth=BTN_BORDER,
                                  highlightbackground=BTN_BORDER_COLOR, highlightthickness=BTN_BORDER)
        self.btn_edit.pack(side=tk.TOP, fill=tk.X, pady=4)
        # boton Renombrar Nodo
        self.btn_rename = tk.Button(left_panel, text="Renombrar Nodo", command=self.modo_actual_rename,
                                    font=btn_font, bg=BTN_BG, fg=BTN_FG, activebackground=BTN_ACTIVE_BG,
                                    relief=BTN_RELIEF, borderwidth=BTN_BORDER,
                                    highlightbackground=BTN_BORDER_COLOR, highlightthickness=BTN_BORDER)
        self.btn_rename.pack(side=tk.TOP, fill=tk.X, pady=4)
        # boton Eliminar
        self.btn_delete = tk.Button(left_panel, text="Eliminar", command=self.modo_actual_delete,
                                    font=btn_font, bg=BTN_BG, fg=BTN_FG, activebackground=BTN_ACTIVE_BG,
                                    relief=BTN_RELIEF, borderwidth=BTN_BORDER,
                                    highlightbackground=BTN_BORDER_COLOR, highlightthickness=BTN_BORDER)
        self.btn_delete.pack(side=tk.TOP, fill=tk.X, pady=4)
        # boton Buscar Ruta
        self.btn_path = tk.Button(left_panel, text="Buscar Ruta", command=self.modo_actual_path_start,
                                  font=btn_font, bg=BTN_BG, fg=BTN_FG, activebackground=BTN_ACTIVE_BG,
                                  relief=BTN_RELIEF, borderwidth=BTN_BORDER,
                                  highlightbackground=BTN_BORDER_COLOR, highlightthickness=BTN_BORDER)
        self.btn_path.pack(side=tk.TOP, fill=tk.X, pady=4)
        # boton Limpiar Todo 
        self.btn_clear = tk.Button(left_panel, text="Limpiar Todo", command=self.funcion_limpiar,
                                   font=btn_font, bg=BTN_BG, fg=BTN_FG, activebackground=BTN_ACTIVE_BG,
                                   relief=BTN_RELIEF, borderwidth=BTN_BORDER,
                                   highlightbackground=BTN_BORDER_COLOR, highlightthickness=BTN_BORDER)
        self.btn_clear.pack(side=tk.TOP, fill=tk.X, pady=4) # Cambiado a side=tk.TOP
        self.modo_actual_nodes() # Establece el modo inicial y aplica estilo al boton.

        # Sección Guardar/Cargar
        tk.Frame(left_panel, height=2, bg="#c0c0c0").pack(side=tk.TOP, fill=tk.X, pady=10) # Separador
        tk.Label(left_panel, text="Archivo", font=("Arial", 12, "bold"), bg=PANEL_BG, fg=BTN_FG).pack(side=tk.TOP, pady=0)

        # boton Guardar Grafo
        self.btn_save = tk.Button(left_panel, text="Guardar Grafo", command=self.save_graph,
                                  font=btn_font, bg=BTN_BG, fg=BTN_FG, activebackground=BTN_ACTIVE_BG,
                                  relief=BTN_RELIEF, borderwidth=BTN_BORDER,
                                  highlightbackground=BTN_BORDER_COLOR, highlightthickness=BTN_BORDER)
        self.btn_save.pack(side=tk.TOP, fill=tk.X, pady=(10, 4))

        # boton Cargar Grafo
        self.btn_load = tk.Button(left_panel, text="Cargar Grafo", command=self.load_graph,
                                  font=btn_font, bg=BTN_BG, fg=BTN_FG, activebackground=BTN_ACTIVE_BG,
                                  relief=BTN_RELIEF, borderwidth=BTN_BORDER,
                                  highlightbackground=BTN_BORDER_COLOR, highlightthickness=BTN_BORDER)
        self.btn_load.pack(side=tk.TOP, fill=tk.X, pady=4)

        # Sección Resultados
        tk.Frame(left_panel, height=2, bg="#c0c0c0").pack(side=tk.TOP, fill=tk.X, pady=10) # Separador
        tk.Label(left_panel, text="Resultados", font=("Arial", 12, "bold"), bg=PANEL_BG, fg=BTN_FG).pack(side=tk.TOP, pady=0)

        # Etiqueta para mostrar la ruta y el costo
        self.results_label = tk.Label(left_panel, text="Resultados:\n---",
                                      bg=RESULTS_BG, fg="#004d40",
                                      justify=tk.LEFT, anchor="n", wraplength=panel_width-20, height=8,
                                      relief=tk.SOLID, borderwidth=1, padx=5, pady=5)
        self.results_label.pack(side=tk.TOP, fill=tk.X, pady=5)

        # Lienzo Principal
        self.canvas = tk.Canvas(root, bg="#f8f6ee", highlightthickness=0) # Área de dibujo.
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) # Ocupa el resto del espacio.

        self.Dibujo_cuadricula() # Dibuja la cuadricula inicial.

        # Conexiones de Eventos del Lienzo
        self.canvas.bind("<Button-1>", self.click_canvas)       # Clic izquierdo llama a click_canvas.
        self.canvas.bind("<B1-Motion>", self.arrastrar_canvas)        # Arrastrar con clic izquierdo llama a arrastrar_canvas.
        self.canvas.bind("<ButtonRelease-1>", self.arrastrar_canvas_finalizado) # Soltar clic izquierdo llama a arrastrar_canvas_finalizado.

    # FUNCIONES DE CAMBIO DE MODO Y DIBUJO - <---ECHO EN GRUPO--->

    def Dibujo_cuadricula(self): #Dibuja lineas grises de fondo para formar una cuadricula
        # Obtiene el tamaño de la pantalla para dibujar lineas suficientemente largas
        width = self.canvas.winfo_screenwidth()
        height = self.canvas.winfo_screenheight()
        # Dibuja lineas verticales.
        for x in range(0, width, GRID_SPACING):
            line = self.canvas.create_line(x, 0, x, height, fill=GRID_COLOR, tags="grid_line")
            self.canvas.tag_lower(line) # Envía la linea al fondo.
        # Dibuja lineas horizontales.
        for y in range(0, height, GRID_SPACING):
            line = self.canvas.create_line(0, y, width, y, fill=GRID_COLOR, tags="grid_line")
            self.canvas.tag_lower(line) # Envía la linea al fondo.

    def modo_actual(self, new_mode, status_text): #actualiza el modo actual y el estilo visual de los botones
        self.mode = new_mode # Guarda el nuevo modo.
        self.instrucciones_actualizacion(status_text) # Actualiza la barra de estado.

        # Si el usuario presiona "Buscar Ruta" limpia la ruta anterior
        if new_mode == "path_start":
            self.restablecer_ruta()

        # Limpia la seleccion temporal de nodos para crear aristas.
        self.cambia_colorvertice(self.selected_node_1, False)
        self.selected_node_1 = None

        # Lista de todos los botones de modo.
        buttons = [self.btn_nodes, self.btn_edges, self.btn_rename, self.btn_delete, self.btn_path, self.btn_edit]

        # Resetea el estilo de TODOS los botones a 'normal' (borde sólido, blanco).
        for btn in buttons:
            btn.config(relief=BTN_RELIEF, bg=BTN_BG, fg=BTN_FG,
                       borderwidth=BTN_BORDER, highlightthickness=BTN_BORDER)

        # Busca cual boton corresponde al modo que se acaba de activar.
        active_button = {
            "nodes": self.btn_nodes,
            "edges": self.btn_edges,
            "rename": self.btn_rename,
            "delete": self.btn_delete,
            "edit": self.btn_edit,
            "path_start": self.btn_path,
            "path_end": self.btn_path # tambien se activa al seleccionar el nodo final.
        }.get(new_mode)

        # Si se encontró un boton activo le aplica el estilo hundido.
        if active_button:
            active_button.config(relief=BTN_SUNKEN_RELIEF, bg=BTN_SUNKEN_BG,
                                 highlightthickness=0)
    # Llamadas por los botones para cambiar el modo.
    def modo_actual_nodes(self):
        self.modo_actual("nodes", "Modo: Mover/Crear Nodo. Arrastra un nodo para moverlo o haz clic en el lienzo para crear.")

    def modo_actual_edges(self):
        self.modo_actual("edges", "Modo: Crear Arista. Haz clic en el primer nodo.")

    def modo_actual_edit(self):
        self.modo_actual("edit", "Modo: Editar Costo. Haz clic en el costo de una arista para cambiarlo.")

    def modo_actual_rename(self):
        self.modo_actual("rename", "Modo: Renombrar. Haz clic en el nodo que deseas renombrar.")

    def modo_actual_delete(self):
        self.modo_actual("delete", "Modo: Eliminar. Haz clic en un nodo o en el costo de una arista.")

    def modo_actual_path_start(self):
        self.modo_actual("path_start", "Modo: Buscar Ruta. Haz clic en el nodo INICIAL.")

    # LÓGICA PRINCIPAL (EVENTOS DEL MAUSE EN EL CANVAS) - <---ECHO POR IA--->

    def click_canvas(self, event): # Manejador principal para clics izquierdos en el lienzo
        node_id = self.get_node_at(event.x, event.y)  # Determina si se hizo clic sobre un nodo.
        # Actua segun el modo actual.
        if self.mode == "nodes": # Modo Mover/Crear Nodo
            if node_id is not None: # Si se hizo clic en un nodo
                # Inicia el proceso de arrastre.
                self.dragging_node = node_id
                self.drag_start_x = event.x
                self.drag_start_y = event.y
            else: # Si se hizo clic en el vacío
                # Crea un nuevo nodo.
                self.crear_vertice(event.x, event.y)
            return # Termina la función aquí para este modo.
        if self.mode == "delete": # Modo Eliminar
            if node_id is not None: # Si se hizo clic en un nodo...
                self.borrar_vertice(node_id) # Llama a borrar nodo.
            else: # Si se hizo clic en el vacío (podría ser una arista)...
                self.editar_eliminar_arista(event.x, event.y) # Comprueba si es una arista.
            return
        if self.mode == "edit": # Modo Editar Costo
            # Solo intenta editar si se hizo clic en una etiqueta de arista.
            self.editar_eliminar_arista(event.x, event.y)
            return
        if self.mode == "rename": # Modo Renombrar
            if node_id is not None: # Si se hizo clic en un nodo...
                self.renombrar_vertice(node_id) # Llama a renombrar.
            return
        if node_id is None: # Si se hizo clic en el vacío...
            self.reset_selections() # Limpia selecciones temporales.
            return

        # Si se hizo clic en un nodo y el modo es...
        if self.mode == "edges": # Crear Arista
            self.seleccion_vertices_arista(node_id)
        elif self.mode == "path_start": # Buscar Ruta (seleccionando inicio)
            self.inicia_seleccion_1vertice(node_id)
        elif self.mode == "path_end": # Buscar Ruta (seleccionando fin)
            self.finaliza_seleccion_2vertice(node_id)

    def arrastrar_canvas(self, event):#Manejador para cuando se arrastra el ratón con el clic presionado
        if self.dragging_node is not None and self.mode == "nodes": # Solo actua si estamos en modo 'nodes' y ya se inició un arrastre.
            node_id = self.dragging_node 
            # Calcula el desplazamiento desde la última posicion
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y
            # Mueve los items visuales (circulo y texto) del nodo en el canvas.
            tag = f"node_{node_id}"
            self.canvas.move(tag, dx, dy)
            # Actualiza las coordenadas guardadas del nodo.
            self.node_coords[node_id] = (self.node_coords[node_id][0] + dx, self.node_coords[node_id][1] + dy)
            # Redibuja las aristas conectadas a este nodo.
            self.actualiza_aristas_movimiento_vertice(node_id)
            # Si hay una ruta activa, la recalcula en tiempo real.
            self.ejercuta_automatico_modificar()
            # Guarda la posicion actual para el próximo cálculo de 'dx', 'dy'.
            self.drag_start_x = event.x
            self.drag_start_y = event.y

    def arrastrar_canvas_finalizado(self, event):
        self.dragging_node = None # Finaliza el estado de arrastre.

    # MANEJADORES DE LÓGICA (CREACIÓN)

    def crear_vertice(self, x, y):
        node_id = self.node_counter # Obtiene un ID único.
        self.node_counter += 1
        # Guarda la información del nodo.
        self.node_coords[node_id] = (x, y)
        display_name = str(node_id) # Nombre inicial es su ID
        self.node_display_names[node_id] = display_name
        # Dibuja el nodo en el canvas
        tag = f"node_{node_id}" # Tag para agrupar circulo y texto.
        # Dibuja el circulo
        oval = self.canvas.create_oval(
            x - NODE_RADIUS, y - NODE_RADIUS, x + NODE_RADIUS, y + NODE_RADIUS,
            fill=NODE_COLOR, outline="", tags=(tag,)
        )
        # Dibuja el texto (ID)
        text = self.canvas.create_text(x, y, text=display_name, fill=NODE_TEXT_COLOR,
                                       font=("Arial", 10, "bold"), tags=(tag,))
        # Guarda las referencias a los items del canvas
        self.node_items[node_id] = (oval, text)
        self.instrucciones_actualizacion(f"Nodo '{display_name}' (ID: {node_id}) creado.")

    def seleccion_vertices_arista(self, node_id): #Gestiona el proceso de seleccionar dos nodos para crear una arista
        if self.selected_node_1 is None: # Si es el primer nodo seleccionado...
            self.selected_node_1 = node_id # Guarda el nodo.
            self.cambia_colorvertice(node_id, True) # Lo resalta.
            name = self.node_display_names[node_id]
            self.instrucciones_actualizacion(f"Nodo '{name}' seleccionado. Haz clic en el segundo nodo.")

        elif self.selected_node_1 != node_id: # Si es el segundo nodo (y diferente al primero)...
            self.crea_arista(self.selected_node_1, node_id) # Llama a la función para crear la arista.
            self.reset_selections() # Limpia la seleccion.
        else: # Si se hizo clic de nuevo en el primer nodo...
            self.reset_selections() # Cancela la seleccion.

    def crea_arista(self, n1, n2): # Clave siempre ordenada (ej. (1, 2)).
        edge_key = tuple(sorted((n1, n2)))
        arrow_shape = tk.NONE # Sin flecha.

        # Comprueba si ya existe una arista entre ellos (en cualquier dirección).
        if n2 in self.graph[n1] or n1 in self.graph[n2]:
            self.instrucciones_actualizacion("Error: Ya existe un vértice entre estos nodos.")
            return

        # Pide el costo (peso) de la arista al usuario.
        n1_name = self.node_display_names[n1]
        n2_name = self.node_display_names[n2]
        # Prompt siempre es para arista no dirigida.
        prompt = f"Ingrese el costo para {n1_name} <-> {n2_name}:"
        weight = simpledialog.askinteger("Costo de la Arista", prompt, minvalue=1)

        if weight is None: # Si el usuario cancela.
            self.instrucciones_actualizacion("Creación de arista cancelada.")
            return
        # Añade la arista a la estructura de datos del grafo (en AMBAS direcciones).
        self.graph[n1][n2] = weight
        self.graph[n2][n1] = weight
        # Dibuja la linea en el canvas.
        x1, y1 = self.node_coords[n1]
        x2, y2 = self.node_coords[n2]
        line = self.canvas.create_line(x1, y1, x2, y2, fill=EDGE_COLOR, width=2, arrow=arrow_shape)

        text_item, text_bg = self.dibuja_costo_arista(x1, y1, x2, y2, str(weight))  # Dibuja el texto del costo (con fondo blanco)

        # Ajusta el orden de las capas visuales.
        self.canvas.tag_lower(text_bg, line) # Fondo del texto detrás del texto.
        self.canvas.tag_raise(f"node_{n1}")  # Nodo 1 encima de la linea.
        self.canvas.tag_raise(f"node_{n2}")  # Nodo 2 encima de la linea.
        # Añade tags a los items de texto y fondo para poder encontrarlos luego (editar/borrar).
        tag = f"edge_{edge_key[0]}_{edge_key[1]}"
        self.canvas.addtag_withtag("edge_label", text_bg)
        self.canvas.addtag_withtag(tag, text_bg)
        self.canvas.addtag_withtag("edge_label", text_item)
        self.canvas.addtag_withtag(tag, text_item)
        # Guarda las referencias a los items del canvas.
        self.edge_items[edge_key] = (line, text_item, text_bg)
        self.instrucciones_actualizacion(f"Arista creada con costo {weight}.")

        self.ejercuta_automatico_modificar()         # Si hay una ruta activa, la recalcula.

    def dibuja_costo_arista(self, x1, y1, x2, y2, text): #Dibuja el texto del costo de la arista con un desplazamiento perpendicular
        # Calcula el punto medio de la linea.
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        # Calcula el vector director y su longitud.
        dx, dy = x2 - x1, y2 - y1
        length = math.sqrt(dx**2 + dy**2)
        if length == 0: length = 1 # Evita división por cero si los nodos están superpuestos.
        # Calcula el vector perpendicular unitario.
        unx, uny = -dy / length, dx / length
        # Calcula la posicion final del texto desplazado.
        text_x_pos = mid_x + unx * LABEL_OFFSET
        text_y_pos = mid_y + uny * LABEL_OFFSET

        # Dibuja un rectángulo de fondo (del color del canvas) para mejorar legibilidad.
        text_bg = self.canvas.create_rectangle(text_x_pos - 10, text_y_pos - 8, text_x_pos + 10, text_y_pos + 8,
                                               fill=self.canvas["bg"], outline="")
        # Dibuja el texto del costo.
        text_item = self.canvas.create_text(text_x_pos, text_y_pos, text=text, fill=EDGE_TEXT_COLOR,
                                       font=("Arial", 9, "bold"))
        return text_item, text_bg # Devuelve las referencias a los items creados.

    # MANEJADORES DE LÓGICA (MODIFICACIÓN/ELIMINACIÓN) - <---ECHO EN GRUPO--->

    def renombrar_vertice(self, node_id): #Permite al usuario cambiar el nombre visible de un nodo
        current_name = self.node_display_names[node_id]
        # Muestra un diálogo pidiendo el nuevo nombre.
        new_name = simpledialog.askstring("Renombrar Nodo",
                                          f"Ingrese el nuevo nombre para el nodo '{current_name}' (ID: {node_id}):",
                                          initialvalue=current_name)

        # Si el usuario ingresó un nombre y es diferente al actual...
        if new_name and new_name != current_name:
            self.node_display_names[node_id] = new_name # Actualiza el nombre guardado.
            _oval, text_item = self.node_items[node_id] # Obtiene el item de texto del canvas.
            self.canvas.itemconfig(text_item, text=new_name) # Cambia el texto visible.
            self.instrucciones_actualizacion(f"Nodo {node_id} renombrado a '{new_name}'.")

    def editar_eliminar_arista(self, x, y): # Determina qué hacer (editar/borrar) al hacer clic cerca de una arista
        edge_key = self.get_edge_key_at(x, y)  # Encuentra la clave (ej. (1,2)) de la arista en la que se hizo clic
        if edge_key is None: # Si no se hizo clic en una arista
            return

        # Actúa según el modo actual
        if self.mode == "delete":
            self.eliminar_arista(edge_key, confirm=True) # Llama a borrar arista
        elif self.mode == "edit":
            self.modificar_costo_arista(edge_key) # Llama a editar costo

    def get_edge_key_at(self, x, y): # Devuelve la clave de la arista (ej. (1,2)) cuya etiqueta está en (x, y)
        clicked_item = self.canvas.find_closest(x, y) # Encuentra el item del canvas mas cercano al clic
        if not clicked_item: # Si no hay items cerca.
            return None
        tags = self.canvas.gettags(clicked_item[0]) # Obtiene los tags asociados a ese item
        if "edge_label" in tags: # Comprueba si el item es una etiqueta de arista
            # Busca el tag específico de la arista (ej. "edge_1_2")
            for t in tags:
                if t.startswith("edge_"):
                    try:
                        # Extrae los IDs de los nodos del tag
                        _prefix, n1_str, n2_str = t.split('_')
                        n1, n2 = int(n1_str), int(n2_str)

                        # Comprueba si la clave existe en el diccionario de aristas (siempre ordenada)
                        key_undir = tuple(sorted((n1, n2)))
                        if key_undir in self.edge_items:
                            return key_undir # Devuelve la clave encontrada.
                    except ValueError: # Si el tag no tiene el formato esperado.
                        continue
        return None # Si no se encontro una etiqueta de arista

    def modificar_costo_arista(self, edge_key): #Permite al usuario cambiar el costo de una arista existente
        n1, n2 = edge_key[0], edge_key[1]

        # Obtiene el costo actual de la arista.
        current_weight = self.graph[n1].get(n2) # Funciona igual para no dirigidos
        if current_weight is None: return # Seguridad: si la arista no existe en el grafo.

        # Prepara el mensaje para el diálogo (siempre no dirigido).
        n1_name = self.node_display_names[n1]
        n2_name = self.node_display_names[n2]
        prompt = f"Nuevo costo para {n1_name} <-> {n2_name}:"

        # Muestra el diálogo pidiendo el nuevo costo.
        new_weight = simpledialog.askinteger("Editar Costo", prompt, initialvalue=current_weight, minvalue=1)

        # Si el usuario ingresó un costo y es diferente al actual...
        if new_weight is not None and new_weight != current_weight:
            # Actualiza el costo en la estructura del grafo (en AMBAS direcciones).
            self.graph[n1][n2] = new_weight
            self.graph[n2][n1] = new_weight

            # Actualiza el texto visible del costo en el canvas.
            _line, text_item, _text_bg = self.edge_items[edge_key]
            self.canvas.itemconfig(text_item, text=str(new_weight))
            self.instrucciones_actualizacion(f"Costo de arista {n1_name}-{n2_name} actualizado a {new_weight}.")

            # Recalcula la ruta por si este cambio la afecta.
            self.ejercuta_automatico_modificar()

    def borrar_vertice(self, node_id): #Elimina un nodo y todas sus aristas conectadas
        name = self.node_display_names[node_id]
        if not messagebox.askyesno("Confirmar Eliminación", f"¿Eliminar nodo '{name}'?"):
            return
        
        self.canvas.delete(f"node_{node_id}") # Borra los items visuales (circulo y texto) del canvas usando su tag.

        # Encuentra todas las aristas conectadas a este nodo.
        keys_to_delete = []
        for edge_key in self.edge_items:
            if node_id in edge_key:
                keys_to_delete.append(edge_key)
        # Llama a eliminar_arista para cada arista encontrada (sin pedir confirmación).
        for key in keys_to_delete:
            self.eliminar_arista(key, confirm=False)
        # Elimina el nodo de todas las estructuras de datos ("memoria").
        del self.node_items[node_id]
        del self.node_coords[node_id]
        del self.node_display_names[node_id]
        if node_id in self.graph: # Elimina la entrada del nodo como origen.
            del self.graph[node_id]
        # Busca y elimina el nodo como destino en las listas de otros nodos.
        for n in list(self.graph.keys()): # Itera sobre una copia de las claves
            if node_id in self.graph[n]:
                del self.graph[n][node_id]
        # Lógica para recalcular o limpiar la ruta si el nodo borrado era parte de ella.
        if node_id == self.start_node or node_id == self.end_node:
            # Si era el inicio o el fin, la ruta ya no es válida.
            self.restablecer_ruta() # Limpia la ruta visual y los resultados.
            self.start_node = None # Olvida el nodo de inicio/fin.
            self.end_node = None
            self.instrucciones_actualizacion(f"Nodo '{name}' eliminado. La ruta ha sido invalidada.")
        elif self.start_node is not None and self.end_node is not None:
            # Si era un nodo intermedio, intenta recalcular.
            self.instrucciones_actualizacion(f"Nodo '{name}' eliminado. Recalculando ruta...")
            self.ejercuta_automatico_modificar()
        else: # Si no habia ruta activa.
            self.instrucciones_actualizacion(f"Nodo '{name}' eliminado.")

    def eliminar_arista(self, edge_key, confirm=True): #Elimina una arista específica
        if edge_key not in self.edge_items: # Comprueba si la arista existe.
            return

        n1, n2 = edge_key[0], edge_key[1]
        # Pide confirmación solo si es una eliminación directa 
        if confirm:
            n1_name = self.node_display_names[n1]
            n2_name = self.node_display_names[n2]
            # Prompt siempre no dirigido.
            prompt = f"¿Eliminar arista {n1_name} <-> {n2_name}?"
            if not messagebox.askyesno("Confirmar Eliminación", prompt):
                return

        # Elimina la arista de la estructura del grafo (en AMBAS direcciones).
        if n2 in self.graph[n1]:
            del self.graph[n1][n2]
        if n1 in self.graph[n2]: # Siempre se intenta borrar la inversa.
            del self.graph[n2][n1]
        # Elimina los items visuales (linea, texto, fondo) del canvas.
        line, text_item, text_bg = self.edge_items[edge_key]
        self.canvas.delete(line)
        self.canvas.delete(text_item)
        self.canvas.delete(text_bg)
        # Elimina la arista del diccionario de items.
        del self.edge_items[edge_key]
        # Si fue una eliminación directa, actualiza estado y recalcula ruta.
        if confirm:
            self.instrucciones_actualizacion(f"Arista {n1}-{n2} eliminada.")
            self.ejercuta_automatico_modificar()

    # LÓGICA DE DIJKSTRA Y BÚSQUEDA DE RUTA - <---ECHO EN GRUPO CON MODIFICACION Y AYUDA DE IA-->

    def inicia_seleccion_1vertice(self, node_id): # Se ejecuta al hacer clic en el nodo inicial para buscar ruta
        self.start_node = node_id # Guarda el nodo inicial
        self.cambia_colorvertice(node_id, True) # Lo resalta
        self.mode = "path_end" # Cambia al modo "esperando nodo final"
        name = self.node_display_names[node_id]
        self.instrucciones_actualizacion(f"Nodo INICIAL: '{name}'. Haz clic en el nodo FINAL.")

    def finaliza_seleccion_2vertice(self, node_id): #Se ejecuta al hacer clic en el nodo final
        if node_id == self.start_node: # No permite que inicio y fin sean el mismo.
            self.instrucciones_actualizacion("Error: El nodo final no puede ser igual al inicial.")
            return

        self.end_node = node_id # Guarda el nodo final.
        self.cambia_colorvertice(node_id, True) # Lo resalta.
        start_name = self.node_display_names[self.start_node]
        end_name = self.node_display_names[self.end_node]
        self.instrucciones_actualizacion(f"Buscando ruta de '{start_name}' a '{end_name}'...")

        self.cerebro_dijkstra() # Ejecuta el algoritmo principal.

    def cerebro_dijkstra(self): #Implementación del algoritmo de Dijkstra
        # Comprueba si los nodos de inicio/fin son válidos y existen
        if self.start_node is None or self.end_node is None or \
           self.start_node not in self.node_coords or \
           self.end_node not in self.node_coords:
            self.restablecer_ruta() # Si no, limpia cualquier ruta anterior.
            return

        # Inicialización de estructuras de datos de Dijkstra.
        distances = {node: float('inf') for node in self.node_coords} # Distancias iniciales infinitas.
        previous_nodes = {node: None for node in self.node_coords} # Nodos previos desconocidos.
        distances[self.start_node] = 0 # Distancia al inicio es 0.
        # Cola de prioridad inicializada con (costo, nodo_inicial).
        pq = [(0, self.start_node)]
        path_found = False # Bandera para saber si se encontró la ruta.

        # Bucle principal: mientras haya nodos por visitar en la cola...
        while pq:
            # Saca el nodo con la distancia mas BAJA de la cola.
            current_dist, current_node = heapq.heappop(pq)

            # Optimización: Si encontramos una ruta mas corta a este nodo ANTES, ignoramos esta.
            if current_dist > distances[current_node]:
                continue

            # Si el nodo actual es el destino, ¡terminamos!
            if current_node == self.end_node:
                path_found = True
                break

            # Si no, explora los vecinos del nodo actual.
            # self.graph[current_node].items() devuelve los vecinos y el peso de la arista hacia ellos.
            # Funciona igual para grafos no dirigidos.
            for neighbor, weight in self.graph[current_node].items():
                # Calcula la distancia hasta el vecino A TRAVÉS del nodo actual.
                distance = current_dist + weight

                # Si esta nueva distancia es MEJOR (mas corta) que la que teníamos...
                if distance < distances[neighbor]:
                    distances[neighbor] = distance # Actualiza la distancia mas corta al vecino.
                    previous_nodes[neighbor] = current_node # Guarda que llegamos desde 'current_node'.
                    # Añade/actualiza el vecino en la cola de prioridad con su nueva distancia.
                    heapq.heappush(pq, (distance, neighbor))

        # --- Procesamiento de Resultados ---
        # Obtiene los nombres visibles para mostrar.
        start_name = self.node_display_names[self.start_node]
        end_name = self.node_display_names[self.end_node]

        # Si no se encontró ruta o el destino sigue siendo inalcanzable...
        if not path_found or distances[self.end_node] == float('inf'):
            self.instrucciones_actualizacion(f"No se encontro ruta desde '{start_name}' hasta '{end_name}'.")
            self.results_label.config(text=f"Ruta no encontrada:\nDe '{start_name}'\na '{end_name}'")
            self.borrar_lineasruta() # Borra la linea naranja si existía.
        else: # Si se encontró una ruta...
            # Reconstruye la ruta yendo hacia atrás desde el nodo final usando 'previous_nodes'.
            path = []
            current = self.end_node
            while current is not None:
                path.append(current)
                current = previous_nodes[current] # Sigue las "migajas de pan" hacia atrás.
            path.reverse() # Invierte la lista para tenerla en orden Inicio -> Fin.

            cost = distances[self.end_node] # Costo total.
            # Crea la cadena de texto de la ruta (ej. "A -> B -> C").
            path_str = " -> ".join([self.node_display_names[node] for node in path])

            # Actualiza la barra de estado y el panel de resultados.
            self.instrucciones_actualizacion(f"Ruta mas corta: {path_str} | Costo total: {cost}")
            self.results_label.config(text=f"Ruta Encontrada:\n{path_str}\n\nCosto Total: {cost}")

            # Dibuja la linea naranja en el canvas.
            self.dibuja_ruta(path)

    # FUNCIONES AUXILIARES - <---ECHO EN GRUPO --->

    def ejercuta_automatico_modificar(self): #Vuelve a ejecutar Dijkstra si hay una ruta activa en modificacion
        if self.start_node is not None and self.end_node is not None:
            self.borrar_lineasruta() # Borra la linea naranja anterior
            self.cerebro_dijkstra() # Ejecuta el algoritmo de nuevo

    def actualiza_aristas_movimiento_vertice(self, node_id): #edibuja todas las aristas conectadas a un nodo cuando este se mueve     
        keys_to_update = [] # Encuentra todas las claves de aristas que incluyen el nodo movido.
        for edge_key in self.edge_items:
            if node_id in edge_key:
                keys_to_update.append(edge_key)

        # Para cada arista conectada
        for key in keys_to_update:
            n1, n2 = key[0], key[1]
            # Obtiene las nuevas coordenadas de los nodos conectados
            x1, y1 = self.node_coords[n1]
            x2, y2 = self.node_coords[n2]
            # Obtiene las referencias a los items visuales de la arist
            line, text_item, text_bg = self.edge_items[key]
            # Actualiza las coordenadas de la linea
            self.canvas.coords(line, x1, y1, x2, y2)
            # Recalcula la posicion del texto del costo (para mantener el desplazamiento).
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            dx, dy = x2 - x1, y2 - y1
            length = math.sqrt(dx**2 + dy**2)
            if length == 0: length = 1
            unx, uny = -dy / length, dx / length
            text_x_pos = mid_x + unx * LABEL_OFFSET
            text_y_pos = mid_y + uny * LABEL_OFFSET
            # Actualiza las coordenadas del texto y su fondo.
            self.canvas.coords(text_item, text_x_pos, text_y_pos)
            self.canvas.coords(text_bg, text_x_pos - 10, text_y_pos - 8, text_x_pos + 10, text_y_pos + 8)

    def get_node_at(self, x, y): #Devuelve el ID del nodo en las coordenadas (x, y) del canvas o None
        for node_id, (nx, ny) in self.node_coords.items(): # Itera sobre todos los nodos existentes
            dist = math.sqrt((nx - x)**2 + (ny - y)**2) # Teorema de Pitágoras para calcular la distancia
            if dist <= NODE_RADIUS: # Si la distancia es menor o igual al radio el clic fue dentro
                return node_id
        return None # Si no se encontró ningun nodo

    def dibuja_ruta(self, path): #Dibuja las lineas naranjas que representan la ruta encontrada
        self.borrar_lineasruta() # Borra la ruta anterior.
        for i in range(len(path) - 1): # Itera sobre los pares de nodos consecutivos en la ruta.
            n1, n2 = path[i], path[i+1] # Nodos actual y siguiente.
            x1, y1 = self.node_coords[n1] # Coordenadas del nodo actual.
            x2, y2 = self.node_coords[n2] # Coordenadas del nodo siguiente.

            # Dibuja la linea naranja entre ellos.
            line = self.canvas.create_line(x1, y1, x2, y2, fill=PATH_COLOR, width=PATH_WIDTH)
            # Guarda la referencia a la linea para poder borrarla después.
            self.path_items.append(line)
            # Asegura que los nodos se dibujen encima de la linea naranja.
            self.canvas.tag_raise(f"node_{n1}")
            self.canvas.tag_raise(f"node_{n2}")

    def cambia_colorvertice(self, node_id, highlight=True): #Cambia el color de un nodo para resaltarlo (o quitar el resalte)
        if node_id not in self.node_items: # Si el nodo ya no existe.
            return
        oval, _text = self.node_items[node_id] # Obtiene el item del circulo
        # Elige el color basado en si se está resaltando o no
        color = HIGHLIGHT_COLOR if highlight else NODE_COLOR
        # Cambia el color de relleno del circulo
        self.canvas.itemconfig(oval, fill=color)

    def reset_selections(self): # Limpia la seleccion temporal usada al crear aristas
        if self.selected_node_1 is not None: # Si habia un nodo seleccionado...
            self.cambia_colorvertice(self.selected_node_1, False) # Le quita el resalte.
        self.selected_node_1 = None # Olvida el nodo seleccionado.

    def restablecer_ruta(self): #limpia la ruta activa (nodos de inicio/fin) y los resultados
        if self.start_node is not None: # Quita el resalte de los nodos de inicio y fin, si existen
            self.cambia_colorvertice(self.start_node, False)
        if self.end_node is not None:
            self.cambia_colorvertice(self.end_node, False)
        # Olvida los nodos de inicio y fin
        self.start_node = None
        self.end_node = None
        self.borrar_lineasruta() # Borra las lineas naranjas del canvas
        self.results_label.config(text="Resultados:\n---") # Resetea el panel de resultados

    def instrucciones_actualizacion(self, text): #Actualiza el texto de la barra de estado inferior
        self.status_label.config(text=text)

    def borrar_lineasruta(self): #Borra solo las lineas naranjas del canvas
        for item in self.path_items: # Itera sobre las lineas guardadas en self.path_items y las borra
            self.canvas.delete(item)
        self.path_items = [] # Vacia la lista

    def funcion_limpiar(self): #resetea completamente la aplicacion
        if not messagebox.askyesno("Confirmar Limpieza", "¿Seguro que deseas limpiar todo el lienzo?"):
            return  # Pide confirmación
        self.canvas.delete("all")  # Borra TODOS los items del canvas (nodos, aristas, ruta, fondo)
        self.Dibujo_cuadricula() # Vuelve a dibujar la cuadricula base
        self.restablecer_ruta() # Limpia la ruta activa y las selecciones temporales
        self.reset_selections()
        # vacia todas las estructuras de datos ("memoria")
        self.graph.clear()
        self.node_coords.clear()
        self.node_items.clear()
        self.edge_items.clear()
        self.node_display_names.clear()
        # Resetea el contador de nodos
        self.node_counter = 0
        # Vuelve al modo inicial ("Mover/Crear Nodo") y aplica el estilo
        self.modo_actual("nodes", "Modo: Mover/Crear Nodo. Arrastra un nodo para moverlo o haz clic en el lienzo para crear.")

    # FUNCIONES DE GUARDAR/CARGAR GRAFO - <---ECHO POR IA--->

    def save_graph(self): #Guarda el estado actual del grafo en un archivo JSON
        # Comprueba si hay algo que guardar.
        if not self.node_coords:
            messagebox.showwarning("Grafo Vacío", "No hay nada que guardar.")
            return

        # Abre el diálogo de "Guardar como..." y pide al usuario un nombre de archivo.
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json", # Extensión por defecto.
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")], # Filtro de archivos.
            title="Guardar grafo como..."
        )
        if not filepath: return # Si el usuario cancela.

        # --- Prepara los datos para guardar ---
        # 1. Guarda la información de cada nodo (ID, nombre, coordenadas).
        nodes_data = []
        for node_id, coords in self.node_coords.items():
            nodes_data.append({
                "id": node_id,
                "name": self.node_display_names[node_id],
                "x": coords[0],
                "y": coords[1]
            })

        # 2. Guarda la información de cada arista (origen, destino, peso).
        edges_data = []
        processed_edges = set() # Ayuda a evitar duplicados en grafos no dirigidos.
        # Itera sobre el grafo lógico.
        for u, neighbors in self.graph.items(): # u = nodo origen
            for v, weight in neighbors.items(): # v = nodo destino, weight = peso
                # Determina la clave única de la arista (siempre ordenada).
                edge_key = tuple(sorted((u, v))) # Modificado para ser siempre no dirigido
                # Si no hemos guardado ya esta arista...
                if edge_key not in processed_edges:
                    edges_data.append({"from": u, "to": v, "weight": weight})
                    processed_edges.add(edge_key) # Marca la arista como guardada.

        # 3. Crea el diccionario final que se guardará en el archivo.
        data_to_save = {
            "node_counter": self.node_counter, # Guarda el último ID usado.
            # "is_directed" fue eliminado.
            "nodes": nodes_data, # Lista de nodos.
            "edges": edges_data  # Lista de aristas.
        }

        # --- Escribe los datos en el archivo JSON ---
        try:
            # Abre el archivo en modo escritura ('w').
            with open(filepath, 'w') as f:
                # Usa json.dump para escribir el diccionario en formato JSON legible.
                json.dump(data_to_save, f, indent=4)
            self.instrucciones_actualizacion(f"Grafo guardado en '{filepath.split('/')[-1]}'")
        except Exception as e:
            # Muestra un error si falla la escritura.
            messagebox.showerror("Error al Guardar", f"No se pudo guardar el archivo:\n{e}")

    def load_graph(self): #Carga un grafo desde un archivo JSON, reemplazando el grafo actual
        # Advierte al usuario si el lienzo no está vacío.
        if self.node_coords and not messagebox.askyesno("Cargar Grafo", "¿Seguro que deseas cargar un nuevo grafo?\nEl grafo actual se perderá."):
            return

        # Abre el diálogo de "Abrir..." y pide al usuario que seleccione un archivo JSON.
        filepath = filedialog.askopenfilename(
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
            title="Cargar grafo desde archivo"
        )
        if not filepath: return # Si el usuario cancela.

        # --- Lee los datos del archivo JSON ---
        try:
            # Abre el archivo en modo lectura ('r').
            with open(filepath, 'r') as f:
                # Usa json.load para leer el archivo y convertirlo de nuevo en un diccionario Python.
                data = json.load(f)
        except Exception as e:
            # Muestra un error si falla la lectura o el formato no es JSON válido.
            messagebox.showerror("Error al Cargar", f"No se pudo leer o procesar el archivo:\n{e}")
            return

        # --- Reconstruye el estado de la aplicación a partir de los datos cargados ---
        self.funcion_limpiar() # ¡Importante! Limpia todo antes de empezar a cargar.

        try:
            # 1. Carga el estado general (contador de nodos).
            self.node_counter = data["node_counter"]
            # self.is_directed.set(...) fue eliminado.

            # 2. Reconstruye los Nodos (lógica y visualmente).
            for node_data in data["nodes"]:
                node_id = node_data["id"]
                name = node_data["name"]
                x = node_data["x"]
                y = node_data["y"]
                # Guarda los datos en las variables de estado.
                self.node_coords[node_id] = (x, y)
                self.node_display_names[node_id] = name
                # Dibuja el nodo en el canvas (similar a crear_vertice).
                tag = f"node_{node_id}"
                oval = self.canvas.create_oval(x - NODE_RADIUS, y - NODE_RADIUS, x + NODE_RADIUS, y + NODE_RADIUS, fill=NODE_COLOR, outline="", tags=(tag,))
                text = self.canvas.create_text(x, y, text=name, fill=NODE_TEXT_COLOR, font=("Arial", 10, "bold"), tags=(tag,))
                self.node_items[node_id] = (oval, text) # Guarda las referencias visuales.

            # 3. Reconstruye las Aristas (lógica y visualmente).
            for edge_data in data["edges"]:
                u = edge_data["from"]
                v = edge_data["to"]
                weight = edge_data["weight"]
                # Añade la arista al grafo lógico (en AMBAS direcciones).
                self.graph[u][v] = weight
                self.graph[v][u] = weight

                # Dibuja la arista en el canvas (sin flecha).
                x1, y1 = self.node_coords[u]; x2, y2 = self.node_coords[v]
                arrow_shape = tk.NONE # Siempre sin flecha.
                line = self.canvas.create_line(x1, y1, x2, y2, fill=EDGE_COLOR, width=2, arrow=arrow_shape)
                text_item, text_bg = self.dibuja_costo_arista(x1, y1, x2, y2, str(weight))
                # Ajusta el orden de capas.
                self.canvas.tag_lower(text_bg, line)
                self.canvas.tag_raise(f"node_{u}"); self.canvas.tag_raise(f"node_{v}")

                # Guarda las referencias visuales y añade tags (con clave ordenada).
                edge_key = tuple(sorted((u, v))) # Siempre ordenada.
                tag = f"edge_{edge_key[0]}_{edge_key[1]}"
                for item in (text_bg, text_item):
                    self.canvas.addtag_withtag("edge_label", item)
                    self.canvas.addtag_withtag(tag, item)
                self.edge_items[edge_key] = (line, text_item, text_bg)

            # Actualiza la barra de estado.
            self.instrucciones_actualizacion(f"Grafo cargado desde '{filepath.split('/')[-1]}'")

        except KeyError as e:
            # Si el archivo JSON no tiene la estructura esperada (falta una clave).
            messagebox.showerror("Error de Formato", f"El archivo JSON no tiene el formato esperado. Falta la clave: {e}")
            self.funcion_limpiar() # Limpia el lienzo si la carga falla a mitad de camino.

def ventana_dijkstra():
    root_dijkstra = tk.Toplevel() # Usa Toplevel para crear una ventana secundaria independiente.
    app = DijkstraGUI(root_dijkstra) # Crea la interfaz de Dijkstra dentro de esa nueva ventana.

if __name__ == "__main__":
    root = tk.Tk()           # Crea la ventana principal de Tkinter.
    app = DijkstraGUI(root)  # Crea una instancia de nuestra clase, construyendo la interfaz.
    root.mainloop()          # Inicia el bucle de eventos de Tkinter (mantiene la ventana abierta y reactiva).