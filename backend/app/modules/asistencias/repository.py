from datetime import date

from sqlmodel import Session, func, select

from app.core.base_repository import BaseRepository
from app.modules.asistencias.model import Asistencia


class AsistenciaRepository(BaseRepository[Asistencia]):
    def __init__(self, session: Session):
        super().__init__(Asistencia, session)

    def ultima_de_alumno(self, alumno_id: int) -> Asistencia | None:
        consulta = select(Asistencia).where(Asistencia.alumno_id == alumno_id)
        orden = (Asistencia.fecha.desc(), Asistencia.hora.desc(), Asistencia.id.desc())
        return self.session.exec(consulta.order_by(*orden)).first()

    def listar(self, alumno_id: int | None = None, fecha: date | None = None) -> list[Asistencia]:
        """Los ingresos más nuevos primero; se puede filtrar por alumno y por día."""
        orden = (Asistencia.fecha.desc(), Asistencia.hora.desc(), Asistencia.id.desc())
        consulta = select(Asistencia).order_by(*orden)
        if alumno_id is not None:
            consulta = consulta.where(Asistencia.alumno_id == alumno_id)
        if fecha is not None:
            consulta = consulta.where(Asistencia.fecha == fecha)
        return list(self.session.exec(consulta.limit(200)).all())

    def contar_entre(self, alumno_id: int, desde: date, hasta: date) -> int:
        """Cantidad de ingresos del alumno entre dos fechas, ambas incluidas."""
        consulta = select(func.count()).select_from(Asistencia)
        consulta = consulta.where(
            Asistencia.alumno_id == alumno_id,
            Asistencia.fecha >= desde,
            Asistencia.fecha <= hasta,
        )
        return self.session.exec(consulta).one()
