from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.uow import UnitOfWork, get_uow
from app.modules.pagos.model import PagoPublic
from app.modules.pagos.service import PagoService
from app.modules.planes.router import solo_admin
from app.modules.usuarios.model import UsuarioPublic

router = APIRouter(prefix="/pagos", tags=["Pagos"])


@router.get("", response_model=list[PagoPublic])
def listar(
    _admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    alumno_id: int | None = None,
):
    """Historial de pagos; con `alumno_id` muestra los de ese alumno."""
    with uow:
        return PagoService(uow).listar(alumno_id)
