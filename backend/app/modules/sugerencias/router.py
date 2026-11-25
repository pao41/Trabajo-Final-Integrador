from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.auditoria import auditar
from app.core.deps import get_alumno_actual, require_role
from app.core.uow import UnitOfWork, get_uow
from app.modules.alumnos.model import AlumnoPublic
from app.modules.sugerencias.model import EstadoSugerencia, SugerenciaPublic
from app.modules.sugerencias.service import AsistenteService
from app.modules.usuarios.model import UsuarioPublic

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


@router.get("", response_model=list[SugerenciaPublic])
def listar(
    _usuario: Annotated[UsuarioPublic, Depends(lectura)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    estado: EstadoSugerencia | None = None,
):
    with uow:
        return AsistenteService(uow).listar(estado)


@router.patch("/{sugerencia_id}/aprobar", response_model=SugerenciaPublic)
def aprobar(
    sugerencia_id: int,
    entrenador: Annotated[UsuarioPublic, Depends(solo_entrenador)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    detalle = f"sugerencia {sugerencia_id}"
    with auditar(entrenador.nombre_usuario, "aprobar sugerencia", detalle), uow:
        return AsistenteService(uow).resolver(sugerencia_id, entrenador.entrenador_id, "aprobada")


@router.patch("/{sugerencia_id}/rechazar", response_model=SugerenciaPublic)
def rechazar(
    sugerencia_id: int,
    entrenador: Annotated[UsuarioPublic, Depends(solo_entrenador)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    detalle = f"sugerencia {sugerencia_id}"
    with auditar(entrenador.nombre_usuario, "rechazar sugerencia", detalle), uow:
        return AsistenteService(uow).resolver(sugerencia_id, entrenador.entrenador_id, "rechazada")
