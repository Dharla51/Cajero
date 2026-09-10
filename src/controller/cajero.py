"""
 fachada del cajero automático, que expone los métodos de retiro y mantiene la bitácora de trans
"""

from datetime import datetime

from src.services.retiro_service import (
    RetiroError,
    retiro_nequi,
    retiro_ahorro_mano,
    retiro_cuenta_ahorros,
)
from src.utils.helpers import ClaveTemporal


class Cajero:
    def __init__(self):
        self.bitacora: list[dict] = []
        self.clave_temporal_nequi = ClaveTemporal()

    # --- Clave temporal (retiro NEQUI) -----------------------------------
    def clave_nequi_vigente(self) -> str:
        return self.clave_temporal_nequi.asegurar_vigente()

    def segundos_restantes_clave_nequi(self) -> int:
        return self.clave_temporal_nequi.segundos_restantes()

    # --- Retiros -----------------------------------------------------------
    def retirar_nequi(self, celular: str, monto: int) -> dict:
        return self._ejecutar("nequi", celular, monto, retiro_nequi, celular, monto)

    def retirar_ahorro_mano(self, vector: str, pin: str, monto: int) -> dict:
        return self._ejecutar("ahorro_mano", vector, monto, retiro_ahorro_mano, vector, pin, monto)

    def retirar_cuenta_ahorros(self, vector: str, pin: str, monto: int) -> dict:
        return self._ejecutar("cuenta_ahorros", vector, monto, retiro_cuenta_ahorros, vector, pin, monto)

    def _ejecutar(self, tipo, vector, monto, funcion_servicio, *args) -> dict:
        registro = {"tipo": tipo, "vector": vector, "monto": monto, "hora": datetime.now().strftime("%H:%M:%S")}
        try:
            resultado = funcion_servicio(*args)
            registro["exitosa"] = True
            self.bitacora.append(registro)
            return resultado
        except RetiroError as e:
            registro["exitosa"] = False
            registro["mensaje"] = str(e)
            self.bitacora.append(registro)
            raise
