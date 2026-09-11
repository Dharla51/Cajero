import tkinter as tk
from tkinter import font as tkfont

"Vista de inicio del cajero automático, donde el usuario selecciona el tipo de retiro que desea realizar."
class HomeView(tk.Frame):
    NOMBRE = "home"

    def __init__(self, parent, app):
        from src.ui.main_window import COLOR_FONDO, COLOR_ACENTO, COLOR_TEXTO, COLOR_PANEL

        super().__init__(parent, bg=COLOR_FONDO)
        self.app = app

        tk.Label(
            self, text="🏧 Cajero Automático", font=("Segoe UI", 28, "bold"),
            bg=COLOR_FONDO, fg="#050505",
        ).pack(pady=(50, 5))
        tk.Label(
            self, text="By Dharla Duran - Metodo Acarreo",
            font=("Segoe UI", 11), bg=COLOR_FONDO, fg="#050505",
        ).pack(pady=(0, 30))

        tk.Label(
            self, text="Seleccione el tipo de retiro", font=("Segoe UI", 15, "bold"),
            bg=COLOR_FONDO, fg="#050505",
        ).pack(pady=(0, 18))

        botones = [
            ("📱  Retiro estilo NEQUI (celular)", lambda: self.app.mostrar("nequi")),
            ("✋  Retiro ahorro a la mano", lambda: self.app.mostrar("ahorro_mano")),
            ("🏦  Retiro por cuenta de ahorros", lambda: self.app.mostrar("cuenta_ahorros")),
        ]
        for texto, comando in botones:
            tk.Button(
                self, text=texto, font=("Segoe UI", 13, "bold"), width=34, height=2,
                bg=COLOR_ACENTO, fg="#050505", activebackground=COLOR_PANEL,
                activeforeground="#050505", relief="flat", bd=0, cursor="hand2",
                command=comando,
            ).pack(pady=8)

        tk.Label(
            self, text="Cajero de prueba: ingrese cualquier vector con el formato correcto,\n"
                       "se crea una cuenta demo automáticamente la primera vez que lo use.",
            font=("Segoe UI", 9), bg=COLOR_FONDO, fg="#050505", justify="center",
        ).pack(side="bottom", pady=20)

    def al_mostrar(self, **kwargs):
        pass
