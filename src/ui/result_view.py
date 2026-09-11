import tkinter as tk
from tkinter import ttk, messagebox

from src.services import caja_service
from src.utils.constantes import DENOMINACIONES_ASC
from src.utils.helpers import formatear_moneda

COLOR_FONDO = "#6D9B61"
COLOR_ACENTO = "#FFF8CF"
COLOR_TEXTO = "#050505"
COLOR_BOTON = "#76C457"


class ResultView(tk.Frame):
    NOMBRE = "resultado"

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLOR_FONDO)
        self.app = app

        self.canvas = tk.Canvas(self, bg=COLOR_FONDO, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scroll_content = tk.Frame(self.canvas, bg=COLOR_FONDO)
        self.canvas.create_window((0, 0), window=self.scroll_content, anchor="nw", width=self.winfo_width())
        self.scroll_content.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.lbl_titulo = tk.Label(self.scroll_content, font=("New times roman", 18, "bold"), bg=COLOR_FONDO, fg="#050505")
        self.lbl_titulo.pack(pady=(18, 4))

        self.lbl_resumen = tk.Label(self.scroll_content, font=("New times roman", 12), bg=COLOR_FONDO, fg="#050505", justify="center")
        self.lbl_resumen.pack(pady=(0, 10))

        frame_billetes = tk.Frame(self.scroll_content, bg=COLOR_FONDO)
        frame_billetes.pack(pady=4)
        tk.Label(frame_billetes, text="Billetes entregados", font=("New times roman", 13, "bold"),
                 bg=COLOR_FONDO, fg="#050505").pack()
        self.lbl_billetes = tk.Label(frame_billetes, font=("Consolas", 12), bg=COLOR_FONDO, fg="#050505",
                                      justify="left")
        self.lbl_billetes.pack(pady=4)

        tk.Label(self.scroll_content, text="Matriz de intentos del acarreo",
                 font=("New times roman", 11, "bold"), bg=COLOR_FONDO, fg="#050505").pack(pady=(14, 4))

        columnas = ["Intento"] + [formatear_moneda(d) for d in [100000, 50000, 20000, 10000]] + ["Estado"]
        self.tabla = ttk.Treeview(self.scroll_content, columns=columnas, show="headings", height=6)
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=110, anchor="center")
        self.tabla.pack(pady=4, padx=20, fill="x")

        self.prediccion_frame = tk.Frame(self.scroll_content, bg=COLOR_FONDO)
        self.prediccion_frame.pack(fill="x", side="bottom", pady=(18, 0))

        self.lbl_titulo_prediccion = tk.Label(
            self.prediccion_frame, text="Verificar disponibilidad para varios retiros",
            font=("New times roman", 22, "bold"), bg="#6D9B61", fg="#050505",
            justify="left", anchor="w"
        )
        self.lbl_titulo_prediccion.pack(anchor="w", padx=20, pady=(18, 8))

        self.lbl_pregunta_prediccion = tk.Label(
            self.prediccion_frame,
            text="¿Cuántos retiros de $0 desea verificar?",
            font=("New times roman", 18, "bold"), bg="#6D9B61", fg="#050505",
            justify="left", anchor="w", wraplength=700
        )
        self.lbl_pregunta_prediccion.pack(anchor="w", padx=20)

        self.entry_prediccion = tk.Entry(
            self.prediccion_frame, font=("New times roman", 24, "bold"),
            justify="center", width=18, bg="#D9D9D9", fg="#050505",
            insertbackground="#050505"
        )
        self.entry_prediccion.bind("<KeyRelease>", lambda event: self._mostrar_matriz_billetes())
        self.entry_prediccion.pack(fill="x", padx=20, pady=(10, 8))

        self.btn_verificar_disponibilidad = tk.Button(
            self.prediccion_frame, text="Verificar disponibilidad",
            font=("New times roman", 18, "bold"), bg="#8a6fe8", fg="#050505",
            relief="flat", bd=0, cursor="hand2", command=self._verificar_disponibilidad
        )
        self.btn_verificar_disponibilidad.pack(fill="x", padx=20, pady=(0, 12))

        self.lbl_resultado_prediccion = tk.Label(
            self.prediccion_frame, font=("New times roman", 14, "bold"),
            bg="#6D9B61", fg="#050505", justify="left", wraplength=700
        )
        self.lbl_resultado_prediccion.pack(anchor="w", padx=20, pady=(0, 12))

        self.lbl_billetes_necesarios_titulo = tk.Label(
            self.prediccion_frame, font=("New times roman", 12, "bold"),
            bg="#6D9B61", fg="#050505", justify="left", anchor="w", wraplength=760
        )
        self.lbl_billetes_necesarios_titulo.pack(anchor="w", padx=20, pady=(10, 4))

        self.lbl_matriz_billetes = tk.Label(
            self.prediccion_frame, font=("Consolas", 11, "bold"),
            bg="#6D9B61", fg="#050505", justify="left", anchor="w", wraplength=760
        )
        self.lbl_matriz_billetes.pack(anchor="w", padx=20)

        self.lbl_billetes_faltantes = tk.Label(
            self.prediccion_frame, font=("New times roman", 11, "bold"),
            bg="#6D9B61", fg="#050505", justify="left", anchor="w", wraplength=760
        )
        self.lbl_billetes_faltantes.pack(anchor="w", padx=20, pady=(6, 0))

        self.lbl_capacidad_total = tk.Label(
            self.prediccion_frame, font=("New times roman", 11, "bold"),
            bg="#6D9B61", fg="#050505", justify="left", anchor="w", wraplength=760
        )
        self.lbl_capacidad_total.pack(anchor="w", padx=20, pady=(4, 12))

        self.lbl_inventario_titulo = tk.Label(
            self.prediccion_frame, text="Inventario de la caja",
            font=("New times roman", 13, "bold"),
            bg="#6D9B61", fg="#050505", justify="left", anchor="w", wraplength=760
        )
        self.lbl_inventario_titulo.pack(anchor="w", padx=20, pady=(8, 4))

        self.lbl_inventario = tk.Label(
            self.prediccion_frame, font=("Consolas", 11, "bold"),
            bg="#6D9B61", fg="#050505", justify="left", anchor="w", wraplength=760
        )
        self.lbl_inventario.pack(anchor="w", padx=20, pady=(0, 10))

        tk.Button(self.scroll_content, text="Realizar otro retiro", font=("New times roman", 12, "bold"),
                  bg=COLOR_ACENTO, fg="#050505", width=22, relief="flat", bd=0,
                  activebackground="#FBE6C2", activeforeground="#050505",
                  cursor="hand2", command=lambda: self.app.mostrar("home")).pack(pady=14)

        self.canvas.bind("<Configure>", lambda event: self.canvas.itemconfig(1, width=event.width))
        self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

    def al_mostrar(self, resultado=None, tipo=""):
        if resultado is None:
            return

        self.resultado_actual = resultado
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
            valores = [str(fila["detalle"].get(d, 0)) for d in [100000, 50000, 20000, 10000]]
            estado = "↺ Reinicio" if fila["reinicio"] else ""
            self.tabla.insert("", "end", values=[etiqueta] + valores + [estado])

        self.entry_prediccion.delete(0, tk.END)
        self.lbl_pregunta_prediccion.configure(
            text=f"¿Cuántos retiros de {formatear_moneda(resultado['monto'])} desea verificar?"
        )
        self.lbl_resultado_prediccion.configure(text="")
        self._mostrar_matriz_billetes()
        self._verificar_disponibilidad()

    def _mostrar_matriz_billetes(self):
        if not hasattr(self, "resultado_actual") or self.resultado_actual is None:
            return

        try:
            cantidad = int(self.entry_prediccion.get().strip())
        except ValueError:
            self.lbl_billetes_necesarios_titulo.configure(text="")
            self.lbl_matriz_billetes.configure(text="")
            self.lbl_billetes_faltantes.configure(text="")
            self.lbl_capacidad_total.configure(text="")
            return

        if cantidad <= 0:
            self.lbl_billetes_necesarios_titulo.configure(text="")
            self.lbl_matriz_billetes.configure(text="")
            self.lbl_billetes_faltantes.configure(text="")
            self.lbl_capacidad_total.configure(text="")
            return

        billetes_retiro = self.resultado_actual.get("billetes", {})
        inventario = caja_service.obtener_caja()
        total_necesario = 0
        total_disponible = 0
        faltantes = []
        lineas = []

        for denom in [100000, 50000, 20000, 10000]:
            necesarios = int(billetes_retiro.get(denom, 0)) * cantidad
            disponible = int(inventario.get(denom, 0))
            faltante = max(0, necesarios - disponible)
            total_necesario += necesarios * denom
            total_disponible += disponible * denom
            faltantes.append((denom, faltante))

            nombre = {
                10000: "10 mil",
                20000: "20 mil",
                50000: "50 mil",
                100000: "100 mil",
            }.get(denom, str(denom))
            lineas.append(f"{nombre:<8}  {necesarios:>3}  (cajero: {disponible:>3})")

        self.lbl_billetes_necesarios_titulo.configure(
            text=f"Billetes necesarios (total {formatear_moneda(total_necesario)}):"
        )
        self.lbl_matriz_billetes.configure(
            text="\n".join(lineas)
        )

        faltantes_activos = [(den, falt) for den, falt in faltantes if falt > 0]
        if faltantes_activos:
            self.lbl_billetes_faltantes.configure(
                text="! Billetes faltantes:\n" + "\n".join(
                    f"{nombre:<8}  {cant}"
                    for denom, cant in faltantes_activos
                    for nombre in [
                        {
                            10000: "10 mil",
                            20000: "20 mil",
                            50000: "50 mil",
                            100000: "100 mil",
                        }.get(denom, str(denom))
                    ]
                )
            )
        else:
            self.lbl_billetes_faltantes.configure(text="")

        inventario = caja_service.obtener_caja()
        lineas_inventario = []
        for denom in [100000, 50000, 20000, 10000]:
            cantidad_actual = inventario.get(denom, 0)
            nombre = {
                10000: "10 mil",
                20000: "20 mil",
                50000: "50 mil",
                100000: "100 mil",
            }.get(denom, str(denom))
            lineas_inventario.append(f"{nombre:<8}  {cantidad_actual:>3} billetes")

        self.lbl_inventario.configure(text="\n".join(lineas_inventario))

        if total_necesario > total_disponible:
            self.lbl_capacidad_total.configure(
                text=f"! Este monto total supera la capacidad máxima del cajero ({formatear_moneda(total_disponible)}), "
                     "por lo que no es posible ni recargándolo."
            )
        else:
            self.lbl_capacidad_total.configure(text="")

    def _verificar_disponibilidad(self):
        if not hasattr(self, "resultado_actual") or self.resultado_actual is None:
            return

        monto = int(self.resultado_actual["monto"])
        try:
            cantidad = int(self.entry_prediccion.get().strip())
        except ValueError:
            self.lbl_resultado_prediccion.configure(text="Ingrese un número válido de retiros.")
            return

        if cantidad <= 0:
            self.lbl_resultado_prediccion.configure(text="La cantidad debe ser mayor que cero.")
            return

        disponible = int(self.resultado_actual.get("saldo_restante", 0))
        total_requerido = cantidad * monto

        if total_requerido <= disponible:
            self.lbl_resultado_prediccion.configure(
                text=f"Sí es posible realizar {cantidad} retiros de {formatear_moneda(monto)}. "
                     f"El cajero tiene suficiente efectivo para cubrirlos."
            )
        else:
            faltante = total_requerido - disponible
            self.lbl_resultado_prediccion.configure(
                text=f"! No es posible realizar {cantidad} retiros de {formatear_moneda(monto)}: "
                     f"el cajero no cuenta con billetes suficientes.\n"
                     f"Falta: {formatear_moneda(faltante)}"
            )

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
