"""
Ventana principal: actúa como contenedor de todas las vistas (Frames)
y expone métodos de navegación (`mostrar`) que cada vista usa para
pasar a la siguiente pantalla.
"""

import tkinter as tk

from src.controller.cajero import Cajero

COLOR_FONDO = "#000000"
COLOR_ACENTO = "#eae8e4"
COLOR_TEXTO = "#ffffff"
FUENTE_TITULO = ("New Times Roman", 20, "bold")
FUENTE_NORMAL = ("New Times Roman", 12)


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cajero Automático")
        self.geometry("760x640")
        self.configure(bg=COLOR_FONDO)
        self.resizable(False, False)

        self.cajero = Cajero()

        self.contenedor = tk.Frame(self, bg=COLOR_FONDO)
        self.contenedor.pack(fill="both", expand=True)

        self.vistas = {}
        self._registrar_vistas()
        self.mostrar("home")

    def _registrar_vistas(self):
        # Import diferido para evitar ciclos de import.
        from src.ui.home_view import HomeView
        from src.ui.retiro_view import RetiroView, CONFIGS_RETIRO
        from src.ui.result_view import ResultView

        for Clase in (HomeView, ResultView):
            vista = Clase(self.contenedor, self)
            self.vistas[vista.NOMBRE] = vista
            vista.place(x=0, y=0, relwidth=1, relheight=1)

        # Los 3 tipos de retiro son la MISMA clase, solo cambia la config.
        for config in CONFIGS_RETIRO:
            vista = RetiroView(self.contenedor, self, config)
            self.vistas[vista.NOMBRE] = vista
            vista.place(x=0, y=0, relwidth=1, relheight=1)

    def mostrar(self, nombre_vista: str, **kwargs):
        vista = self.vistas[nombre_vista]
        if hasattr(vista, "al_mostrar"):
            vista.al_mostrar(**kwargs)
        vista.tkraise()


def iniciar_app():
    app = MainWindow()
    app.mainloop()
