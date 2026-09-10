"""
Utilidades generales: normalización de vectores/moneda y la clave
temporal de NEQUI. Se fusionaron aquí (antes eran 2 archivos separados)
porque cada uno tenía muy poco contenido por sí solo.
"""

import random
import time

from src.utils.constantes import (
    LONGITUD_VECTOR_INTERNO,
    LONGITUD_CLAVE_TEMPORAL,
    SEGUNDOS_VIGENCIA_CLAVE,
)


# --- Normalización de vectores y moneda ---------------------------------

def normalizar_interno(numero: str, longitud: int = LONGITUD_VECTOR_INTERNO) -> str:
    """
    Rellena `numero` con ceros a la izquierda hasta `longitud` dígitos.
    Uso EXCLUSIVAMENTE interno (llaves de almacenamiento/cuentas).
    El usuario jamás debe ver este valor.
    """
    numero = str(numero).strip()
    if len(numero) > longitud:
        raise ValueError(f"El número '{numero}' excede la longitud interna de {longitud} dígitos.")
    return numero.zfill(longitud)


def formatear_moneda(valor: int) -> str:
    """Formatea un entero como moneda estilo colombiano: $ 100.000"""
    return f"$ {valor:,.0f}".replace(",", ".")


# --- Clave temporal de NEQUI --------------------------------------------

def generar_clave(longitud: int = LONGITUD_CLAVE_TEMPORAL) -> str:
    """Genera una clave numérica aleatoria de `longitud` dígitos, como string."""
    return "".join(str(random.randint(0, 9)) for _ in range(longitud))


class ClaveTemporal:
    """
    Clave temporal con tiempo de expiración. Se usa en el flujo NEQUI: es
    visible 60 segundos y luego se regenera sola automáticamente.
    """

    def __init__(self, duracion_segundos: int = SEGUNDOS_VIGENCIA_CLAVE):
        self.duracion_segundos = duracion_segundos
        self.valor = generar_clave()
        self.creada_en = time.time()

    def segundos_restantes(self) -> int:
        return max(0, int(self.duracion_segundos - (time.time() - self.creada_en)))

    def vigente(self) -> bool:
        return self.segundos_restantes() > 0

    def regenerar(self) -> None:
        self.valor = generar_clave()
        self.creada_en = time.time()

    def asegurar_vigente(self) -> str:
        """Si la clave expiró, la regenera automáticamente. Devuelve el valor vigente."""
        if not self.vigente():
            self.regenerar()
        return self.valor
