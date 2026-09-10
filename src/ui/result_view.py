import tkinter as tk
from tkinter import ttk, messagebox

from src.utils.constantes import DENOMINACIONES_ASC
from src.utils.helpers import formatear_moneda

COLOR_FONDO = "#183c6c"
COLOR_ACENTO = "#f7f4ec"
COLOR_TEXTO = "#ffffff"
COLOR_BOTON = "#13345c"


class ResultView(tk.Frame):
    NOMBRE = "resultado"

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLOR_FONDO)
        self.app = app

        self.lbl_titulo = tk.Label(self, font=("Segoe UI", 18, "bold"), bg=COLOR_FONDO, fg=COLOR_ACENTO)
        self.lbl_titulo.pack(pady=(18, 4))

        self.lbl_resumen = tk.Label(self, font=("Segoe UI", 12), bg=COLOR_FONDO, fg=COLOR_TEXTO, justify="center")
        self.lbl_resumen.pack(pady=(0, 10))

        frame_billetes = tk.Frame(self, bg=COLOR_FONDO)
        frame_billetes.pack(pady=4)
        tk.Label(frame_billetes, text="Billetes entregados", font=("Segoe UI", 13, "bold"),
                 bg=COLOR_FONDO, fg=COLOR_ACENTO).pack()
        self.lbl_billetes = tk.Label(frame_billetes, font=("Consolas", 12), bg=COLOR_FONDO, fg=COLOR_TEXTO,
                                      justify="left")
        self.lbl_billetes.pack(pady=4)

        tk.Label(self, text="Matriz de intentos del acarreo",
                 font=("Segoe UI", 11, "bold"), bg=COLOR_FONDO, fg=COLOR_ACENTO).pack(pady=(14, 4))

        columnas = ["Intento"] + [formatear_moneda(d) for d in DENOMINACIONES_ASC] + ["Estado"]
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=6)
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=110, anchor="center")
        self.tabla.pack(pady=4, padx=20, fill="x")

        self.lbl_prediccion = tk.Label(self, font=("Segoe UI", 12, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO)
        self.lbl_prediccion.pack(pady=(14, 2))

        self.lbl_combinaciones = tk.Label(self, font=("Segoe UI", 10), bg=COLOR_FONDO, fg="#9db4d1")
        self.lbl_combinaciones.pack(pady=(0, 2))

        self.lbl_saldo = tk.Label(self, font=("Segoe UI", 10), bg=COLOR_FONDO, fg="#9db4d1")
        self.lbl_saldo.pack(pady=(0, 10))

        tk.Button(self, text="Realizar otro retiro", font=("Segoe UI", 12, "bold"),
                  bg=COLOR_ACENTO, fg="#0b1f3a", width=22, relief="flat", cursor="hand2",
                  command=lambda: self.app.mostrar("home")).pack(pady=14)

    def al_mostrar(self, resultado=None, tipo=""):
        if resultado is None:
            return

        self._avisar_si_hubo_recarga(resultado)

        self.lbl_titulo.configure(text=f"✅ {tipo} exitoso")
        self.lbl_resumen.configure(
            text=f"Monto retirado: {formatear_moneda(resultado['monto'])}   |   "
                 f"Total de billetes entregados: {resultado['total_billetes']}"
        )

        lineas = [
            f"{formatear_moneda(d):>12}  x  {resultado['billetes'][d]:>3}"
            for d in DENOMINACIONES_ASC if resultado["billetes"].get(d, 0) > 0
        ]
        self.lbl_billetes.configure(text="\n".join(lineas) if lineas else "No se requieren billetes.")

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for fila in resultado["matriz_intentos"]:
            etiqueta = f"Intento {fila['intento']} (Ciclo {fila['ciclo']})"
            valores = [str(fila["detalle"].get(d, 0)) for d in DENOMINACIONES_ASC]
            estado = "↺ Reinicio" if fila["reinicio"] else ""
            self.tabla.insert("", "end", values=[etiqueta] + valores + [estado])

        self.lbl_prediccion.configure(
            text=f"🔮 Con el efectivo que le queda al cajero podría entregar aproximadamente "
                 f"{resultado['prediccion_retiros']} retiro(s) más de este mismo monto."
        )
        self.lbl_combinaciones.configure(
            text=f"Combinaciones posibles de billetes para {formatear_moneda(resultado['monto'])}: "
                 f"{resultado['combinaciones_posibles']:,}".replace(",", ".")
        )
        self.lbl_saldo.configure(text=f"Efectivo disponible en el cajero: {formatear_moneda(resultado['saldo_restante'])}")

    def _avisar_si_hubo_recarga(self, resultado):
        detalle_recarga = resultado.get("recarga_detalle")
        if not detalle_recarga:
            return
        lineas_recarga = "\n".join(
            f"  + {formatear_moneda(d)}  x  {cant}"
            for d in DENOMINACIONES_ASC
            if detalle_recarga.get(d, 0) > 0
        )
        messagebox.showinfo(
            "Cajero recargándose",
            "⏳ El cajero se quedó sin billetes suficientes y se está "
            "cargando de dinero. Por favor espere un momento...\n\n"
            f"Billetes agregados (déficit vs. inventario inicial):\n{lineas_recarga}\n\n"
            "✅ Listo — el cajero volvió a la normalidad y su retiro fue procesado.",
            parent=self,
        )
