from datetime import date

from app.core.uow import UnitOfWork
from app.modules.planes.model import Inscripcion


def calcular_estado(inscripcion: Inscripcion, hoy: date, dias_aviso: int) -> str:
    """Estado según la fecha de hoy (RN01, RN09) y, en planes por clases, el saldo (RN31)."""
    if hoy >= inscripcion.fecha_vencimiento or inscripcion.clases_restantes == 0:
        return "vencido"
    if (inscripcion.fecha_vencimiento - hoy).days < dias_aviso:
        return "por_vencer"
    return "activo"


class InscripcionService:
    """Inscripción de alumnos a los planes y control de su estado."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow
