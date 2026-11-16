from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.uow import UnitOfWork, get_uow
from app.modules.planes.inscripcion_service import InscripcionService
from app.modules.planes.model import InscripcionPublic
from app.modules.planes.router import solo_admin
from app.modules.usuarios.model import UsuarioPublic

router = APIRouter(prefix="/inscripciones", tags=["Inscripciones"])


@router.get("", response_model=list[InscripcionPublic])
def listar(
    _admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    alumno_id: int | None = None,
):
    """Lista las inscripciones; con `alumno_id` muestra las de ese alumno."""
    with uow:
        return InscripcionService(uow).listar(alumno_id)
