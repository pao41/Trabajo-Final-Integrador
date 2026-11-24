from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.deps import require_role
from app.core.uow import UnitOfWork, get_uow
from app.modules.rutinas.model import RutinaPublic
from app.modules.rutinas.service import RutinaService
from app.modules.usuarios.model import UsuarioPublic

router = APIRouter(prefix="/rutinas", tags=["Rutinas"])

# El administrador solo consulta; cargar y editar es exclusivo del entrenador
lectura = require_role(["administrador", "entrenador"])
solo_entrenador = require_role(["entrenador"])


@router.get("", response_model=list[RutinaPublic])
def listar(
    _usuario: Annotated[UsuarioPublic, Depends(lectura)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        return RutinaService(uow).listar()
