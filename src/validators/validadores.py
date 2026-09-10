"""
Todas las validaciones de entrada del cajero, en un solo lugar:
formato de vectores (celular, ahorro a la mano, cuenta de ahorros),
clave/PIN, y monto contra las denominaciones disponibles.

Cada función devuelve (es_valido: bool, mensaje_error: str).
"""

from src.utils.constantes import (
    DENOMINACIONES,
    LONGITUD_CELULAR,
    LONGITUD_AHORRO_MANO,
    LONGITUD_CUENTA_AHORROS,
    LONGITUD_PIN,
)


def solo_digitos(cadena: str) -> bool:
    """True si `cadena` contiene ÚNICAMENTE dígitos 0-9 (sin signos, espacios, letras)."""
    return cadena is not None and str(cadena).isdigit()


def longitud_exacta(cadena: str, longitud: int) -> bool:
    return isinstance(cadena, str) and len(cadena) == longitud


def validar_celular(numero: str) -> tuple[bool, str]:
    """Retiro estilo NEQUI: 10 dígitos, debe iniciar en 3."""
    if not numero:
        return False, "Debe ingresar el número de celular."
    if not solo_digitos(numero):
        return False, "El número de celular solo puede contener dígitos (0-9)."
    if not longitud_exacta(numero, LONGITUD_CELULAR):
        return False, f"El número de celular debe tener exactamente {LONGITUD_CELULAR} dígitos."
    if numero[0] != "3":
        return False, "El número de celular debe iniciar en 3 (estándar de móviles en Colombia)."
    return True, ""


def validar_ahorro_mano(numero: str) -> tuple[bool, str]:
    """11 dígitos, primer dígito en {0,1}, segundo dígito obligatoriamente 3."""
    if not numero:
        return False, "Debe ingresar el vector de ahorro a la mano."
    if not solo_digitos(numero):
        return False, "El vector solo puede contener dígitos (0-9)."
    if not longitud_exacta(numero, LONGITUD_AHORRO_MANO):
        return False, f"El vector debe tener exactamente {LONGITUD_AHORRO_MANO} dígitos."
    if numero[0] not in ("0", "1"):
        return False, "El primer dígito debe ser 0 o 1 (no se admiten valores del 2 al 9)."
    if numero[1] != "3":
        return False, "El segundo dígito debe ser obligatoriamente 3."
    return True, ""


def validar_cuenta_ahorros(numero: str) -> tuple[bool, str]:
    """11 dígitos, solo 0-9."""
    if not numero:
        return False, "Debe ingresar el número de cuenta de ahorros."
    if not solo_digitos(numero):
        return False, "El número de cuenta solo puede contener dígitos (0-9)."
    if not longitud_exacta(numero, LONGITUD_CUENTA_AHORROS):
        return False, f"El número de cuenta debe tener exactamente {LONGITUD_CUENTA_AHORROS} dígitos."
    return True, ""


def validar_pin(pin: str) -> tuple[bool, str]:
    """Clave de 4 dígitos (nunca visible en pantalla)."""
    if not pin:
        return False, "Debe ingresar la clave."
    if not solo_digitos(pin):
        return False, "La clave solo puede contener dígitos (0-9)."
    if not longitud_exacta(pin, LONGITUD_PIN):
        return False, f"La clave debe tener exactamente {LONGITUD_PIN} dígitos."
    return True, ""


def validar_monto(monto, denominaciones=None) -> tuple[bool, str]:
    """El monto solo es representable si es múltiplo de la denominación
    más pequeña (10.000) — el cajero no maneja billetes de 5.000."""
    denominaciones = denominaciones or DENOMINACIONES
    menor_denominacion = min(denominaciones)

    try:
        monto = int(monto)
    except (TypeError, ValueError):
        return False, "El monto debe ser un valor numérico."

    if monto <= 0:
        return False, "El monto debe ser mayor a cero."

    if monto % menor_denominacion != 0:
        return (
            False,
            f"No se puede dispensar {monto:,}. El cajero solo entrega en múltiplos "
            f"de {menor_denominacion:,} usando billetes de "
            f"{', '.join(f'{d:,}' for d in sorted(denominaciones, reverse=True))}. "
            "Inicie el proceso nuevamente.",
        )

    return True, ""
