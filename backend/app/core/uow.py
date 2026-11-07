from sqlmodel import Session

from app.core.database import engine
from app.modules.usuarios.repository import UsuarioRepository


class UnitOfWork:
    """Abre una sesión y, al terminar el bloque with, confirma todo junto o lo descarta."""

    def __init__(self):
        self.session: Session | None = None

    def __enter__(self):
        # expire_on_commit=False deja los objetos legibles después del commit
        self.session = Session(engine, expire_on_commit=False)
        # Acá se crea el repositorio de cada módulo (una línea por módulo)
        self.usuarios = UsuarioRepository(self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                self.session.rollback()
            else:
                self.session.commit()
        finally:
            # La sesión se cierra siempre, aunque el commit falle
            self.session.close()


def get_uow() -> UnitOfWork:
    """Dependencia de FastAPI: entrega un Unit of Work por petición."""
    return UnitOfWork()