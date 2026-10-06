# Pestaña 3: Ver Cantidad de Productos
from tkinter import ttk

import customtkinter as ctk

import config
import datos


class TabConsulta(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        ctk.CTkLabel(
            self,
            text="Ver Cantidad de Productos",
            font=config.FUENTE_SUBTITULO,
            text_color=config.COLOR_HEADER
        ).pack(pady=15)

        estilo = ttk.Style()
        estilo.theme_use("default")
        estilo.configure("Treeview", background="white", fieldbackground="white",
                         rowheight=30, borderwidth=0, font=("Arial", 11))
        estilo.configure("Treeview.Heading", background=config.COLOR_HEADER,
                         foreground="white", relief="flat", font=("Arial", 11, "bold"))
        estilo.map("Treeview", background=[("selected", config.COLOR_VERDE)])
        estilo.map("Treeview.Heading", background=[
                   ("active", config.COLOR_HEADER)])

        # Tabla visual (Treeview)
        frame_tabla = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        frame_tabla.pack(padx=20, pady=10)

        columnas = ("Producto", "Cantidad")
        tabla = ttk.Treeview(frame_tabla, columns=columnas,
                             show="headings", height=6)
        tabla.heading("Producto", text="Producto")
        tabla.heading("Cantidad", text="Cantidad")
        tabla.column("Producto", anchor="center", width=260)
        tabla.column("Cantidad", anchor="center", width=160)

        # Datos estáticos de muestra
        for item in datos.datos_ejemplo:
            tabla.insert("", "end", values=item)

        tabla.pack(padx=8, pady=8)
