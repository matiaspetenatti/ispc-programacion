# Pestaña 1: Ejecutar Pedido
import sqlite3
from tkinter import messagebox, ttk

import customtkinter as ctk

import config
import pedidos


class TabPedido(ctk.CTkFrame):

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app          # para saber qué empleado ejecuta el pedido
        self.areas = {}         # texto del combo -> id_area
        # texto del combo -> (id_producto, nombre, stock)
        self.productos = {}
        # id_producto -> [nombre, cantidad] (el pedido en armado)
        self.items = {}

        ctk.CTkLabel(
            self,
            text="Ejecutar Pedido",
            font=config.FUENTE_SUBTITULO,
            text_color=config.COLOR_HEADER
        ).pack(pady=(5, 5))

        # --- Formulario ---
        frame_form = ctk.CTkFrame(self, fg_color="transparent")
        frame_form.pack(pady=2)

        ctk.CTkLabel(frame_form, text="Área solicitante:",
                     font=config.FUENTE_NORMAL).grid(row=0, column=0, sticky="w", pady=4)
        self.cb_area = ctk.CTkComboBox(frame_form, state="readonly", width=260)
        self.cb_area.grid(row=0, column=1, columnspan=2,
                          pady=4, padx=10, sticky="w")

        ctk.CTkLabel(frame_form, text="Producto:",
                     font=config.FUENTE_NORMAL).grid(row=1, column=0, sticky="w", pady=4)
        self.cb_prod = ctk.CTkComboBox(frame_form, state="readonly", width=260)
        self.cb_prod.grid(row=1, column=1, columnspan=2,
                          pady=4, padx=10, sticky="w")

        ctk.CTkLabel(frame_form, text="Cantidad:",
                     font=config.FUENTE_NORMAL).grid(row=2, column=0, sticky="w", pady=4)
        self.ent_cant = ctk.CTkEntry(frame_form, width=100)
        self.ent_cant.grid(row=2, column=1, pady=4, padx=10, sticky="w")

        ctk.CTkButton(
            frame_form,
            text="Agregar al pedido",
            font=config.FUENTE_BOTON,
            fg_color=config.COLOR_AZUL,
            hover_color=config.COLOR_AZUL_HOVER,
            width=150,
            command=self.agregar_item
        ).grid(row=2, column=2, pady=4)

        # --- Lista de productos del pedido ---
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
                                  show="headings", height=4)
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
            text="Ejecutar pedido",
            font=config.FUENTE_BOTON,
            fg_color=config.COLOR_VERDE,
            hover_color=config.COLOR_VERDE_HOVER,
            width=170,
            command=self.ejecutar_pedido
        ).pack(side="left", padx=8)

        self.cargar_combos()

    # ---------- Carga de datos desde la base ----------
    def cargar_combos(self):
        try:
            areas = pedidos.obtener_areas()
            productos = pedidos.obtener_productos()
        except sqlite3.Error as error:
            messagebox.showerror("Error de base de datos",
                                 f"No se pudieron cargar los datos:\n{error}")
            return

        area_actual = self.cb_area.get()
        self.areas = {nombre: id_area for id_area, nombre in areas}
        self.cb_area.configure(values=list(self.areas))
        if area_actual in self.areas:
            self.cb_area.set(area_actual)       # no perder lo que ya eligió
        else:
            self.cb_area.set("Seleccionar...")

        self.productos = {
            f"{nombre} (stock: {stock})": (id_producto, nombre, stock)
            for id_producto, nombre, stock in productos
        }
        self.cb_prod.configure(values=list(self.productos))
        self.cb_prod.set("Seleccionar...")

    # ---------- Armado del pedido ----------
    def agregar_item(self):
        area = self.cb_area.get()
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

        id_producto, nombre, stock = self.productos[producto]

        # Si el producto ya estaba en la lista, se suma (un producto aparece una vez por pedido)
        ya_pedido = self.items[id_producto][1] if id_producto in self.items else 0
        if ya_pedido + cantidad > stock:
            messagebox.showwarning(
                "Stock insuficiente",
                f"'{nombre}': hay {stock} en stock y ya se piden {ya_pedido}.\n"
                f"No se pueden agregar {cantidad} más.")
            return

        self.items[id_producto] = [nombre, ya_pedido + cantidad]
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
            # el id del producto se usa como identificador de la fila
            self.tabla.insert("", "end", iid=str(id_producto),
                              values=(nombre, cantidad))

    # ---------- Ejecución ----------
    def ejecutar_pedido(self):
        area = self.cb_area.get()
        if area not in self.areas:
            messagebox.showwarning("Datos incompletos",
                                   "Seleccione el área que solicita el pedido.")
            return
        if not self.items:
            messagebox.showwarning("Pedido vacío",
                                   "Agregue al menos un producto al pedido.")
            return

        if not messagebox.askyesno(
                "Confirmar pedido",
                f"¿Ejecutar el pedido para el área '{area}'?\n"
                "Se descontará el stock de los productos."):
            return

        id_area = self.areas[area]
        id_empleado = self.app.empleado_actual[0]
        lista = [(id_producto, datos[1])
                 for id_producto, datos in self.items.items()]

        try:
            id_pedido = pedidos.ejecutar_pedido(id_area, id_empleado, lista)
        except pedidos.StockInsuficiente as error:
            messagebox.showwarning("Stock insuficiente", str(error))
            self.cargar_combos()    # el stock pudo haber cambiado
            return
        except sqlite3.Error as error:
            messagebox.showerror("Error de base de datos",
                                 f"No se pudo registrar el pedido:\n{error}")
            return

        messagebox.showinfo("Pedido ejecutado",
                            f"Pedido N° {id_pedido} registrado para '{area}'.")
        self.items.clear()
        self.refrescar_tabla()
        self.ent_cant.delete(0, "end")
        self.cargar_combos()        # refresca el stock mostrado
