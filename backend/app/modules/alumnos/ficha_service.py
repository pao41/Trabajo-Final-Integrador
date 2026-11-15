from fastapi import HTTPException, status

from app.core.uow import UnitOfWork
from app.modules.alumnos.model import (
    FichaSalud,
    FichaSaludDatos,
    FichaSaludPublic,
    MetaAlumno,
    MetaDatos,
    MetaPublic,
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

    def guardar_ficha(self, alumno_id: int, datos: FichaSaludDatos) -> FichaSaludPublic:
        """Crea la ficha del alumno o, si ya existe, la modifica (una por alumno)."""
        self._comprobar_alumno(alumno_id)
        ficha = self.uow.fichas_salud.get_by_alumno(alumno_id)
        if not ficha:
            ficha = self.uow.fichas_salud.add(FichaSalud(alumno_id=alumno_id))
        ficha.problemas_cardiacos = datos.problemas_cardiacos
        ficha.lesiones = datos.lesiones
        ficha.observaciones = datos.observaciones
        return FichaSaludPublic.model_validate(self.uow.fichas_salud.update(ficha))

    def obtener_meta(self, alumno_id: int) -> MetaPublic:
        self._comprobar_alumno(alumno_id)
        meta = self.uow.metas.get_by_alumno(alumno_id)
        # Si todavía no se configuró, se informa la meta por defecto
        if not meta:
            return MetaPublic()
        return MetaPublic.model_validate(meta)

    def guardar_meta(self, alumno_id: int, datos: MetaDatos) -> MetaPublic:
        """Crea o modifica la meta semanal del alumno."""
        self._comprobar_alumno(alumno_id)
        meta = self.uow.metas.get_by_alumno(alumno_id)
        if not meta:
            meta = self.uow.metas.add(MetaAlumno(alumno_id=alumno_id))
        meta.meta_asistencias_semanales = datos.meta_asistencias_semanales
        return MetaPublic.model_validate(self.uow.metas.update(meta))

    def _comprobar_alumno(self, alumno_id: int) -> None:
        if not self.uow.alumnos.get_by_id(alumno_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado",
            )
