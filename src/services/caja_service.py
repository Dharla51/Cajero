"""
Servicios para gestionar el inventario físico de billetes del cajero.
"""

from src.repositories.inventario_repository import cargar_caja, guardar_inventario
from src.utils.constantes import INVENTARIO_INICIAL


def obtener_caja() -> dict:
    return cargar_caja()


def valor_total_caja(inventario: dict) -> int:
    return sum(denom * cant for denom, cant in inventario.items())


def hay_disponibilidad(billetes_requeridos: dict, inventario: dict | None = None) -> bool:
    inventario = inventario if inventario is not None else cargar_caja()
    return all(inventario.get(denom, 0) >= cantidad for denom, cantidad in billetes_requeridos.items())


def calcular_deficit(inventario_actual: dict, objetivo: dict | None = None) -> dict:
    """
    Para cada denominación, cuántos billetes FALTAN para volver al
    inventario objetivo (por defecto, el inicial): objetivo - lo_que_hay.
    Nunca negativo (si ya hay igual o más que el objetivo, el déficit es 0).
    """
    objetivo = objetivo or INVENTARIO_INICIAL
    return {
        denom: max(0, objetivo.get(denom, 0) - inventario_actual.get(denom, 0))
        for denom in objetivo
    }


def recargar_caja() -> dict:
    """
    Recarga el cajero: calcula el déficit de cada denominación frente al
    inventario inicial y SUMA exactamente esa cantidad al inventario
    actual (no lo reemplaza).

    Devuelve el detalle de billetes agregados por denominación, por
    ejemplo {100000: 12, 50000: 5, 20000: 0, 10000: 0}
    """
    inventario_actual = cargar_caja()
    deficit = calcular_deficit(inventario_actual)

    nuevo_inventario = {
        denom: inventario_actual.get(denom, 0) + deficit.get(denom, 0)
        for denom in INVENTARIO_INICIAL
    }
    guardar_inventario(nuevo_inventario)
    return deficit


def descontar_o_recargar(billetes_requeridos: dict) -> dict | None:
    """
    Intenta descontar `billetes_requeridos` del inventario actual.
    Si NO hay suficientes billetes de alguna denominación, recarga el
    cajero y vuelve a intentar.

    Devuelve el detalle de billetes agregados en la recarga si
    hubo que recargar, o None si el inventario ya alcanzaba.

    Lanza ValueError si ni siquiera un inventario recién recargado
    alcanza para el retiro solicitado (monto mayor a la capacidad total
    del cajero).
    """
    caja = cargar_caja()
    detalle_recarga = None

    if not hay_disponibilidad(billetes_requeridos, caja):
        detalle_recarga = recargar_caja()
        caja = cargar_caja()

        if not hay_disponibilidad(billetes_requeridos, caja):
            raise ValueError(
                "El monto solicitado supera la capacidad total del cajero, "
                "incluso después de recargarlo. Intente con un monto menor."
            )

    for denom, cantidad in billetes_requeridos.items():
        caja[denom] = caja.get(denom, 0) - cantidad
    guardar_inventario(caja)

    return detalle_recarga


def maximo_retiro_posible() -> int:
    inventario = cargar_caja()
    return valor_total_caja(inventario)


def retiros_posibles(monto_retiro: int) -> int:
    """
    Predicción: con el efectivo que le queda AL CAJERO (no a la cuenta,
    porque las cuentas no tienen saldo propio), ¿cuántos retiros de este
    mismo monto podría seguir entregando?
    """
    if monto_retiro <= 0:
        return 0
    return maximo_retiro_posible() // monto_retiro
