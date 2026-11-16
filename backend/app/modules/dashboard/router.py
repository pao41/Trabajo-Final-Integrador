from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.deps import require_role
from app.core.uow import UnitOfWork, get_uow
from app.modules.dashboard.model import DashboardPublic
from app.modules.dashboard.service import DashboardService
from app.modules.usuarios.model import UsuarioPublic

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# Solo el administrador ve la facturación y los indicadores
solo_admin = require_role(["administrador"])


@router.get("", response_model=DashboardPublic)
def obtener(
    _admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    """Indicadores del mes en curso y de las últimas semanas."""
    with uow:
        return DashboardService(uow).obtener()