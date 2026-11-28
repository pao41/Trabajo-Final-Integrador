from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.auditoria import auditar
from app.core.deps import require_role
from app.core.uow import UnitOfWork, get_uow
from app.modules.entrenadores.model import EntrenadorDatos, EntrenadorPublic
from app.modules.entrenadores.service import EntrenadorService
from app.modules.usuarios.model import UsuarioPublic

router = APIRouter(prefix="/entrenadores", tags=["Entrenadores"])

# Solo el administrador gestiona entrenadores
solo_admin = require_role(["administrador"])


@router.get("", response_model=list[EntrenadorPublic])
def listar(
    _admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        return EntrenadorService(uow).listar()


@router.post("", response_model=EntrenadorPublic, status_code=status.HTTP_201_CREATED)
def crear(
    datos: EntrenadorDatos,
    admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with auditar(admin.nombre_usuario, "crear entrenador", f"entrenador {datos.nombre}"), uow:
        return EntrenadorService(uow).crear(datos)


@router.put("/{entrenador_id}", response_model=EntrenadorPublic)
def editar(
    entrenador_id: int,
    datos: EntrenadorDatos,
    admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with auditar(admin.nombre_usuario, "editar entrenador", f"entrenador {entrenador_id}"), uow:
        return EntrenadorService(uow).editar(entrenador_id, datos)


@router.patch("/{entrenador_id}/desactivar", response_model=EntrenadorPublic)
def desactivar(
    entrenador_id: int,
    admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with auditar(admin.nombre_usuario, "baja de entrenador", f"entrenador {entrenador_id}"), uow:
        return EntrenadorService(uow).cambiar_estado(entrenador_id, False)


@router.patch("/{entrenador_id}/activar", response_model=EntrenadorPublic)
def activar(
    entrenador_id: int,
    admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with auditar(admin.nombre_usuario, "reactivar entrenador", f"entrenador {entrenador_id}"), uow:
        return EntrenadorService(uow).cambiar_estado(entrenador_id, True)
