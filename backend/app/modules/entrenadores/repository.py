from sqlmodel import Session, func, select

from app.core.base_repository import BaseRepository
from app.modules.entrenadores.model import Entrenador


class EntrenadorRepository(BaseRepository[Entrenador]):
    def __init__(self, session: Session):
        super().__init__(Entrenador, session)

    def listar(self) -> list[Entrenador]:
        return list(self.session.exec(select(Entrenador).order_by(Entrenador.nombre)).all())

    def get_by_nombre(self, nombre: str) -> Entrenador | None:
        """Busca por nombre sin distinguir mayúsculas ni espacios de los costados."""
        consulta = select(Entrenador).where(func.lower(Entrenador.nombre) == nombre.strip().lower())
        return self.session.exec(consulta).first()
