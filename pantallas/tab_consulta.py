# Pestaña 3: Ver Stock
import sqlite3
from tkinter import messagebox, ttk

import customtkinter as ctk

import config
import productos


class TabConsulta(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        # Fila superior: título + botón Actualizar
        frame_titulo = ctk.CTkFrame(self, fg_color="transparent")
        frame_titulo.pack(fill="x", padx=20, pady=(5, 5))

        ctk.CTkLabel(
            frame_titulo,
            text="Ver Stock",
            font=config.FUENTE_SUBTITULO,
            text_color=config.COLOR_HEADER
        ).pack(side="left")

        ctk.CTkButton(
            frame_titulo,
            text="Actualizar",
            font=config.FUENTE_BOTON,
            fg_color=config.COLOR_AZUL,
            hover_color=config.COLOR_AZUL_HOVER,
            width=120,
            command=self.cargar_stock
        ).pack(side="right")

        estilo = ttk.Style()
        estilo.theme_use("default")
        estilo.configure("Treeview", background="white", fieldbackground="white",
                         rowheight=26, borderwidth=0, font=("Arial", 11))
        estilo.configure("Treeview.Heading", background=config.COLOR_HEADER,
                         foreground="white", relief="flat", font=("Arial", 11, "bold"))
        estilo.map("Treeview", background=[("selected", config.COLOR_VERDE)])
        estilo.map("Treeview.Heading", background=[
                   ("active", config.COLOR_HEADER)])

        # Tabla visual (Treeview) con barra de desplazamiento
        frame_tabla = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        frame_tabla.pack(padx=20, pady=5)

        columnas = ("Producto", "Marca", "Ubicación", "Stock")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas,
                                  show="headings", height=9)
        anchos = (220, 120, 120, 80)
        for columna, ancho in zip(columnas, anchos):
            self.tabla.heading(columna, text=columna)
            self.tabla.column(columna, anchor="center", width=ancho)

        barra = ctk.CTkScrollbar(frame_tabla, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra.set)

        self.tabla.pack(side="left", padx=(8, 0), pady=8)
        barra.pack(side="right", fill="y", padx=(0, 4), pady=8)

        self.cargar_stock()

    def cargar_stock(self):
        try:
            filas = productos.obtener_stock()
        except sqlite3.Error as error:
            messagebox.showerror("Error de base de datos",
                                 f"No se pudo consultar el stock:\n{error}")
            return

        self.tabla.delete(*self.tabla.get_children())
        for fila in filas:
            self.tabla.insert("", "end", values=fila)
