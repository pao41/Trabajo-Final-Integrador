from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.modules.usuarios.model import Usuario


class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self, session: Session):
        super().__init__(Usuario, session)

    def get_by_nombre_usuario(self, nombre_usuario: str) -> Usuario | None:
        consulta = select(Usuario).where(Usuario.nombre_usuario == nombre_usuario)
        return self.session.exec(consulta).first()