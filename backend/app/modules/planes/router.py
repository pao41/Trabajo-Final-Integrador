from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.deps import require_role
from app.core.uow import UnitOfWork, get_uow
from app.modules.planes.model import PlanPublic
from app.modules.planes.service import PlanService
from app.modules.usuarios.model import UsuarioPublic

router = APIRouter(prefix="/planes", tags=["Planes"])

# Solo el administrador gestiona planes y precios (RN36)
solo_admin = require_role(["administrador"])


@router.get("", response_model=list[PlanPublic])
def listar(
    _admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        return PlanService(uow).listar()
