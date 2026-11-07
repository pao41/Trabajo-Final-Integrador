from fastapi import HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.core.uow import UnitOfWork
from app.modules.usuarios.model import CambioPassword, Usuario, UsuarioCreate, UsuarioPublic


class UsuarioService:
    """Reglas de negocio de los usuarios del personal."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def crear(self, datos: UsuarioCreate) -> UsuarioPublic:
        """Crea un usuario; el nombre de usuario no se puede repetir."""
        self._validar_largo(datos.password)
        nombre = datos.nombre_usuario.strip().lower()
        if self.uow.usuarios.get_by_nombre_usuario(nombre):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un usuario con ese nombre",
            )
        # Por ahora todos son administradores; el perfil entrenador llega con su módulo
        usuario = Usuario(
            nombre_usuario=nombre,
            password_hash=hash_password(datos.password),
            rol="administrador",
        )
        return UsuarioPublic.model_validate(self.uow.usuarios.add(usuario))

    