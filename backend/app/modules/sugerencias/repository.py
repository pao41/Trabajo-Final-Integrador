from sqlmodel import Session, func, select

from app.core.base_repository import BaseRepository
from app.modules.sugerencias.model import RutinaAsignada


class SugerenciaRepository(BaseRepository[RutinaAsignada]):
    def __init__(self, session: Session):
        super().__init__(RutinaAsignada, session)

    def listar(self, estado: str | None = None) -> list[RutinaAsignada]:
        """Las sugerencias, de la más nueva a la más vieja; opcionalmente de un solo estado."""
        consulta = select(RutinaAsignada).order_by(RutinaAsignada.id.desc())
        if estado:
            consulta = consulta.where(RutinaAsignada.estado == estado)
        return list(self.session.exec(consulta).all())

    def de_alumno(self, alumno_id: int) -> list[RutinaAsignada]:
        consulta = select(RutinaAsignada).where(RutinaAsignada.alumno_id == alumno_id)
        return list(self.session.exec(consulta).all())

    def existe_de_rutina(self, rutina_id: int) -> bool:
        """Indica si la rutina fue sugerida alguna vez a un alumno (en cualquier estado)."""
        consulta = select(RutinaAsignada.id).where(RutinaAsignada.rutina_id == rutina_id)
        return self.session.exec(consulta.limit(1)).first() is not None

    def conteo_aprobadas_por_alumno(self) -> dict[int, int]:
        """Cuántas rutinas aprobadas tiene cada alumno (los que no tienen ninguna no figuran)."""
        consulta = (
            select(RutinaAsignada.alumno_id, func.count())
            .where(RutinaAsignada.estado == "aprobada")
            .group_by(RutinaAsignada.alumno_id)
        )
        return {alumno_id: total for alumno_id, total in self.session.exec(consulta).all()}
