"""
Algoritmo del acarreo
"""

Billete = [100000, 50000, 20000, 10000]  

#Niveles de los billetes 

Matriz = [
    [0, 1, 2, 3],  
    [0, 1, 2],     
    [0, 1],        
    [0],           
]


def ColocarBil(permitidos, restante):
    "poner 1 en la fila de los billetes que se pueden usar, y devolver el restante"
    fila = [0, 0, 0, 0]
    for i in range(len(permitidos) - 1, -1, -1):
        idx = permitidos[i]
        if Billete[idx] <= restante:
            fila[idx] = 1
            restante -= Billete[idx]
    return fila, restante


def generar_matriz_acarreo(monto: int) -> dict:
    
    "es la matriz de acarreo, con las filas de billetes y el conteo total por denominación"
    
    if not isinstance(monto, int) or monto <= 0 or monto % 10000 != 0:
        return {"filas": [], "conteo": [0, 0, 0, 0], "restante": monto}

    filas = []
    restante = monto
    nivel = 0

    while restante > 0:
        fila, nuevo_restante = ColocarBil(Matriz[nivel], restante)

        if any(v == 1 for v in fila):
            filas.append(fila)
            restante = nuevo_restante
            nivel = (nivel + 1) % len(Matriz)  # avanzar nivel
        else:
            # Reinicio: fila de ceros
            filas.append([0, 0, 0, 0])

            reinicio, r2 = ColocarBil([0, 1, 2, 3], restante)
            if any(v == 1 for v in reinicio):
                filas.append(reinicio)
                restante = r2
                nivel = 1  # después del reinicio continuamos desde nivel 2
            else:
                break

    conteo = [0, 0, 0, 0]
    for fila in filas:
        for i in range(4):
            conteo[i] += fila[i]

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
        100000: conteo[0],
        50000: conteo[1],
        20000: conteo[2],
        10000: conteo[3],
    }


def _fila_a_detalle(fila_bits: list) -> dict:
    return {
        10000: fila_bits[3],
        20000: fila_bits[2],
        50000: fila_bits[1],
        100000: fila_bits[0],
    }


def _adaptar_matriz(filas_crudas: list) -> list:
    matriz = []
    intento = 1
    ciclo = 1
    for fila_bits in filas_crudas:
        es_reinicio = all(v == 0 for v in fila_bits)
        matriz.append(
            {
                "intento": intento,
                "ciclo": ciclo,
                "detalle": _fila_a_detalle(fila_bits),
                "reinicio": es_reinicio,
            }
        )
        if es_reinicio:
            ciclo += 1
            intento = 1
        else:
            intento += 1
    return matriz


def ejecutar_acarreo(monto: int) -> dict:
    crudo = generar_matriz_acarreo(monto)
    billetes = calcular_billetes(monto)
    matriz = _adaptar_matriz(crudo["filas"])

    return {
        "monto": monto,
        "billetes": billetes,
        "total_billetes": sum(billetes.values()),
        "valor_verificado": sum(d * c for d, c in billetes.items()),
        "matriz_intentos": matriz,
        "combinaciones_posibles": contar_combinaciones(monto),
    }
