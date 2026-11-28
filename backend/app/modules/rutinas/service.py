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
        self._validar_nombre(datos.nombre)
        rutina = Rutina(**datos.model_dump(), entrenador_id=entrenador_id)
        return RutinaPublic.model_validate(self.uow.rutinas.add(rutina))

    def editar(self, rutina_id: int, datos: RutinaDatos) -> RutinaPublic:
        """Modifica la rutina; conserva el entrenador que la cargó."""
        rutina = self.uow.rutinas.get_by_id(rutina_id)
        if not rutina:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Rutina no encontrada")
        self._validar_nombre(datos.nombre, rutina_id)
        for campo, valor in datos.model_dump().items():
            setattr(rutina, campo, valor)
        return RutinaPublic.model_validate(self.uow.rutinas.update(rutina))

    def eliminar(self, rutina_id: int) -> None:
        """Elimina una rutina que nunca se sugirió; con historial no se borra (RN28, RN47)."""
        rutina = self.uow.rutinas.get_by_id(rutina_id)
        if not rutina:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Rutina no encontrada")
        if self.uow.sugerencias.existe_de_rutina(rutina_id):
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                "No se puede eliminar una rutina que ya fue sugerida a un alumno",
            )
        self.uow.rutinas.delete(rutina)

    def _validar_nombre(self, nombre: str, propia_id: int | None = None) -> None:
        """El nombre no se repite en el banco (RN45); al editar se ignora la propia rutina."""
        otra = self.uow.rutinas.get_by_nombre(nombre)
        if otra and otra.id != propia_id:
            raise HTTPException(status.HTTP_409_CONFLICT, "Ya existe una rutina con ese nombre")
