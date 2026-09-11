"""
Constantes globales del cajero automático.
Aquí se centraliza todo lo "configurable" para que el resto del código
no tenga números mágicos regados por todas partes.
"""

DENOMINACIONES = [100000, 50000, 20000, 10000]
DENOMINACIONES_ASC = [10000, 20000, 50000, 100000]


LONGITUD_VECTOR_INTERNO = 16

# Longitudes de vectores "públicos" (los que digita/ve el usuario)
LONGITUD_CELULAR = 10          # Retiro tipo NEQUI
LONGITUD_REPORTE_NEQUI = 11    # Reporte final (se antepone un 0)
LONGITUD_AHORRO_MANO = 11
LONGITUD_CUENTA_AHORROS = 11

LONGITUD_PIN = 4
LONGITUD_CLAVE_TEMPORAL = 6
SEGUNDOS_VIGENCIA_CLAVE = 60

# Montos fijos preestablecidos por cada tipo de retiro (más la opción "otro")
MONTOS_FIJOS = {
    "nequi": [20000, 50000, 100000, 200000],
    "ahorro_mano": [30000, 100000, 150000, 300000],
    "cuenta_ahorros": [50000, 200000, 400000, 600000],
}

# --- Inventario de billetes ---
# Cantidad inicial de billetes disponibles en el cajero, por denominación.
INVENTARIO_INICIAL = {
    100000: 40,
    50000: 40,
    20000: 40,
    10000: 40,
}

# La recarga del inventario ahora ocurre SOLO cuando se agota (no por un
# umbral preventivo) — ver src/services/inventario_service.py

TIPOS_RETIRO = ("nequi", "ahorro_mano", "cuenta_ahorros")
