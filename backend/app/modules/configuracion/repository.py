from sqlmodel import Session

from app.core.base_repository import BaseRepository
from app.modules.configuracion.model import Configuracion


class ConfiguracionRepository(BaseRepository[Configuracion]):
    def __init__(self, session: Session):
        super().__init__(Configuracion, session)

    def get_actual(self) -> Configuracion | None:
        """La configuración es una sola fila, siempre la del id 1."""
        return self.get_by_id(1)
