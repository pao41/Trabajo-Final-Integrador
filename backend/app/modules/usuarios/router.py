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