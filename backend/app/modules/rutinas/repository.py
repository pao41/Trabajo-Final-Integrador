from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.modules.rutinas.model import Rutina


class RutinaRepository(BaseRepository[Rutina]):
    def __init__(self, session: Session):
        super().__init__(Rutina, session)

    def listar(self) -> list[Rutina]:
        return list(self.session.exec(select(Rutina).order_by(Rutina.tipo, Rutina.nombre)).all())
