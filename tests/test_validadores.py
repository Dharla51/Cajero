from src.validators.validadores import (
    validar_celular,
    validar_ahorro_mano,
    validar_cuenta_ahorros,
    validar_pin,
    validar_monto,
)


def test_celular_valido():
    assert validar_celular("3001234567")[0] is True


def test_celular_letras_invalido():
    assert validar_celular("30012A4567")[0] is False


def test_celular_longitud_invalida():
    assert validar_celular("300123456")[0] is False


def test_celular_debe_iniciar_en_3():
    ok, msg = validar_celular("4001234567")
    assert ok is False
    assert "3" in msg


def test_ahorro_mano_valido():
    assert validar_ahorro_mano("03345566778")[0] is True
    assert validar_ahorro_mano("13345566778")[0] is True


def test_ahorro_mano_primer_digito_invalido():
    ok, _ = validar_ahorro_mano("23345566778")
    assert ok is False


def test_ahorro_mano_segundo_digito_invalido():
    ok, _ = validar_ahorro_mano("04345566778")
    assert ok is False


def test_cuenta_ahorros_valida():
    assert validar_cuenta_ahorros("50123456789")[0] is True


def test_cuenta_ahorros_caracter_especial():
    assert validar_cuenta_ahorros("501234567-9")[0] is False


def test_pin_valido():
    assert validar_pin("1234")[0] is True


def test_pin_longitud_invalida():
    assert validar_pin("123")[0] is False


def test_monto_multiplo_valido():
    assert validar_monto(150000)[0] is True


def test_monto_no_multiplo_invalido():
    ok, msg = validar_monto(145000)
    assert ok is False
    assert "reiniciar" in msg.lower() or "múltiplos" in msg.lower()
