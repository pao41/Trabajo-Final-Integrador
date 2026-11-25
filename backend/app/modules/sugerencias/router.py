from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.deps import get_alumno_actual, require_role
from app.core.uow import UnitOfWork, get_uow
from app.modules.alumnos.model import AlumnoPublic
from app.modules.sugerencias.service import AsistenteService

router = APIRouter(prefix="/sugerencias", tags=["Asistente de IA"])

# El administrador solo consulta; aprobar y rechazar es exclusivo del entrenador
lectura = require_role(["administrador", "entrenador"])
solo_entrenador = require_role(["entrenador"])


@router.post("", status_code=status.HTTP_201_CREATED)
def solicitar(
    alumno: Annotated[AlumnoPublic, Depends(get_alumno_actual)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    """El alumno pide una sugerencia; queda pendiente hasta que la apruebe un entrenador."""
    with uow:
        AsistenteService(uow).solicitar(alumno.id)
    return {"mensaje": "Tu sugerencia quedó pendiente de aprobación del entrenador"}