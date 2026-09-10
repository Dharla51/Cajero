import pytest

from src.services import retiro_service
from src.services.retiro_service import RetiroError
from src.repositories.cuenta_repository import reiniciar_cuentas
from cajero_automatico.src.services.caja_service import recargar_caja


@pytest.fixture(autouse=True)
def datos_limpios():
    """Cada prueba arranca con cuentas e inventario frescos (cajero de prueba)."""
    reiniciar_cuentas()
    recargar_caja()
    yield


def test_retiro_nequi_monto_invalido():
    with pytest.raises(RetiroError):
        retiro_service.retiro_nequi("3009998877", 145000)


def test_retiro_nequi_celular_con_letras():
    with pytest.raises(RetiroError):
        retiro_service.retiro_nequi("30A9998877", 50000)


def test_retiro_ahorro_mano_no_requiere_cuenta_previa():
    # Como es un cajero de prueba, cualquier vector válido crea su cuenta
    # automáticamente la primera vez que se usa.
    resultado = retiro_service.retiro_ahorro_mano("03345566778", "1234", 30000)
    assert resultado["monto"] == 30000
    assert resultado["valor_verificado"] == 30000


def test_retiro_ahorro_mano_clave_incorrecta_en_segundo_intento():
    # Primer uso: registra la cuenta con clave 1234
    retiro_service.retiro_ahorro_mano("03345566778", "1234", 30000)
    # Segundo uso con clave distinta: debe fallar
    with pytest.raises(RetiroError):
        retiro_service.retiro_ahorro_mano("03345566778", "9999", 30000)


def test_retiro_cuenta_ahorros_tambien_se_autocrea():
    resultado = retiro_service.procesar_retiro_cuenta_ahorros("50123456789", "1234", 50000)
    assert resultado["monto"] == 50000
