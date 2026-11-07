from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.core.deps import get_current_user, require_role
from app.core.uow import UnitOfWork, get_uow
from app.modules.usuarios.model import CambioPassword, UsuarioCreate, UsuarioPublic
from app.modules.usuarios.service import UsuarioService

auth_router = APIRouter(prefix="/auth", tags=["Autenticación"])
router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# Solo el administrador gestiona usuarios
solo_admin = require_role(["administrador"])


@auth_router.post("/token")
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    response: Response,
):
    """Valida usuario y contraseña y deja el token en una cookie HttpOnly."""
    with uow:
        token = UsuarioService(uow).autenticar(form.username, form.password)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
        max_age=settings.access_token_expire_minutes * 60,
    )
    return {"mensaje": "Sesión iniciada"}


@auth_router.post("/logout")
def logout(response: Response):
    """Borra la cookie de sesión."""
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
    )
    return {"mensaje": "Sesión cerrada"}


@auth_router.get("/me", response_model=UsuarioPublic)
def me(usuario: Annotated[UsuarioPublic, Depends(get_current_user)]):
    """Devuelve quién tiene la sesión iniciada."""
    return usuario


@router.get("", response_model=list[UsuarioPublic])
def listar(
    _admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        return UsuarioService(uow).listar()


@router.post("", response_model=UsuarioPublic, status_code=status.HTTP_201_CREATED)
def crear(
    datos: UsuarioCreate,
    _admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        return UsuarioService(uow).crear(datos)


@router.patch("/{usuario_id}/desactivar", response_model=UsuarioPublic)
def desactivar(
    usuario_id: int,
    admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        return UsuarioService(uow).cambiar_estado(usuario_id, False, admin.id)


@router.patch("/{usuario_id}/activar", response_model=UsuarioPublic)
def activar(
    usuario_id: int,
    admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        return UsuarioService(uow).cambiar_estado(usuario_id, True, admin.id)


@router.put("/{usuario_id}/password", status_code=status.HTTP_204_NO_CONTENT)
def restablecer_password(
    usuario_id: int,
    datos: CambioPassword,
    _admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        UsuarioService(uow).restablecer_password(usuario_id, datos)