# Pestaña 2: Ingreso de Stock
import sqlite3
from tkinter import messagebox, ttk

import customtkinter as ctk

import compras
import config
import pedidos


class TabIngreso(ctk.CTkFrame):

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app          # para saber qué empleado recibe la mercadería
        self.proveedores = {}   # texto del combo -> id_proveedor
        self.productos = {}     # texto del combo -> (id_producto, nombre)
        # id_producto -> [nombre, cantidad] (el ingreso en armado)
        self.items = {}

        ctk.CTkLabel(
            self,
            text="Ingreso de Stock",
            font=config.FUENTE_SUBTITULO,
            text_color=config.COLOR_HEADER
        ).pack(pady=(5, 5))

        # --- Formulario ---
        frame_form = ctk.CTkFrame(self, fg_color="transparent")
        frame_form.pack(pady=2)

        ctk.CTkLabel(frame_form, text="Proveedor:",
                     font=config.FUENTE_NORMAL).grid(row=0, column=0, sticky="w", pady=4)
        self.cb_prov = ctk.CTkComboBox(frame_form, state="readonly", width=260)
        self.cb_prov.grid(row=0, column=1, columnspan=2,
                          pady=4, padx=10, sticky="w")

        ctk.CTkLabel(frame_form, text="N° de remito:",
                     font=config.FUENTE_NORMAL).grid(row=1, column=0, sticky="w", pady=4)
        self.ent_remito = ctk.CTkEntry(frame_form, width=260)
        self.ent_remito.grid(row=1, column=1, columnspan=2,
                             pady=4, padx=10, sticky="w")

        ctk.CTkLabel(frame_form, text="Producto:",
                     font=config.FUENTE_NORMAL).grid(row=2, column=0, sticky="w", pady=4)
        self.cb_prod = ctk.CTkComboBox(frame_form, state="readonly", width=260)
        self.cb_prod.grid(row=2, column=1, columnspan=2,
                          pady=4, padx=10, sticky="w")

        ctk.CTkLabel(frame_form, text="Cantidad:",
                     font=config.FUENTE_NORMAL).grid(row=3, column=0, sticky="w", pady=4)
        self.ent_cant = ctk.CTkEntry(frame_form, width=100)
        self.ent_cant.grid(row=3, column=1, pady=4, padx=10, sticky="w")

        ctk.CTkButton(
            frame_form,
            text="Agregar a la lista",
            font=config.FUENTE_BOTON,
            fg_color=config.COLOR_AZUL,
            hover_color=config.COLOR_AZUL_HOVER,
            width=150,
            command=self.agregar_item
        ).grid(row=3, column=2, pady=4)

        # --- Lista de productos del ingreso ---
        estilo = ttk.Style()
        estilo.theme_use("default")
        estilo.configure("Treeview", background="white", fieldbackground="white",
                         rowheight=26, borderwidth=0, font=("Arial", 11))
        estilo.configure("Treeview.Heading", background=config.COLOR_HEADER,
                         foreground="white", relief="flat", font=("Arial", 11, "bold"))
        estilo.map("Treeview", background=[("selected", config.COLOR_VERDE)])
        estilo.map("Treeview.Heading", background=[
                   ("active", config.COLOR_HEADER)])

        frame_tabla = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        frame_tabla.pack(padx=20, pady=6)

        self.tabla = ttk.Treeview(frame_tabla, columns=("Producto", "Cantidad"),
                                  show="headings", height=3)
        self.tabla.heading("Producto", text="Producto")
        self.tabla.heading("Cantidad", text="Cantidad")
        self.tabla.column("Producto", anchor="center", width=300)
        self.tabla.column("Cantidad", anchor="center", width=120)
        self.tabla.pack(padx=6, pady=6)

        # --- Botones ---
        frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        frame_botones.pack(pady=4)

        ctk.CTkButton(
            frame_botones,
            text="Quitar seleccionado",
            font=config.FUENTE_BOTON,
            fg_color=config.COLOR_ROJO,
            hover_color=config.COLOR_ROJO_HOVER,
            width=170,
            command=self.quitar_item
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            frame_botones,
            text="Guardar Ingreso",
            font=config.FUENTE_BOTON,
            fg_color=config.COLOR_VERDE,
            hover_color=config.COLOR_VERDE_HOVER,
            width=170,
            command=self.guardar_ingreso
        ).pack(side="left", padx=8)

        self.cargar_combos()

    # ---------- Carga de datos desde la base ----------
    def cargar_combos(self):
        """Lee proveedores y productos de la base (conserva el proveedor elegido)."""
        try:
            proveedores = compras.obtener_proveedores()
            productos = pedidos.obtener_productos()
        except sqlite3.Error as error:
            messagebox.showerror("Error de base de datos",
                                 f"No se pudieron cargar los datos:\n{error}")
            return

        proveedor_actual = self.cb_prov.get()
        self.proveedores = {nombre: id_prov for id_prov, nombre in proveedores}
        self.cb_prov.configure(values=list(self.proveedores))
        if proveedor_actual in self.proveedores:
            self.cb_prov.set(proveedor_actual)
        else:
            self.cb_prov.set("Seleccionar...")

        self.productos = {
            f"{nombre} (stock: {stock})": (id_producto, nombre)
            for id_producto, nombre, stock in productos
        }
        self.cb_prod.configure(values=list(self.productos))
        self.cb_prod.set("Seleccionar...")

    # ---------- Armado del ingreso ----------
    def agregar_item(self):
        producto = self.cb_prod.get()
        texto_cant = self.ent_cant.get().strip()

        if producto not in self.productos:
            messagebox.showwarning("Datos incompletos",
                                   "Seleccione un producto.")
            return

        if not texto_cant.isdigit() or int(texto_cant) <= 0:
            messagebox.showwarning("Cantidad inválida",
                                   "La cantidad debe ser un número entero mayor a 0.")
            self.ent_cant.focus()
            return
        cantidad = int(texto_cant)

        id_producto, nombre = self.productos[producto]

        # Si el producto ya estaba en la lista, se suma (aparece una vez por compra)
        ya_cargado = self.items[id_producto][1] if id_producto in self.items else 0
        self.items[id_producto] = [nombre, ya_cargado + cantidad]

        self.refrescar_tabla()
        self.cb_prod.set("Seleccionar...")
        self.ent_cant.delete(0, "end")

    def quitar_item(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección",
                                   "Seleccione un producto de la lista para quitarlo.")
            return
        self.items.pop(int(seleccion[0]), None)
        self.refrescar_tabla()

    def refrescar_tabla(self):
        self.tabla.delete(*self.tabla.get_children())
        for id_producto, (nombre, cantidad) in self.items.items():
            self.tabla.insert("", "end", iid=str(id_producto),
                              values=(nombre, cantidad))

    # ---------- Guardado ----------
    def guardar_ingreso(self):
        proveedor = self.cb_prov.get()
        remito = self.ent_remito.get().strip()

        if proveedor not in self.proveedores:
            messagebox.showwarning("Datos incompletos",
                                   "Seleccione el proveedor.")
            return
        if remito == "":
            messagebox.showwarning("Datos incompletos",
                                   "Ingrese el número de remito.")
            self.ent_remito.focus()
            return
        if not self.items:
            messagebox.showwarning("Ingreso vacío",
                                   "Agregue al menos un producto a la lista.")
            return

        if not messagebox.askyesno(
                "Confirmar ingreso",
                f"¿Registrar el ingreso del remito {remito} de '{proveedor}'?\n"
                "Se sumará el stock de los productos."):
            return

        id_proveedor = self.proveedores[proveedor]
        id_empleado = self.app.empleado_actual[0]
        lista = [(id_producto, datos[1])
                 for id_producto, datos in self.items.items()]

        try:
            id_compra = compras.registrar_ingreso(id_proveedor, remito,
                                                  id_empleado, lista)
        except sqlite3.Error as error:
            messagebox.showerror("Error de base de datos",
                                 f"No se pudo registrar el ingreso:\n{error}")
            return

        messagebox.showinfo("Ingreso registrado",
                            f"Ingreso N° {id_compra} registrado correctamente.")
        self.items.clear()
        self.refrescar_tabla()
        self.ent_remito.delete(0, "end")
        self.ent_cant.delete(0, "end")
        self.cargar_combos()        # refresca el stock mostrado
