from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.deps import require_role
from app.core.uow import UnitOfWork, get_uow
from app.modules.alumnos.model import AlumnoPublic
from app.modules.alumnos.service import AlumnoService
from app.modules.usuarios.model import UsuarioPublic

router = APIRouter(prefix="/alumnos", tags=["Alumnos"])

# Solo el administrador gestiona alumnos
solo_admin = require_role(["administrador"])


@router.get("", response_model=list[AlumnoPublic])
def listar(
    _admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    buscar: str | None = None,
):
    """Lista los alumnos; con `buscar` filtra por nombre o DNI."""
    with uow:
        return AlumnoService(uow).listar(buscar)