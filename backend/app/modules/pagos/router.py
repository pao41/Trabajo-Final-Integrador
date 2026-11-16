from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.uow import UnitOfWork, get_uow
from app.modules.pagos.model import PagoDatos, PagoPublic, PagoRegistrado
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


@router.post("", response_model=PagoRegistrado, status_code=status.HTTP_201_CREATED)
def registrar(
    datos: PagoDatos,
    _admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        return PagoService(uow).registrar(datos)
