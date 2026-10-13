# Pestaña 5: Historial de Pedidos
import sqlite3
from tkinter import messagebox, ttk

import customtkinter as ctk

import config
import pedidos


class TabHistorial(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        ctk.CTkLabel(
            self,
            text="Historial de Pedidos",
            font=config.FUENTE_SUBTITULO,
            text_color=config.COLOR_HEADER
        ).pack(pady=(5, 5))

        estilo = ttk.Style()
        estilo.theme_use("default")
        estilo.configure("Treeview", background="white", fieldbackground="white",
                         rowheight=26, borderwidth=0, font=("Arial", 11))
        estilo.configure("Treeview.Heading", background=config.COLOR_HEADER,
                         foreground="white", relief="flat", font=("Arial", 11, "bold"))
        estilo.map("Treeview", background=[("selected", config.COLOR_VERDE)])
        estilo.map("Treeview.Heading", background=[
                   ("active", config.COLOR_HEADER)])

        # --- Lista de pedidos ---
        frame_pedidos = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        frame_pedidos.pack(padx=20, pady=4)

        columnas = ("N°", "Fecha", "Área", "Empleado", "Estado", "Unidades")
        self.tabla = ttk.Treeview(frame_pedidos, columns=columnas,
                                  show="headings", height=5)
        anchos = (50, 140, 120, 120, 80, 70)
        for columna, ancho in zip(columnas, anchos):
            self.tabla.heading(columna, text=columna)
            self.tabla.column(columna, anchor="center", width=ancho)
        self.tabla.pack(padx=6, pady=6)
        self.tabla.bind("<<TreeviewSelect>>", self.mostrar_detalle)

        # --- Detalle del pedido seleccionado ---
        self.lbl_detalle = ctk.CTkLabel(
            self, text="Seleccione un pedido para ver su detalle",
            font=config.FUENTE_NORMAL, text_color=config.COLOR_HEADER)
        self.lbl_detalle.pack(pady=(4, 2))

        frame_detalle = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        frame_detalle.pack(padx=20, pady=2)

        self.tabla_detalle = ttk.Treeview(frame_detalle,
                                          columns=("Producto", "Cantidad"),
                                          show="headings", height=4)
        self.tabla_detalle.heading("Producto", text="Producto")
        self.tabla_detalle.heading("Cantidad", text="Cantidad")
        self.tabla_detalle.column("Producto", anchor="center", width=300)
        self.tabla_detalle.column("Cantidad", anchor="center", width=120)
        self.tabla_detalle.pack(padx=6, pady=6)

        ctk.CTkButton(
            self,
            text="Actualizar",
            font=config.FUENTE_BOTON,
            fg_color=config.COLOR_AZUL,
            hover_color=config.COLOR_AZUL_HOVER,
            width=150,
            command=self.cargar_historial
        ).pack(pady=4)

        self.cargar_historial()

    def cargar_historial(self):
        try:
            historial = pedidos.obtener_historial()
        except sqlite3.Error as error:
            messagebox.showerror("Error de base de datos",
                                 f"No se pudo cargar el historial:\n{error}")
            return

        self.tabla.delete(*self.tabla.get_children())
        self.limpiar_detalle()
        for fila in historial:
            # el id del pedido se usa como identificador de la fila
            self.tabla.insert("", "end", iid=str(fila[0]), values=fila)

    def limpiar_detalle(self):
        self.tabla_detalle.delete(*self.tabla_detalle.get_children())
        self.lbl_detalle.configure(
            text="Seleccione un pedido para ver su detalle")

    def mostrar_detalle(self, evento=None):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        id_pedido = int(seleccion[0])

        try:
            detalle = pedidos.obtener_detalle(id_pedido)
        except sqlite3.Error as error:
            messagebox.showerror("Error de base de datos",
                                 f"No se pudo cargar el detalle:\n{error}")
            return

        self.tabla_detalle.delete(*self.tabla_detalle.get_children())
        for fila in detalle:
            self.tabla_detalle.insert("", "end", values=fila)
        self.lbl_detalle.configure(text=f"Detalle del pedido N° {id_pedido}")
