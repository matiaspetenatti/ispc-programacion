# Punto de entrada de la app

import customtkinter as ctk

from app import SistemaControlStock

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    app = SistemaControlStock()
    app.mainloop()
