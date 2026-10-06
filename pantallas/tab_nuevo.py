# Pestaña 4: Agregar Producto
from tkinter import messagebox
import customtkinter as ctk
import config


class TabNuevo(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        ctk.CTkLabel(
            self,
            text="Agregar Producto",
            font=config.FUENTE_SUBTITULO,
            text_color=config.COLOR_HEADER
        ).pack(pady=15)

        frame_form = ctk.CTkFrame(self, fg_color="transparent")
        frame_form.pack(pady=10)

        ctk.CTkLabel(frame_form, text="Nombre del Producto:",
                     font=config.FUENTE_NORMAL).grid(row=0, column=0, sticky="w", pady=8)
        self.ent_nombre = ctk.CTkEntry(frame_form, width=220)
        self.ent_nombre.grid(row=0, column=1, pady=8, padx=10)

        ctk.CTkLabel(frame_form, text="Cantidad Inicial:",
                     font=config.FUENTE_NORMAL).grid(row=1, column=0, sticky="w", pady=8)
        self.ent_stock = ctk.CTkEntry(frame_form, width=220)
        self.ent_stock.grid(row=1, column=1, pady=8, padx=10)

        btn_guardar = ctk.CTkButton(
            self,
            text="Agregar",
            font=config.FUENTE_BOTON,
            fg_color=config.COLOR_VIOLETA,
            hover_color=config.COLOR_VIOLETA_HOVER,
            width=180,
            command=self.agregar_producto
        )
        btn_guardar.pack(pady=20)

    def agregar_producto(self):
        messagebox.showinfo(
            "Navegación", "Acción simulada: Producto agregado.")
