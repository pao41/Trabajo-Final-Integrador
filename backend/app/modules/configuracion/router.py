from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.auditoria import auditar
from app.core.deps import require_role
from app.core.uow import UnitOfWork, get_uow
from app.modules.configuracion.model import ConfiguracionDatos
from app.modules.configuracion.service import ConfiguracionService
from app.modules.usuarios.model import UsuarioPublic

router = APIRouter(prefix="/configuracion", tags=["Configuración"])

# Solo el administrador cambia la configuración
solo_admin = require_role(["administrador"])


@router.get("", response_model=ConfiguracionDatos)
def obtener(
    _admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        return ConfiguracionService(uow).obtener()


@router.put("", response_model=ConfiguracionDatos)
def guardar(
    datos: ConfiguracionDatos,
    admin: Annotated[UsuarioPublic, Depends(solo_admin)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with auditar(admin.nombre_usuario, "cambiar configuración", "configuración"), uow:
        return ConfiguracionService(uow).guardar(datos)
