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
