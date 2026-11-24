from fastapi import HTTPException, status

from app.core.uow import UnitOfWork
from app.modules.rutinas.model import Rutina, RutinaDatos, RutinaPublic


class RutinaService:
    """Reglas de negocio del banco de rutinas, que carga y mantiene el entrenador."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def listar(self) -> list[RutinaPublic]:
        return [RutinaPublic.model_validate(r) for r in self.uow.rutinas.listar()]

    def crear(self, datos: RutinaDatos, entrenador_id: int) -> RutinaPublic:
        """Carga una rutina a nombre del entrenador que la crea (RN24, RN35)."""
        rutina = Rutina(**datos.model_dump(), entrenador_id=entrenador_id)
        return RutinaPublic.model_validate(self.uow.rutinas.add(rutina))

    def editar(self, rutina_id: int, datos: RutinaDatos) -> RutinaPublic:
        """Modifica la rutina; conserva el entrenador que la cargó."""
        rutina = self.uow.rutinas.get_by_id(rutina_id)
        if not rutina:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Rutina no encontrada")
        for campo, valor in datos.model_dump().items():
            setattr(rutina, campo, valor)
        return RutinaPublic.model_validate(self.uow.rutinas.update(rutina))