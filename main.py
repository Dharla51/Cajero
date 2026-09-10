

from src.repositories.cuenta_repository import reiniciar_cuentas
from src.services.caja_service import recargar_caja
from src.ui.main_window import iniciar_app

if __name__ == "__main__":
    reiniciar_cuentas()
    recargar_caja()
    iniciar_app()
