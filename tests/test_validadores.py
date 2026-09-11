from src.validators.validadores import validar_celular


def test_validar_celular_rechaza_digito_inicial_distinto_a_tres():
    ok, msg = validar_celular("1234567890")
    assert ok is False
    assert "iniciar en 3" in msg


def test_validar_celular_acepta_numero_que_empieza_en_tres():
    ok, msg = validar_celular("3001234567")
    assert ok is True
    assert msg == ""
