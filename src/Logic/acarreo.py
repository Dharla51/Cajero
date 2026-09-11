"Algoritmo de acarreo"

from src.utils.constantes import DENOMINACIONES


def calcular_retiro_carreo(monto: int) -> list[int]:
    """Devuelve la cantidad de billetes por denominación, sin usar matriz."""
    cantidad = [0 for _ in DENOMINACIONES]
    if not isinstance(monto, int) or monto <= 0 or monto % DENOMINACIONES[0] != 0:
        return cantidad

    restante = monto
    while restante > 0:
        antes = restante
        for skip in range(len(DENOMINACIONES)):
            for j in range(skip, len(DENOMINACIONES)):
                valor = DENOMINACIONES[j]
                if restante < valor:
                    break
                cantidad[j] += 1
                restante -= valor
        if restante == antes:
            break
    return cantidad


def calcularRetiroCarreo(monto: int) -> list[int]:
    return calcular_retiro_carreo(monto)


def generar_matriz_acarreo(monto: int) -> dict:
    """Devuelve todo el recorrido de la matriz del acarreo y el conteo final."""
    if not isinstance(monto, int) or monto <= 0 or monto % DENOMINACIONES[0] != 0:
        return {"filas": [], "conteo": [0, 0, 0, 0], "restante": monto}

    filas = []
    conteo = [0, 0, 0, 0]
    restante = monto
    nivel = 0
    intento = 1
    ciclo = 1

    while restante > 0:
        fila = [0, 0, 0, 0]
        for idx in range(nivel, len(DENOMINACIONES)):
            valor = DENOMINACIONES[idx]
            if valor <= restante:
                fila[idx] = 1
                restante -= valor

        detalle = {
            10000: fila[0],
            20000: fila[1],
            50000: fila[2],
            100000: fila[3],
        }

        reinicio = all(v == 0 for v in fila)
        filas.append(
            {
                "intento": intento,
                "ciclo": ciclo,
                "detalle": detalle,
                "reinicio": reinicio,
            }
        )

        for i, valor in enumerate(fila):
            conteo[i] += valor

        if reinicio:
            nivel = 0
            ciclo += 1
            intento = 1
            continue

        if nivel == len(DENOMINACIONES) - 1:
            nivel = 0
            ciclo += 1
            intento = 1
        else:
            nivel += 1
            intento += 1

    return {"filas": filas, "conteo": conteo, "restante": restante}


def contar_combinaciones(monto: int) -> int:
    """
    Cuenta cuántas combinaciones distintas de billetes suman `monto`
    """
    if not isinstance(monto, int) or monto <= 0 or monto % 10000 != 0:
        return 0

    unidades = monto // 10000  # convertir a múltiplos de 10k
    valores = [1, 2, 5, 10]    # billetes en unidades de 10k
    dp = [0] * (unidades + 1)
    dp[0] = 1

    for v in valores:
        for i in range(v, unidades + 1):
            dp[i] += dp[i - v]

    return dp[unidades]


# ---------------------------------------------------------------------
# ---------------------------------------------------------------------

def calcular_billetes(monto: int) -> dict:
    resultado = generar_matriz_acarreo(monto)
    conteo = resultado["conteo"]
    return {
        10000: conteo[0],
        20000: conteo[1],
        50000: conteo[2],
        100000: conteo[3],
    }


def ejecutar_acarreo(monto: int) -> dict:
    crudo = generar_matriz_acarreo(monto)
    cantidad = crudo["conteo"]
    billetes = {
        10000: cantidad[0],
        20000: cantidad[1],
        50000: cantidad[2],
        100000: cantidad[3],
    }

    matriz = []
    for fila in crudo["filas"]:
        detalle = fila["detalle"]
        matriz.append(
            {
                "intento": fila["intento"],
                "ciclo": fila["ciclo"],
                "detalle": detalle,
                "reinicio": fila["reinicio"],
            }
        )

    return {
        "monto": monto,
        "billetes": billetes,
        "total_billetes": sum(billetes.values()),
        "valor_verificado": sum(d * c for d, c in billetes.items()),
        "matriz_intentos": matriz,
        "combinaciones_posibles": contar_combinaciones(monto),
    }
