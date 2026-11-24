from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.deps import require_role
from app.core.uow import UnitOfWork, get_uow
from app.modules.entrenadores.model import EntrenadorPublic
from app.modules.entrenadores.service import EntrenadorService
from app.modules.usuarios.model import UsuarioPublic

router = APIRouter(prefix="/entrenadores", tags=["Entrenadores"])

# Solo el administrador gestiona entrenadores
solo_admin = require_role(["administrador"])


@router.get("", response_model=list[EntrenadorPublic])
def listar(
    _admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        return EntrenadorService(uow).listar()