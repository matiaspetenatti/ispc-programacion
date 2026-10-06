# Punto de entrada de la app

import customtkinter as ctk

import base_datos
import usuarios
from app import SistemaControlStock

if __name__ == "__main__":

    base_datos.crear_tablas()
    usuarios.crear_usuario_demo()

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    app = SistemaControlStock()
    app.mainloop()
