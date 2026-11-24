from typing import Annotated

from fastapi import APIRouter, Depends, Response

from app.core.config import settings
from app.core.deps import COOKIE_ALUMNO
from app.core.security import MINUTOS_SESION_ALUMNO
from app.core.uow import UnitOfWork, get_uow
from app.modules.panel_alumno.model import AccesoDatos
from app.modules.panel_alumno.service import PanelAlumnoService

router = APIRouter(prefix="/panel-alumno", tags=["Panel del Alumno"])


@router.post("/acceso")
def acceder(
    datos: AccesoDatos,
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    response: Response,
):
    """Valida DNI y código y deja el token del alumno en una cookie HttpOnly."""
    with uow:
        token = PanelAlumnoService(uow).acceder(datos)
    response.set_cookie(
        key=COOKIE_ALUMNO,
        value=token,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
        max_age=MINUTOS_SESION_ALUMNO * 60,
    )
    return {"mensaje": "Acceso correcto"}