import tkinter as tk

from src.services import caja_service
from src.utils.constantes import DENOMINACIONES, INVENTARIO_INICIAL
from src.utils.helpers import formatear_moneda


class InventarioView(tk.Frame):
    NOMBRE = "inventario_caja"

    def __init__(self, parent, app):
        from src.ui.main_window import COLOR_FONDO, COLOR_ACENTO, COLOR_PANEL

        super().__init__(parent, bg=COLOR_FONDO)
        self.app = app

        self.frame_contenido = tk.Frame(self, bg=COLOR_FONDO)
        self.frame_contenido.pack(fill="both", expand=True, padx=20, pady=18)

        self.lbl_titulo = tk.Label(
            self.frame_contenido,
            text="INVENTARIO DE CAJA",
            font=("Segoe UI", 18, "bold"),
            bg=COLOR_FONDO,
            fg="#050505",
            anchor="w",
        )
        self.lbl_titulo.pack(fill="x", pady=(0, 10))

        self.barra_container = tk.Frame(self.frame_contenido, bg="#1E6E12", bd=0, highlightthickness=0)
        self.barra_container.pack(fill="x")

        self.barra = tk.Frame(self.barra_container, bg="#76C457", height=24)
        self.barra.pack(side="left", fill="y", ipadx=0)

        self.lbl_porcentaje = tk.Label(
            self.barra_container,
            text="0%",
            font=("Segoe UI", 12, "bold"),
            bg="#1E6E12",
            fg="#050505",
        )
        self.lbl_porcentaje.pack(side="right", padx=(10, 0))

        self.lbl_rango = tk.Label(
            self.frame_contenido,
            text="$0.000 / $0.000",
            font=("Segoe UI", 12, "bold"),
            bg=COLOR_FONDO,
            fg="#050505",
        )
        self.lbl_rango.pack(fill="x", pady=(8, 4))

        self.lbl_resumen = tk.Label(
            self.frame_contenido,
            text="0 billetes",
            font=("Segoe UI", 11),
            bg=COLOR_FONDO,
            fg="#050505",
        )
        self.lbl_resumen.pack(fill="x", pady=(0, 8))

        self.lbl_cabecera = tk.Label(
            self.frame_contenido,
            text="Retiro: 1      Disponís: $0.000      ",
            font=("Segoe UI", 12),
            bg=COLOR_FONDO,
            fg="#050505",
        )
        self.lbl_cabecera.pack(fill="x", pady=(0, 6))

        self.lista_billetes = tk.Frame(self.frame_contenido, bg=COLOR_FONDO)
        self.lista_billetes.pack(fill="x")

        self.btn_reabastecer = tk.Button(
            self.frame_contenido,
            text="Reabastecer caja",
            font=("Segoe UI", 12, "bold"),
            bg="#B5B5B5",
            fg="#050505",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self._reabastecer_caja,
        )
        self.btn_reabastecer.pack(fill="x", pady=(18, 0), ipady=8)

        self.btn_volver = tk.Button(
            self.frame_contenido,
            text="Volver",
            font=("Segoe UI", 12, "bold"),
            bg=COLOR_ACENTO,
            fg="#050505",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda: self.app.mostrar("home"),
        )
        self.btn_volver.pack(fill="x", pady=(12, 0), ipady=8)

    def al_mostrar(self, **kwargs):
        self._renderizar_inventario()

    def _reabastecer_caja(self):
        caja_service.recargar_caja()
        self._renderizar_inventario()

    def _renderizar_inventario(self):
        caja_service.recargar_si_hace_falta(0.2)
        inventario = caja_service.obtener_caja()
        inventario_inicial = INVENTARIO_INICIAL

        total_actual = sum(denom * cant for denom, cant in inventario.items())
        total_inicial = sum(denom * cant for denom, cant in inventario_inicial.items())
        porcentaje = 100 if total_inicial == 0 else round((total_actual / total_inicial) * 100, 2)

        self.lbl_porcentaje.configure(text=f"{porcentaje:.2f}%")
        self.barra.configure(width=max(6, int(660 * (porcentaje / 100))))

        self.lbl_rango.configure(
            text=f"{formatear_moneda(total_actual)} / {formatear_moneda(total_inicial)}"
        )
        self.lbl_resumen.configure(text=f"{sum(inventario.values())} billetes")

        self.lbl_cabecera.configure(
            text=f"Retiros: {caja_service.retiros_posibles(10000)}  |  Disponís: {formatear_moneda(caja_service.maximo_retiro_posible())}"
        )

        for widget in self.lista_billetes.winfo_children():
            widget.destroy()

        for denom in DENOMINACIONES:
            actual = inventario.get(denom, 0)
            inicial = inventario_inicial.get(denom, 0)
            porcentaje_denom = 100 if inicial == 0 else round((actual / inicial) * 100, 2)
            fila = tk.Frame(self.lista_billetes, bg=COLOR_FONDO)
            fila.pack(fill="x", pady=4)

            tk.Label(fila, text=formatear_moneda(denom), font=("Segoe UI", 11), bg=COLOR_FONDO, fg="#050505", width=12, anchor="w").pack(side="left")
            tk.Label(fila, text=f"{actual:>4}", font=("Segoe UI", 11, "bold"), bg=COLOR_FONDO, fg="#050505", width=6, anchor="e").pack(side="left")
            tk.Label(fila, text=f"{inicial:>4}", font=("Segoe UI", 11), bg=COLOR_FONDO, fg="#050505", width=6, anchor="e").pack(side="left", padx=(10, 6))
            tk.Label(fila, text=f"{porcentaje_denom:.1f}%", font=("Segoe UI", 10, "bold"), bg=COLOR_FONDO, fg="#050505", width=8, anchor="e").pack(side="left")
            tk.Label(fila, text="billetes", font=("Segoe UI", 10), bg=COLOR_FONDO, fg="#050505").pack(side="left")

        if total_actual < total_inicial * 0.5:
            self.btn_reabastecer.configure(bg="#76C457")
        else:
            self.btn_reabastecer.configure(bg="#B5B5B5")
