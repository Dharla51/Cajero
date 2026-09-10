from cajero_automatico.src.services import caja_service
from src.repositories.inventario_repository import guardar_inventario
from src.utils.constantes import INVENTARIO_INICIAL


def test_hay_disponibilidad_true():
    guardar_inventario({100000: 10, 50000: 10, 20000: 10, 10000: 10})
    assert caja_service.hay_disponibilidad({100000: 2, 50000: 1}) is True


def test_hay_disponibilidad_false():
    guardar_inventario({100000: 1, 50000: 0, 20000: 0, 10000: 0})
    assert caja_service.hay_disponibilidad({100000: 5}) is False


def test_calcular_deficit_es_la_resta_valor_inicial_menos_lo_que_hay():
    actual = {100000: 30, 50000: 40, 20000: 40, 10000: 40}
    deficit = caja_service.calcular_deficit(actual)
    # 40(inicial) - 30(actual) = 10 billetes de 100.000 por agregar; el resto ya está al máximo
    assert deficit == {100000: 10, 50000: 0, 20000: 0, 10000: 0}


def test_recargar_inventario_suma_el_deficit_no_sobrescribe():
    # Solo el 100.000 está corto; los demás YA están completos.
    guardar_inventario({100000: 5, 50000: 40, 20000: 40, 10000: 40})
    detalle = caja_service.recargar_caja()
    assert detalle == {100000: 35, 50000: 0, 20000: 0, 10000: 0}
    inventario = caja_service.obtener_caja()
    assert inventario == dict(INVENTARIO_INICIAL)


def test_recarga_automatica_solo_cuando_falta_stock():
    # Inventario suficiente -> NO debe recargar (devuelve None)
    guardar_inventario(dict(INVENTARIO_INICIAL))
    detalle = caja_service.descontar_o_recargar({100000: 1})
    assert detalle is None

    # Inventario agotado -> SÍ debe recargar (devuelve el detalle) antes de descontar
    guardar_inventario({100000: 0, 50000: 0, 20000: 1, 10000: 0})
    detalle = caja_service.descontar_o_recargar({100000: 2})
    assert detalle is not None
    assert detalle[100000] == INVENTARIO_INICIAL[100000]  # se agregaron todos, no había ninguno
    inventario = caja_service.obtener_caja()
    assert caja_service.valor_total_caja(inventario) > 0
