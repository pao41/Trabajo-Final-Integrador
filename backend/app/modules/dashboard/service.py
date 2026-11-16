from app.core.uow import UnitOfWork

SEMANAS = 4
METODOS_PAGO = ["efectivo", "transferencia", "debito", "credito"]


class DashboardService:
    """Calcula los indicadores del dashboard con la fecha de hoy."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow