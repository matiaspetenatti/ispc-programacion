# PANTALLA PRINCIPAL
import customtkinter as ctk

import config
from pantallas.tab_pedido import TabPedido
from pantallas.tab_ingreso import TabIngreso
from pantallas.tab_consulta import TabConsulta
from pantallas.tab_nuevo import TabNuevo


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
        tabview = ctk.CTkTabview(
            self,
            fg_color=config.COLOR_FONDO_TAB,
            segmented_button_selected_color=config.COLOR_HEADER,
            segmented_button_selected_hover_color=config.COLOR_HEADER
        )
        tabview.pack(fill="both", expand=True, padx=15, pady=15)

        # Pestañas
        self.tab_pedido = tabview.add("Ejecutar Pedido")
        self.tab_ingreso = tabview.add("Ingreso de Stock")
        self.tab_consulta = tabview.add("Ver Stock")
        self.tab_nuevo = tabview.add("Agregar Producto")

        # Contenido de cada pestaña (cada una está en su propio archivo)
        TabPedido(self.tab_pedido).pack(fill="both", expand=True)
        TabIngreso(self.tab_ingreso).pack(fill="both", expand=True)
        TabConsulta(self.tab_consulta).pack(fill="both", expand=True)
        TabNuevo(self.tab_nuevo).pack(fill="both", expand=True)
