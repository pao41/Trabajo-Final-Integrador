from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.deps import require_role
from app.core.uow import UnitOfWork, get_uow
from app.modules.alumnos.model import AlumnoConCodigo, AlumnoDatos, AlumnoPublic
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


@router.post("", response_model=AlumnoConCodigo, status_code=status.HTTP_201_CREATED)
def crear(
    datos: AlumnoDatos,
    _admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        return AlumnoService(uow).crear(datos)


@router.get("/{alumno_id}", response_model=AlumnoPublic)
def obtener(
    alumno_id: int,
    _admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        return AlumnoService(uow).obtener(alumno_id)


@router.put("/{alumno_id}", response_model=AlumnoPublic)
def editar(
    alumno_id: int,
    datos: AlumnoDatos,
    _admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        return AlumnoService(uow).editar(alumno_id, datos)


@router.patch("/{alumno_id}/desactivar", response_model=AlumnoPublic)
def desactivar(
    alumno_id: int,
    _admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        return AlumnoService(uow).cambiar_estado(alumno_id, False)