from datetime import timedelta

from app.core.uow import UnitOfWork

# Tiempo que debe pasar entre dos ingresos del mismo alumno 
VENTANA = timedelta(hours=2)


class AsistenciaService:
    """Registro de ingresos al gimnasio (check-in manual desde el mostrador)."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow