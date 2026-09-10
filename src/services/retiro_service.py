"""
servicio de retiro: valida los datos de la solicitud, ejecuta el algoritmo de acarreo y
descuenta los billetes del inventario. Si no hay suficientes billetes, recarga el cajero y vuelve a intentar.
"""

from src.algorithms.acarreo import ejecutar_acarreo
from src.repositories.cuenta_repository import Cuenta_no_existente
from src.services import caja_service
from src.validators.validadores import (
    validar_celular,
    validar_ahorro_mano,
    validar_cuenta_ahorros,
    validar_pin,
    validar_monto,
)


class RetiroError(Exception):
    """Error de negocio durante un retiro. El mensaje ya viene listo para el usuario."""


def retiro_nequi(celular: str, monto: int) -> dict:
    ok, msg = validar_celular(celular)
    if not ok:
        raise RetiroError(msg)

    ok, msg = validar_monto(monto)
    if not ok:
        raise RetiroError(msg)

    # no requiere cuenta pre-registrada, se crea sola.
    Cuenta_no_existente(celular, tipo="nequi")

    return finalizar(monto)


def retiro_ahorro_mano(vector: str, pin: str, monto: int) -> dict:
    ok, msg = validar_ahorro_mano(vector)
    if not ok:
        raise RetiroError(msg)
    return procesar_con_pin(vector, pin, monto, "ahorro_mano")


def retiro_cuenta_ahorros(vector: str, pin: str, monto: int) -> dict:
    ok, msg = validar_cuenta_ahorros(vector)
    if not ok:
        raise RetiroError(msg)
    return procesar_con_pin(vector, pin, monto, "cuenta_ahorros")


def procesar_con_pin(vector: str, pin: str, monto: int, tipo: str) -> dict:
    ok, msg = validar_pin(pin)
    if not ok:
        raise RetiroError(msg)

    # Cajero de PRUEBA: si el vector no existe, se crea con esta misma
    # clave; si ya existe, la clave debe coincidir con la registrada.
    cuenta = Cuenta_no_existente(vector, tipo=tipo, pin=pin)
    if cuenta.get("pin") != pin:
        raise RetiroError("Clave incorrecta.")

    ok, msg = validar_monto(monto)
    if not ok:
        raise RetiroError(msg)

    return finalizar(monto)


def finalizar(monto: int) -> dict:
    resultado = ejecutar_acarreo(monto)

    try:
        resultado["recarga_detalle"] = caja_service.descontar_o_recargar(resultado["billetes"])
    except ValueError as e:
        raise RetiroError(str(e))

    resultado["prediccion_retiros"] = caja_service.retiros_posibles(monto)
    resultado["saldo_restante"] = caja_service.maximo_retiro_posible()
    return resultado
