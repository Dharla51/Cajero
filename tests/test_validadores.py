from src.Logic.acarreo import calcular_billetes, generar_matriz_acarreo
from src.validators.validadores import validar_celular


def test_validar_celular_rechaza_digito_inicial_distinto_a_tres():
    ok, msg = validar_celular("1234567890")
    assert ok is False
    assert "iniciar en 3" in msg


def test_validar_celular_acepta_numero_que_empieza_en_tres():
    ok, msg = validar_celular("3001234567")
    assert ok is True
    assert msg == ""


def test_acarreo_usa_orden_de_denominaciones_esperado():
    resultado = generar_matriz_acarreo(300000)
    assert resultado["conteo"] == [1, 2, 3, 1]
    assert calcular_billetes(300000) == {10000: 1, 20000: 2, 50000: 3, 100000: 1}
