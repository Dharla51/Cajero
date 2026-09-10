from src.algorithms.acarreo import ejecutar_acarreo, generar_matriz_acarreo, calcular_billetes


def test_calculo_200000_ejemplo_manuscrito():
    # Validado contra el ejemplo manuscrito: 200.000 -> 10k(1) 20k(2) 50k(1) 100k(1)
    billetes = calcular_billetes(200000)
    assert billetes == {100000: 1, 50000: 1, 20000: 2, 10000: 1}


def test_calculo_300000_ejemplo_manuscrito():
    # Validado contra el ejemplo manuscrito: 300.000 -> 10k(1) 20k(2) 50k(3) 100k(1)
    billetes = calcular_billetes(300000)
    assert billetes == {100000: 1, 50000: 3, 20000: 2, 10000: 1}


def test_matriz_300000_coincide_con_hoja_manuscrita():
    # Fila 1: 10k+20k+50k+100k (180.000) | Fila 2: 20k+50k (70.000) | Fila 3: 50k (50.000)
    resultado = ejecutar_acarreo(300000)
    matriz = resultado["matriz_intentos"]
    assert len(matriz) == 3
    assert matriz[0]["detalle"] == {10000: 1, 20000: 1, 50000: 1, 100000: 1}
    assert matriz[1]["detalle"] == {10000: 0, 20000: 1, 50000: 1, 100000: 0}
    assert matriz[2]["detalle"] == {10000: 0, 20000: 0, 50000: 1, 100000: 0}
    assert not any(f["reinicio"] for f in matriz)


def test_matriz_siempre_evalua_10000_primero():
    # El orden de evaluación de cada fila SIEMPRE debe iniciar en el billete de 10.000
    resultado = ejecutar_acarreo(890000)
    for fila in resultado["matriz_intentos"]:
        claves = list(fila["detalle"].keys())
        assert claves[0] == 10000


def test_reinicio_es_una_fila_de_ceros():
    # Cuando un nivel ya no cabe en el restante, se marca una fila de puros
    # ceros (reinicio) antes de continuar con las 4 denominaciones de nuevo.
    resultado = ejecutar_acarreo(130000)
    filas_reinicio = [f for f in resultado["matriz_intentos"] if f["reinicio"]]
    assert len(filas_reinicio) >= 1
    for f in filas_reinicio:
        assert all(v == 0 for v in f["detalle"].values())


def test_acarreo_valor_total_coincide_con_monto():
    for monto in [130000, 200000, 300000, 890000, 990000]:
        resultado = ejecutar_acarreo(monto)
        assert resultado["valor_verificado"] == monto


def test_monto_no_multiplo_de_10000_no_genera_billetes():
    billetes = calcular_billetes(145000)
    assert billetes == {100000: 0, 50000: 0, 20000: 0, 10000: 0}


def test_generar_matriz_acarreo_monto_invalido():
    resultado = generar_matriz_acarreo(145000)
    assert resultado["filas"] == []
    assert resultado["conteo"] == [0, 0, 0, 0]


def test_ejecutar_acarreo_incluye_combinaciones_posibles():
    resultado = ejecutar_acarreo(300000)
    assert resultado["combinaciones_posibles"] > 0
