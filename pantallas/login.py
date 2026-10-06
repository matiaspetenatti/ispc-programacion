# PANTALLA 1: LOGIN
import customtkinter as ctk

import config


class PantallaLogin(ctk.CTkFrame):

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app  # la ventana principal, para poder cambiar de pantalla

        frame_login = ctk.CTkFrame(self, fg_color="white", corner_radius=16)
        frame_login.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            frame_login,
            text="Control de Stock",
            font=config.FUENTE_TITULO,
            text_color=config.COLOR_HEADER
        ).pack(padx=50, pady=(30, 20))

        ctk.CTkLabel(frame_login, text="Usuario:",
                     font=config.FUENTE_NORMAL).pack(anchor="w", padx=40)
        self.ent_usuario = ctk.CTkEntry(frame_login, width=250)
        self.ent_usuario.pack(padx=40, pady=5)

        ctk.CTkLabel(frame_login, text="Contraseña:",
                     font=config.FUENTE_NORMAL).pack(anchor="w", padx=40)
        self.ent_clave = ctk.CTkEntry(frame_login, width=250, show="*")
        self.ent_clave.pack(padx=40, pady=5)

        btn_ingresar = ctk.CTkButton(
            frame_login,
            text="Ingresar",
            font=config.FUENTE_BOTON,
            fg_color=config.COLOR_VERDE,
            hover_color=config.COLOR_VERDE_HOVER,
            width=180,
            command=self.validar_login
        )
        btn_ingresar.pack(pady=(20, 30))

    def validar_login(self):
        # Simulamos un login valido y pasamos a la pantalla principal
        self.app.pantalla_principal()
