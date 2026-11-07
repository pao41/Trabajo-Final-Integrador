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

    def autenticar(self, nombre_usuario: str, password: str) -> str:
        """Valida usuario y contraseña y devuelve el token de sesión."""
        usuario = self.uow.usuarios.get_by_nombre_usuario(nombre_usuario.strip().lower())
        # El mismo mensaje si falla el usuario, la contraseña o la cuenta está desactivada
        datos_validos = usuario is not None and verify_password(password, usuario.password_hash)
        if not datos_validos or not usuario.activo:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos",
            )
        return create_access_token(usuario.id, usuario.rol)

    def listar(self) -> list[UsuarioPublic]:
        return [UsuarioPublic.model_validate(u) for u in self.uow.usuarios.get_all()]

    def cambiar_estado(self, usuario_id: int, activo: bool, quien_actua_id: int) -> UsuarioPublic:
        """Activa o desactiva un usuario (no se eliminan); nadie puede desactivarse a sí mismo."""
        if not activo and usuario_id == quien_actua_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="No podés desactivar tu propio usuario",
            )
        usuario = self._buscar(usuario_id)
        usuario.activo = activo
        return UsuarioPublic.model_validate(self.uow.usuarios.update(usuario))

    def restablecer_password(self, usuario_id: int, datos: CambioPassword) -> None:
        """Reemplaza la contraseña de un usuario (la restablece el administrador)."""
        self._validar_largo(datos.nueva_password)
        usuario = self._buscar(usuario_id)
        usuario.password_hash = hash_password(datos.nueva_password)
        self.uow.usuarios.update(usuario)

    def _buscar(self, usuario_id: int) -> Usuario:
        usuario = self.uow.usuarios.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )
        return usuario

    def _validar_largo(self, password: str) -> None:
        # bcrypt solo admite hasta 72 bytes (una letra con tilde ocupa 2)
        if len(password.encode("utf-8")) > 72:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="La contraseña es demasiado larga",
            )