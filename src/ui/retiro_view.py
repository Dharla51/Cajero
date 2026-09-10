"""
UNA sola vista genérica para los 3 tipos de retiro (NEQUI, ahorro a la
mano, cuenta de ahorros). Antes eran 4 archivos casi idénticos (una
clase base + 3 vistas que solo cambiaban textos y un par de campos);
ahora es una sola clase parametrizada por un diccionario de
configuración (ver CONFIGS_RETIRO al final del archivo).
"""

import tkinter as tk
from tkinter import simpledialog

from src.utils.constantes import MONTOS_FIJOS, LONGITUD_PIN
from src.utils.helpers import formatear_moneda
from src.services.retiro_service import RetiroError

COLOR_FONDO = "#0b1f3a"
COLOR_ACENTO = "#f2b705"
COLOR_TEXTO = "#ffffff"
COLOR_BOTON = "#13345c"
COLOR_ERROR = "#ff6b6b"


class RetiroView(tk.Frame):
    """Pantalla de retiro genérica: se comporta distinto según `config`."""

    def __init__(self, parent, app, config: dict):
        super().__init__(parent, bg=COLOR_FONDO)
        self.app = app
        self.config = config
        self.NOMBRE = config["tipo"]  # usado por MainWindow para enrutar
        self.monto_seleccionado = tk.IntVar(value=0)
        self._id_reloj = None

        tk.Label(self, text=config["titulo"], font=("Segoe UI", 20, "bold"),
                 bg=COLOR_FONDO, fg=COLOR_ACENTO).pack(pady=(28, 5))
        tk.Label(self, text=config["instruccion_vector"], font=("Segoe UI", 11),
                 bg=COLOR_FONDO, fg=COLOR_TEXTO, justify="center").pack(pady=(0, 6))

        self.entry_vector = tk.Entry(self, font=("Segoe UI", 16), justify="center", width=20)
        self.entry_vector.pack(pady=4)
        self._solo_digitos(self.entry_vector, config["longitud_vector"])

        # Clave temporal (solo NEQUI) o PIN a digitar (ahorro a la mano / cuenta ahorros)
        self.entry_pin = None
        self.lbl_clave = None
        self.lbl_temporizador = None
        if config["requiere_pin"]:
            tk.Label(self, text="Clave (4 dígitos)", font=("Segoe UI", 11),
                      bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=(14, 2))
            self.entry_pin = tk.Entry(self, font=("Segoe UI", 16), justify="center", width=10, show="●")
            self.entry_pin.pack(pady=2)
            self._solo_digitos(self.entry_pin, LONGITUD_PIN)
        elif config["tiene_clave_temporal"]:
            self.lbl_clave = tk.Label(self, font=("Segoe UI", 13, "bold"), bg=COLOR_FONDO, fg=COLOR_ACENTO)
            self.lbl_clave.pack(pady=(14, 0))
            self.lbl_temporizador = tk.Label(self, font=("Segoe UI", 10), bg=COLOR_FONDO, fg="#9db4d1")
            self.lbl_temporizador.pack()

        tk.Label(self, text="Seleccione el monto a retirar", font=("Segoe UI", 12),
                 bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=(20, 6))
        self._construir_selector_montos(config["tipo"])

        self.lbl_error = tk.Label(self, font=("Segoe UI", 11), bg=COLOR_FONDO, fg=COLOR_ERROR,
                                   wraplength=600, justify="center")
        self.lbl_error.pack(pady=(16, 6))

        frame_botones = tk.Frame(self, bg=COLOR_FONDO)
        frame_botones.pack(pady=10)
        tk.Button(frame_botones, text="Confirmar retiro", font=("Segoe UI", 12, "bold"),
                  bg=COLOR_ACENTO, fg="#0b1f3a", width=18, relief="flat", cursor="hand2",
                  command=self._confirmar).pack(side="left", padx=6)
        tk.Button(frame_botones, text="Volver", font=("Segoe UI", 12),
                  bg=COLOR_BOTON, fg=COLOR_TEXTO, width=12, relief="flat", cursor="hand2",
                  command=lambda: self.app.mostrar("home")).pack(side="left", padx=6)

    # --- helpers de construcción ------------------------------------------

    def _solo_digitos(self, entry: tk.Entry, longitud_maxima: int):
        def validar(valor_propuesto, maximo=longitud_maxima):
            if valor_propuesto == "":
                return True
            return valor_propuesto.isdigit() and len(valor_propuesto) <= int(maximo)

        entry.configure(validate="key", validatecommand=(self.register(validar), "%P"))

    def _construir_selector_montos(self, tipo: str):
        montos = MONTOS_FIJOS[tipo]
        self.botones_monto = {}
        fila = tk.Frame(self, bg=COLOR_FONDO)
        fila.pack()

        def seleccionar(valor, boton):
            self.monto_seleccionado.set(valor)
            for b in self.botones_monto.values():
                b.configure(bg=COLOR_BOTON)
            boton.configure(bg=COLOR_ACENTO)

        for monto in montos:
            btn = tk.Button(fila, text=formatear_moneda(monto), font=("Segoe UI", 11), width=12,
                             bg=COLOR_BOTON, fg=COLOR_TEXTO, relief="flat", cursor="hand2")
            btn.configure(command=lambda m=monto, b=btn: seleccionar(m, b))
            btn.pack(side="left", padx=4, pady=4)
            self.botones_monto[monto] = btn

        btn_otro = tk.Button(fila, text="Otro monto...", font=("Segoe UI", 11), width=12,
                              bg=COLOR_BOTON, fg=COLOR_TEXTO, relief="flat", cursor="hand2")

        def elegir_otro():
            valor = simpledialog.askinteger(
                "Otro monto", "Ingrese el monto a retirar (múltiplo de $10.000):", parent=self
            )
            if valor is not None:
                seleccionar(valor, btn_otro)
                btn_otro.configure(text=formatear_moneda(valor))

        btn_otro.configure(command=elegir_otro)
        btn_otro.pack(side="left", padx=4, pady=4)
        self.botones_monto["otro"] = btn_otro

    # --- ciclo de vida de la vista ------------------------------------------

    def al_mostrar(self, **kwargs):
        self.entry_vector.delete(0, tk.END)
        if self.entry_pin:
            self.entry_pin.delete(0, tk.END)
        self.monto_seleccionado.set(0)
        self.lbl_error.configure(text="")
        for b in self.botones_monto.values():
            b.configure(bg=COLOR_BOTON)
        self.botones_monto["otro"].configure(text="Otro monto...")
        if self.config["tiene_clave_temporal"]:
            self._refrescar_clave()

    def _refrescar_clave(self):
        clave = self.app.cajero.clave_nequi_vigente()
        restante = self.app.cajero.segundos_restantes_clave_nequi()
        self.lbl_clave.configure(text=f"Clave temporal: {clave}")
        self.lbl_temporizador.configure(text=f"Válida por {restante} segundos (se renueva automáticamente)")
        if self._id_reloj:
            self.after_cancel(self._id_reloj)
        self._id_reloj = self.after(1000, self._refrescar_clave)

    def _confirmar(self):
        vector = self.entry_vector.get().strip()
        monto = self.monto_seleccionado.get()
        pin = self.entry_pin.get().strip() if self.entry_pin else None

        if monto <= 0:
            self.lbl_error.configure(text="Debe seleccionar un monto a retirar.")
            return
        try:
            resultado = self.config["funcion_retiro"](self.app.cajero, vector, pin, monto)
        except RetiroError as e:
            self.lbl_error.configure(text=str(e))
            return

        self.app.mostrar("resultado", resultado=resultado, tipo=self.config["titulo_resultado"])


# --- Configuración de cada uno de los 3 tipos de retiro ---------------------
# Cada entrada define todo lo que cambia entre un tipo de retiro y otro;
# el comportamiento (validaciones, layout, flujo) vive una sola vez en
# la clase RetiroView de arriba.

CONFIGS_RETIRO = [
    {
        "tipo": "nequi",
        "titulo": "📱 Retiro estilo NEQUI",
        "titulo_resultado": "Retiro estilo NEQUI",
        "instruccion_vector": "Ingrese su número de celular (10 dígitos, debe iniciar en 3)",
        "longitud_vector": 10,
        "requiere_pin": False,
        "tiene_clave_temporal": True,
        "funcion_retiro": lambda cajero, vector, pin, monto: cajero.retirar_nequi(vector, monto),
    },
    {
        "tipo": "ahorro_mano",
        "titulo": "✋ Retiro ahorro a la mano",
        "titulo_resultado": "Retiro ahorro a la mano",
        "instruccion_vector": "Vector de 11 dígitos (empieza en 0 o 1, segundo dígito debe ser 3)",
        "longitud_vector": 11,
        "requiere_pin": True,
        "tiene_clave_temporal": False,
        "funcion_retiro": lambda cajero, vector, pin, monto: cajero.retirar_ahorro_mano(vector, pin, monto),
    },
    {
        "tipo": "cuenta_ahorros",
        "titulo": "🏦 Retiro por cuenta de ahorros",
        "titulo_resultado": "Retiro por cuenta de ahorros",
        "instruccion_vector": "Número de cuenta (11 dígitos)",
        "longitud_vector": 11,
        "requiere_pin": True,
        "tiene_clave_temporal": False,
        "funcion_retiro": lambda cajero, vector, pin, monto: cajero.retirar_cuenta_ahorros(vector, pin, monto),
    },
]
