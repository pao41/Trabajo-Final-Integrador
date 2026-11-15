from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.deps import require_role
from app.core.uow import UnitOfWork, get_uow
from app.modules.alumnos.ficha_service import FichaMetaService
from app.modules.alumnos.model import FichaSaludPublic
from app.modules.usuarios.model import UsuarioPublic

router = APIRouter(prefix="/alumnos", tags=["Ficha de salud y meta"])

# La ficha de salud también la puede consultar (no modificar) el entrenador
admin_o_entrenador = require_role(["administrador", "entrenador"])


@router.get("/{alumno_id}/ficha-salud", response_model=FichaSaludPublic)
def obtener_ficha(
    alumno_id: int,
    _usuario: Annotated[UsuarioPublic, Depends(admin_o_entrenador)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        return FichaMetaService(uow).obtener_ficha(alumno_id)