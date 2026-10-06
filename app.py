# Ventana principal

import customtkinter as ctk

import config
from pantallas.login import PantallaLogin
from pantallas.principal import PantallaPrincipal


class SistemaControlStock(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title(config.TITULO_APP)
        self.geometry(config.TAMANO_VENTANA)
        self.configure(fg_color=config.COLOR_FONDO)

        self.pantalla_login()

    # PANTALLA 1: LOGIN
    def pantalla_login(self):
        self.limpiar_pantalla()
        PantallaLogin(self, self).pack(fill="both", expand=True)

    # PANTALLA 2: PRINCIPAL (con las pestañas)
    def pantalla_principal(self):
        self.limpiar_pantalla()
        PantallaPrincipal(self, self).pack(fill="both", expand=True)

    # Metodo Auxiliar
    # Con este metodo simulamos el cambio entre pantallas
    def limpiar_pantalla(self):
        for elemento in self.winfo_children():
            elemento.destroy()
