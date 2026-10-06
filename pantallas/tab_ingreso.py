# Pestaña 2: Ingreso de Stock
from tkinter import messagebox

import customtkinter as ctk

import config
import datos


class TabIngreso(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        ctk.CTkLabel(
            self,
            text="Ingreso de Stock",
            font=config.FUENTE_SUBTITULO,
            text_color=config.COLOR_HEADER
        ).pack(pady=15)

        frame_form = ctk.CTkFrame(self, fg_color="transparent")
        frame_form.pack(pady=10)

        ctk.CTkLabel(frame_form, text="Proveedor:",
                     font=config.FUENTE_NORMAL).grid(row=0, column=0, sticky="w", pady=8)
        self.ent_prov = ctk.CTkEntry(frame_form, width=220)
        self.ent_prov.grid(row=0, column=1, pady=8, padx=10)

        ctk.CTkLabel(frame_form, text="Seleccionar producto:",
                     font=config.FUENTE_NORMAL).grid(row=1, column=0, sticky="w", pady=8)
        self.cb_prod = ctk.CTkComboBox(frame_form, state="readonly",
                                       width=220, values=datos.productos_demo)
        self.cb_prod.set("Seleccionar...")
        self.cb_prod.grid(row=1, column=1, pady=8, padx=10)

        ctk.CTkLabel(frame_form, text="Cantidad:",
                     font=config.FUENTE_NORMAL).grid(row=2, column=0, sticky="w", pady=8)
        self.ent_cant = ctk.CTkEntry(frame_form, width=220)
        self.ent_cant.grid(row=2, column=1, pady=8, padx=10)

        btn_ingresar = ctk.CTkButton(
            self,
            text="Guardar Ingreso",
            font=config.FUENTE_BOTON,
            fg_color=config.COLOR_AZUL,
            hover_color=config.COLOR_AZUL_HOVER,
            width=180,
            command=self.guardar_ingreso
        )
        btn_ingresar.pack(pady=20)

    def guardar_ingreso(self):
        messagebox.showinfo("Navegación", "Acción simulada: Stock ingresado.")
