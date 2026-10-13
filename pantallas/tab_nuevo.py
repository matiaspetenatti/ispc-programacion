# Pestaña 4: Agregar Producto
import sqlite3
from tkinter import messagebox

import customtkinter as ctk

import config
import productos


class TabNuevo(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.marcas = []    # nombres de marcas que ya existen en la base

        ctk.CTkLabel(
            self,
            text="Agregar Producto",
            font=config.FUENTE_SUBTITULO,
            text_color=config.COLOR_HEADER
        ).pack(pady=(5, 5))

        frame_form = ctk.CTkFrame(self, fg_color="transparent")
        frame_form.pack(pady=5)

        ctk.CTkLabel(frame_form, text="Nombre del Producto:",
                     font=config.FUENTE_NORMAL).grid(row=0, column=0, sticky="w", pady=6)
        self.ent_nombre = ctk.CTkEntry(frame_form, width=260)
        self.ent_nombre.grid(row=0, column=1, pady=6, padx=10)

        # Combo editable: se elige una marca existente o se escribe una nueva
        ctk.CTkLabel(frame_form, text="Marca:",
                     font=config.FUENTE_NORMAL).grid(row=1, column=0, sticky="w", pady=6)
        self.cb_marca = ctk.CTkComboBox(frame_form, width=260)
        self.cb_marca.grid(row=1, column=1, pady=6, padx=10)

        ctk.CTkLabel(frame_form, text="Ubicación (opcional):",
                     font=config.FUENTE_NORMAL).grid(row=2, column=0, sticky="w", pady=6)
        self.ent_ubicacion = ctk.CTkEntry(frame_form, width=260)
        self.ent_ubicacion.grid(row=2, column=1, pady=6, padx=10)

        ctk.CTkLabel(frame_form, text="Descripción (opcional):",
                     font=config.FUENTE_NORMAL).grid(row=3, column=0, sticky="w", pady=6)
        self.ent_descripcion = ctk.CTkEntry(frame_form, width=260)
        self.ent_descripcion.grid(row=3, column=1, pady=6, padx=10)

        ctk.CTkLabel(frame_form, text="Cantidad Inicial:",
                     font=config.FUENTE_NORMAL).grid(row=4, column=0, sticky="w", pady=6)
        self.ent_stock = ctk.CTkEntry(frame_form, width=260)
        self.ent_stock.grid(row=4, column=1, pady=6, padx=10)

        btn_guardar = ctk.CTkButton(
            self,
            text="Agregar",
            font=config.FUENTE_BOTON,
            fg_color=config.COLOR_VIOLETA,
            hover_color=config.COLOR_VIOLETA_HOVER,
            width=180,
            command=self.agregar_producto
        )
        btn_guardar.pack(pady=10)

        self.cargar_marcas()

    def cargar_marcas(self):
        try:
            self.marcas = productos.obtener_marcas()
        except sqlite3.Error as error:
            messagebox.showerror("Error de base de datos",
                                 f"No se pudieron cargar las marcas:\n{error}")
            return
        self.cb_marca.configure(values=self.marcas)
        self.cb_marca.set("")

    def agregar_producto(self):
        nombre = self.ent_nombre.get().strip()
        marca = self.cb_marca.get().strip()
        ubicacion = self.ent_ubicacion.get().strip()
        descripcion = self.ent_descripcion.get().strip()
        texto_stock = self.ent_stock.get().strip()

        if nombre == "":
            messagebox.showwarning("Datos incompletos",
                                   "Ingrese el nombre del producto.")
            self.ent_nombre.focus()
            return

        if marca == "":
            messagebox.showwarning("Datos incompletos",
                                   "Elija o escriba la marca del producto.")
            return

        # Si lo deja vacío se toma como 0
        if texto_stock == "":
            texto_stock = "0"
        if not texto_stock.isdigit():
            messagebox.showwarning("Cantidad inválida",
                                   "La cantidad inicial debe ser un número entero (0 o más).")
            self.ent_stock.focus()
            return
        stock_inicial = int(texto_stock)

        # Si la marca es nueva, confirmar (evita crear marcas por un error de tipeo)
        if marca.casefold() not in [m.casefold() for m in self.marcas]:
            if not messagebox.askyesno(
                    "Marca nueva",
                    f"La marca '{marca}' todavía no existe.\n¿Desea crearla?"):
                return

        try:
            productos.crear_producto(nombre, marca, ubicacion,
                                     descripcion, stock_inicial)
        except productos.ProductoDuplicado as error:
            messagebox.showwarning("Producto existente", str(error))
            self.ent_nombre.focus()
            return
        except sqlite3.Error as error:
            messagebox.showerror("Error de base de datos",
                                 f"No se pudo agregar el producto:\n{error}")
            return

        messagebox.showinfo("Producto agregado",
                            f"'{nombre}' se agregó con {stock_inicial} unidades.")
        for campo in (self.ent_nombre, self.ent_ubicacion,
                      self.ent_descripcion, self.ent_stock):
            campo.delete(0, "end")
        self.cargar_marcas()    # por si se creó una marca nueva
