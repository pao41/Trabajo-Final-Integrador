from sqlmodel import Session, select

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
