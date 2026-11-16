from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.modules.planes.model import Plan


class PlanRepository(BaseRepository[Plan]):
    def __init__(self, session: Session):
        super().__init__(Plan, session)

    def get_by_nombre(self, nombre: str) -> Plan | None:
        consulta = select(Plan).where(Plan.nombre == nombre)
        return self.session.exec(consulta).first()

    def listar(self) -> list[Plan]:
        return list(self.session.exec(select(Plan).order_by(Plan.nombre)).all())
