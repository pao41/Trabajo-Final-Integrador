from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.auditoria import auditar
from app.core.deps import require_role
from app.core.uow import UnitOfWork, get_uow
from app.modules.rutinas.model import RutinaDatos, RutinaPublic
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


@router.post("", response_model=RutinaPublic, status_code=status.HTTP_201_CREATED)
def crear(
    datos: RutinaDatos,
    entrenador: Annotated[UsuarioPublic, Depends(solo_entrenador)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        return RutinaService(uow).crear(datos, entrenador.entrenador_id)


@router.put("/{rutina_id}", response_model=RutinaPublic)
def editar(
    rutina_id: int,
    datos: RutinaDatos,
    _entrenador: Annotated[UsuarioPublic, Depends(solo_entrenador)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        return RutinaService(uow).editar(rutina_id, datos)


@router.delete("/{rutina_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(
    rutina_id: int,
    entrenador: Annotated[UsuarioPublic, Depends(solo_entrenador)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with auditar(entrenador.nombre_usuario, "eliminar rutina", f"rutina {rutina_id}"), uow:
        RutinaService(uow).eliminar(rutina_id)
