from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.modules.entrenadores.model import Entrenador


class EntrenadorRepository(BaseRepository[Entrenador]):
    def __init__(self, session: Session):
        super().__init__(Entrenador, session)

    def listar(self) -> list[Entrenador]:
        return list(self.session.exec(select(Entrenador).order_by(Entrenador.nombre)).all())
