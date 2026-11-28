from sqlmodel import Session, func, select

from app.core.base_repository import BaseRepository
from app.modules.rutinas.model import Rutina


class RutinaRepository(BaseRepository[Rutina]):
    def __init__(self, session: Session):
        super().__init__(Rutina, session)

    def listar(self) -> list[Rutina]:
        return list(self.session.exec(select(Rutina).order_by(Rutina.tipo, Rutina.nombre)).all())

    def get_by_nombre(self, nombre: str) -> Rutina | None:
        """Busca por nombre sin distinguir mayúsculas ni espacios de los costados."""
        consulta = select(Rutina).where(func.lower(Rutina.nombre) == nombre.strip().lower())
        return self.session.exec(consulta).first()
