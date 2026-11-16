from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.auditoria import auditar
from app.core.deps import require_role
from app.core.uow import UnitOfWork, get_uow
from app.modules.planes.model import PlanDatos, PlanPublic
from app.modules.planes.service import PlanService
from app.modules.usuarios.model import UsuarioPublic

router = APIRouter(prefix="/planes", tags=["Planes"])

# Solo el administrador gestiona planes y precios (RN36)
solo_admin = require_role(["administrador"])


@router.get("", response_model=list[PlanPublic])
def listar(
    _admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        return PlanService(uow).listar()


@router.post("", response_model=PlanPublic, status_code=status.HTTP_201_CREATED)
def crear(
    datos: PlanDatos,
    admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with auditar(admin.nombre_usuario, "crear plan", f"plan {datos.nombre}"), uow:
        return PlanService(uow).crear(datos)


@router.put("/{plan_id}", response_model=PlanPublic)
def editar(
    plan_id: int,
    datos: PlanDatos,
    admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with auditar(admin.nombre_usuario, "editar plan", f"plan {plan_id}"), uow:
        return PlanService(uow).editar(plan_id, datos)
