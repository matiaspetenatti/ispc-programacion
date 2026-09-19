import tkinter as tk
from tkinter import messagebox, ttk


class SistemaControlStock(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Control de Stock - ISPC")
        self.geometry("650x480")
        self.configure(bg="#A2D9CE")

        # Datos de ejemplo
        self.productos_demo = [
            "Tornillo M6",
            "Tuerca M6",
            "Placa Base A1",
            "Soporte Motor",
            "Espina M8",
            "Resorte",
            "Oring",
            "Cables 1,5mm",
            "Cable 3mm",
            "Reguladores de caudal"

        ]

        self.pantalla_login()

    # PANTALLA 1: LOGIN
    def pantalla_login(self):
        self.limpiar_pantalla()

        frame_login = tk.Frame(self, bg="#A2D9CE")
        frame_login.pack(expand=True)

        tk.Label(
            frame_login,
            text="Control de Stock",
            font=("Arial", 18, "bold"),
            bg="#A2D9CE",
            fg="#1B4F72"
        ).pack(pady=20)

        tk.Label(frame_login, text="Usuario:", font=(
            "Arial", 11), bg="#A2D9CE").pack(anchor="w")
        self.ent_usuario = tk.Entry(frame_login, font=("Arial", 11), width=25)
        self.ent_usuario.pack(pady=5)

        tk.Label(frame_login, text="Contraseña:", font=(
            "Arial", 11), bg="#A2D9CE").pack(anchor="w")
        self.ent_clave = tk.Entry(frame_login, font=(
            "Arial", 11), width=25, show="*")
        self.ent_clave.pack(pady=5)

        btn_ingresar = tk.Button(
            frame_login,
            text="Ingresar",
            font=("Arial", 11, "bold"),
            bg="#27AE60",
            fg="white",
            width=15,
            command=self.validar_login
        )
        btn_ingresar.pack(pady=20)

    def validar_login(self):
        # Simulamos un login valido y pasamos a la pantalla principal
        self.pantalla_principal()

    # PANTALLA PRINCIPAL: PESTAÑAS Y NAVEGACIÓN
    def pantalla_principal(self):
        self.limpiar_pantalla()

        # Encabezado
        header = tk.Frame(self, bg="#1B4F72", height=40)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Control de Stock - Panel General",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#1B4F72"
        ).pack(side="left", padx=10, pady=5)

        btn_salir = tk.Button(
            header,
            text="Cerrar Sesión",
            bg="#C0392B",
            fg="white",
            command=self.pantalla_login
        )
        btn_salir.pack(side="right", padx=10, pady=5)

        # Contenedor de Pestañas
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Pestañas
        self.tab_pedido = tk.Frame(notebook, bg="#E8F8F5")
        self.tab_ingreso = tk.Frame(notebook, bg="#E8F8F5")
        self.tab_consulta = tk.Frame(notebook, bg="#E8F8F5")
        self.tab_nuevo = tk.Frame(notebook, bg="#E8F8F5")

        notebook.add(self.tab_pedido, text="Ejecutar Pedido")
        notebook.add(self.tab_ingreso, text="Ingreso de Stock")
        notebook.add(self.tab_consulta, text="Ver Stock")
        notebook.add(self.tab_nuevo, text="Agregar Producto")

        self.build_tab_pedido()
        self.build_tab_ingreso()
        self.build_tab_consulta()
        self.build_tab_nuevo()

    # Pestaña 1: Ejecutar Pedido
    def build_tab_pedido(self):
        tk.Label(
            self.tab_pedido,
            text="Ejecutar Pedido",
            font=("Arial", 14, "bold"),
            bg="#E8F8F5"
        ).pack(pady=15)

        frame_form = tk.Frame(self.tab_pedido, bg="#E8F8F5")
        frame_form.pack(pady=10)

        tk.Label(frame_form, text="Seleccionar producto:", bg="#E8F8F5", font=(
            "Arial", 11)).grid(row=0, column=0, sticky="w", pady=8)
        cb_prod = ttk.Combobox(frame_form, state="readonly",
                               width=25, values=self.productos_demo)
        cb_prod.grid(row=0, column=1, pady=8, padx=10)

        tk.Label(frame_form, text="Cantidad:", bg="#E8F8F5", font=(
            "Arial", 11)).grid(row=1, column=0, sticky="w", pady=8)
        ent_cant = tk.Entry(frame_form, width=27)
        ent_cant.grid(row=1, column=1, pady=8, padx=10)

        btn_ejecutar = tk.Button(
            self.tab_pedido,
            text="Ejecutar pedido",
            font=("Arial", 10, "bold"),
            bg="#27AE60",
            fg="white",
            width=18,
            command=lambda: messagebox.showinfo(
                "Navegación", "Acción simulada: Pedido ejecutado.")
        )
        btn_ejecutar.pack(pady=20)

    # Pestaña 2: Ingreso de Stock
    def build_tab_ingreso(self):
        tk.Label(
            self.tab_ingreso,
            text="Ingreso de Stock",
            font=("Arial", 14, "bold"),
            bg="#E8F8F5"
        ).pack(pady=15)

        frame_form = tk.Frame(self.tab_ingreso, bg="#E8F8F5")
        frame_form.pack(pady=10)

        tk.Label(frame_form, text="Proveedor:", bg="#E8F8F5", font=(
            "Arial", 11)).grid(row=0, column=0, sticky="w", pady=8)
        ent_prov = tk.Entry(frame_form, width=27)
        ent_prov.grid(row=0, column=1, pady=8, padx=10)

        tk.Label(frame_form, text="Seleccionar producto:", bg="#E8F8F5", font=(
            "Arial", 11)).grid(row=1, column=0, sticky="w", pady=8)
        cb_prod = ttk.Combobox(frame_form, state="readonly",
                               width=25, values=self.productos_demo)
        cb_prod.grid(row=1, column=1, pady=8, padx=10)

        tk.Label(frame_form, text="Cantidad:", bg="#E8F8F5", font=(
            "Arial", 11)).grid(row=2, column=0, sticky="w", pady=8)
        ent_cant = tk.Entry(frame_form, width=27)
        ent_cant.grid(row=2, column=1, pady=8, padx=10)

        btn_ingresar = tk.Button(
            self.tab_ingreso,
            text="Guardar Ingreso",
            font=("Arial", 10, "bold"),
            bg="#2980B9",
            fg="white",
            width=18,
            command=lambda: messagebox.showinfo(
                "Navegación", "Acción simulada: Stock ingresado.")
        )
        btn_ingresar.pack(pady=20)

    # Pestaña 3: Ver Cantidad de Productos
    def build_tab_consulta(self):
        tk.Label(
            self.tab_consulta,
            text="Ver Cantidad de Productos",
            font=("Arial", 14, "bold"),
            bg="#E8F8F5"
        ).pack(pady=15)

        # Tabla visual (Treeview)
        columnas = ("Producto", "Cantidad")
        tabla = ttk.Treeview(
            self.tab_consulta, columns=columnas, show="headings", height=6)

        tabla.heading("Producto", text="Producto")
        tabla.heading("Cantidad", text="Cantidad")
        tabla.column("Producto", anchor="center", width=250)
        tabla.column("Cantidad", anchor="center", width=150)

        # Datos estáticos de muestra
        datos_ejemplo = [
            ("Tornillo M6", "100 unidades"),
            ("Tuerca M6", "250 unidades"),
            ("Placa Base A1", "15 unidades"),
            ("Soporte Motor", "8 unidades")
        ]

        for item in datos_ejemplo:
            tabla.insert("", tk.END, values=item)

        tabla.pack(padx=20, pady=10)

    # Pestaña 4: Agregar Producto
    def build_tab_nuevo(self):
        tk.Label(
            self.tab_nuevo,
            text="Agregar Producto",
            font=("Arial", 14, "bold"),
            bg="#E8F8F5"
        ).pack(pady=15)

        frame_form = tk.Frame(self.tab_nuevo, bg="#E8F8F5")
        frame_form.pack(pady=10)

        tk.Label(frame_form, text="Nombre del Producto:", bg="#E8F8F5",
                 font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=8)
        ent_nombre = tk.Entry(frame_form, width=27)
        ent_nombre.grid(row=0, column=1, pady=8, padx=10)

        tk.Label(frame_form, text="Cantidad Inicial:", bg="#E8F8F5", font=(
            "Arial", 11)).grid(row=1, column=0, sticky="w", pady=8)
        ent_stock = tk.Entry(frame_form, width=27)
        ent_stock.grid(row=1, column=1, pady=8, padx=10)

        btn_guardar = tk.Button(
            self.tab_nuevo,
            text="Agregar",
            font=("Arial", 10, "bold"),
            bg="#8E44AD",
            fg="white",
            width=18,
            command=lambda: messagebox.showinfo(
                "Navegación", "Acción simulada: Producto agregado.")
        )
        btn_guardar.pack(pady=20)

    # Metodo Auxiliar
    # Con este metodo simulamos el cambio entre pantallas
    def limpiar_pantalla(self):
        for elemento in self.winfo_children():
            elemento.destroy()


if __name__ == "__main__":
    app = SistemaControlStock()
    app.mainloop()
