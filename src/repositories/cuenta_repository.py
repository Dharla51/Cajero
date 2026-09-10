"""
repositorio temporal de cuentas, que guarda la información en un archivo JSON en disco.
"""

import json
import os

from src.utils.helpers import normalizar_interno

_RUTA_DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")
_RUTA_CUENTAS = os.path.join(_RUTA_DATA, "cuentas.json")


def _asegurar_archivo():
    os.makedirs(_RUTA_DATA, exist_ok=True)
    if not os.path.exists(_RUTA_CUENTAS):
        guardar_cuentas({})


def reiniciar_cuentas() -> None:
    """Deja el archivo de cuentas vacío (usado al arrancar la app de prueba)."""
    guardar_cuentas({})


def cargar_cuentas() -> dict:
    _asegurar_archivo()
    with open(_RUTA_CUENTAS, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_cuentas(cuentas: dict) -> None:
    os.makedirs(_RUTA_DATA, exist_ok=True)
    with open(_RUTA_CUENTAS, "w", encoding="utf-8") as f:
        json.dump(cuentas, f, indent=2, ensure_ascii=False)


def obtener_cuenta(vector_publico: str) -> dict | None:
    cuentas = cargar_cuentas()
    llave = normalizar_interno(vector_publico)
    return cuentas.get(llave)


def Cuenta_no_existente(vector_publico: str, tipo: str, pin: str | None = None) -> dict:
    """
    Crea la cuenta (solo identidad: tipo + clave) la primera vez que se usa
    un vector válido. NO tiene saldo propio — el dinero siempre sale del
    cajero.
    """
    cuentas = cargar_cuentas()
    llave = normalizar_interno(vector_publico)
    if llave not in cuentas:
        cuentas[llave] = {"tipo": tipo, "pin": pin}
        guardar_cuentas(cuentas)
    return cuentas[llave]
