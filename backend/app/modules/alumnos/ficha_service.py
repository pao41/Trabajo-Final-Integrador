from app.core.uow import UnitOfWork
from app.modules.alumnos.model import (
    FichaSaludPublic,
)


class FichaMetaService:
    """Ficha de salud y meta semanal de cada alumno."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def obtener_ficha(self, alumno_id: int) -> FichaSaludPublic:
        self._comprobar_alumno(alumno_id)
        ficha = self.uow.fichas_salud.get_by_alumno(alumno_id)
        # Si todavía no se cargó, se devuelve una ficha vacía
        if not ficha:
            return FichaSaludPublic()
        return FichaSaludPublic.model_validate(ficha)