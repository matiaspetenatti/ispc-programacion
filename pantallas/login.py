# PANTALLA 1: LOGIN
import customtkinter as ctk

import config

import sqlite3
from tkinter import messagebox
import usuarios


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

        ctk.CTkLabel(frame_login, text="Usuario (legajo):",
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

        self.ent_usuario.bind("<Return>", lambda evento: self.validar_login())
        self.ent_clave.bind("<Return>", lambda evento: self.validar_login())

        self.ent_usuario.focus()

    def validar_login(self):
        legajo = self.ent_usuario.get().strip()
        clave = self.ent_clave.get()

        # Que no esten vacios
        if legajo == "" or clave == "":
            messagebox.showwarning("Datos incompletos",
                                   "Ingrese usuario y contraseña.")
            return

        # Comprobar contra la base de datos
        try:
            empleado = usuarios.validar_login(legajo, clave)
        except sqlite3.Error as error:
            messagebox.showerror("Error de base de datos",
                                 f"No se pudo consultar la base de datos:\n{error}")
            return

        # Si no coincide, no se entra
        if empleado is None:
            messagebox.showerror("Error de inicio de sesión",
                                 "Usuario o contraseña incorrectos.")
            self.ent_clave.delete(0, "end")
            self.ent_clave.focus()
            return

        # Login correcto: guardamos quién es y pasamos a la pantalla principal
        self.app.empleado_actual = empleado
        self.app.pantalla_principal()
