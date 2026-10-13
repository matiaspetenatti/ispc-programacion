# PANTALLA PRINCIPAL
import customtkinter as ctk

import config
from pantallas.tab_pedido import TabPedido
from pantallas.tab_ingreso import TabIngreso
from pantallas.tab_consulta import TabConsulta
from pantallas.tab_nuevo import TabNuevo
from pantallas.tab_historial import TabHistorial


class PantallaPrincipal(ctk.CTkFrame):

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app

        # Encabezado
        header = ctk.CTkFrame(self, fg_color=config.COLOR_HEADER,
                              corner_radius=0, height=50)
        header.pack(fill="x")

        ctk.CTkLabel(
            header,
            text="Control de Stock - Panel General",
            font=config.FUENTE_HEADER,
            text_color="white"
        ).pack(side="left", padx=15, pady=10)

        btn_salir = ctk.CTkButton(
            header,
            text="Cerrar Sesión",
            width=120,
            fg_color=config.COLOR_ROJO,
            hover_color=config.COLOR_ROJO_HOVER,
            command=self.app.pantalla_login
        )
        btn_salir.pack(side="right", padx=15, pady=10)

        nombre_empleado = self.app.empleado_actual[1]
        ctk.CTkLabel(
            header,
            text=f"Usuario: {nombre_empleado}",
            font=config.FUENTE_NORMAL,
            text_color="white"
        ).pack(side="right", padx=10)

        # Contenedor de Pestañas
        # command: se ejecuta cada vez que el usuario cambia de pestaña
        self.tabview = ctk.CTkTabview(
            self,
            fg_color=config.COLOR_FONDO_TAB,
            segmented_button_selected_color=config.COLOR_HEADER,
            segmented_button_selected_hover_color=config.COLOR_HEADER,
            command=self.al_cambiar_pestana
        )
        self.tabview.pack(fill="both", expand=True, padx=15, pady=15)

        # Pestañas
        self.tab_pedido = self.tabview.add("Ejecutar Pedido")
        self.tab_ingreso = self.tabview.add("Ingreso de Stock")
        self.tab_consulta = self.tabview.add("Ver Stock")
        self.tab_nuevo = self.tabview.add("Agregar Producto")
        self.tab_historial = self.tabview.add("Historial")

        # Contenido de cada pestaña (cada una está en su propio archivo)
        self.contenido_pedido = TabPedido(self.tab_pedido, self.app)
        self.contenido_pedido.pack(fill="both", expand=True)

        self.contenido_ingreso = TabIngreso(self.tab_ingreso, self.app)
        self.contenido_ingreso.pack(fill="both", expand=True)

        self.contenido_consulta = TabConsulta(self.tab_consulta)
        self.contenido_consulta.pack(fill="both", expand=True)

        TabNuevo(self.tab_nuevo).pack(fill="both", expand=True)

        self.contenido_historial = TabHistorial(self.tab_historial)
        self.contenido_historial.pack(fill="both", expand=True)

    def al_cambiar_pestana(self):
        """Recarga los datos de la pestaña que se acaba de abrir.

        Así, si se ingresa stock o se ejecuta un pedido, las demás pestañas
        muestran los valores actualizados sin tener que reiniciar la app.
        """
        actual = self.tabview.get()
        if actual == "Ejecutar Pedido":
            self.contenido_pedido.cargar_combos()
        elif actual == "Ingreso de Stock":
            self.contenido_ingreso.cargar_combos()
        elif actual == "Ver Stock":
            self.contenido_consulta.cargar_stock()
        elif actual == "Historial":
            self.contenido_historial.cargar_historial()
