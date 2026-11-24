from typing import Annotated

from fastapi import Depends, HTTPException, Request, status

from app.core.security import decode_access_token, decode_alumno_token
from app.core.uow import UnitOfWork, get_uow
from app.modules.alumnos.model import AlumnoPublic
from app.modules.usuarios.model import UsuarioPublic

# Cookie de la sesión del alumno (distinta de la del personal)
COOKIE_ALUMNO = "alumno_token"


def get_current_user(
    request: Request,
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> UsuarioPublic:
    """Identifica a quien hace la petición a partir de la cookie de sesión."""
    # El token se lee solo de la cookie HttpOnly
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No hay una sesión iniciada",
        )
    datos = decode_access_token(token)
    if datos is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="La sesión es inválida o venció",
        )
    with uow:
        usuario = uow.usuarios.get_by_id(int(datos["sub"]))
        # Se consulta la base en cada petición: una cuenta desactivada pierde el acceso enseguida
        if not usuario or not usuario.activo:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="La sesión es inválida o venció",
            )
        return UsuarioPublic.model_validate(usuario)


def require_role(roles: list[str]):
    """Crea una dependencia que solo deja pasar a los perfiles indicados."""

    def comprobar(
        usuario: Annotated[UsuarioPublic, Depends(get_current_user)],
    ) -> UsuarioPublic:
        if usuario.rol not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tenés permiso para realizar esta acción",
            )
        return usuario

    return comprobar


def get_alumno_actual(
    request: Request,
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> AlumnoPublic:
    """Identifica al alumno que hace la petición a partir de su cookie de sesión."""
    token = request.cookies.get(COOKIE_ALUMNO)
    datos = decode_alumno_token(token) if token else None
    if datos is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "No hay una sesión iniciada")
    with uow:
        alumno = uow.alumnos.get_by_id(int(datos["sub"]))
        # Si lo dieron de baja después de entrar, pierde el acceso enseguida
        if not alumno or not alumno.activo:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "La sesión es inválida o venció")
        return AlumnoPublic.model_validate(alumno)