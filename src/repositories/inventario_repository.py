"""
Persistencia simple del inventario de billetes en data/inventario.json
"""

import json
import os

from src.utils.constantes import INVENTARIO_INICIAL

_RUTA_DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")
_RUTA_INVENTARIO = os.path.join(_RUTA_DATA, "inventario.json")


def _asegurar_archivo():
    os.makedirs(_RUTA_DATA, exist_ok=True)
    if not os.path.exists(_RUTA_INVENTARIO):
        guardar_inventario({str(k): v for k, v in INVENTARIO_INICIAL.items()})


def cargar_caja() -> dict:
    """Devuelve el inventario como {denominacion(int): cantidad(int)}."""
    _asegurar_archivo()
    with open(_RUTA_INVENTARIO, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {int(k): int(v) for k, v in data.items()}


def guardar_inventario(inventario: dict) -> None:
    os.makedirs(_RUTA_DATA, exist_ok=True)
    data = {str(k): int(v) for k, v in inventario.items()}
    with open(_RUTA_INVENTARIO, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
