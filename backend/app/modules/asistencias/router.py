from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.uow import UnitOfWork, get_uow
from app.modules.asistencias.model import AsistenciaDatos, AsistenciaPublic, AsistenciaRegistrada
from app.modules.asistencias.service import AsistenciaService
from app.modules.planes.router import solo_admin
from app.modules.usuarios.model import UsuarioPublic

router = APIRouter(prefix="/asistencias", tags=["Asistencia"])


@router.get("", response_model=list[AsistenciaPublic])
def listar(
    _admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    alumno_id: int | None = None,
    fecha: date | None = None,
):
    """Ingresos registrados; con `alumno_id` los de un alumno y con `fecha` los de ese día."""
    with uow:
        return AsistenciaService(uow).listar(alumno_id, fecha)


@router.post("", response_model=AsistenciaRegistrada, status_code=status.HTTP_201_CREATED)
def registrar(
    datos: AsistenciaDatos,
    _admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        return AsistenciaService(uow).registrar(datos)