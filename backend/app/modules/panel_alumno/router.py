from typing import Annotated

from fastapi import APIRouter, Depends, Response

from app.core.config import settings
from app.core.deps import COOKIE_ALUMNO, get_alumno_actual
from app.core.security import MINUTOS_SESION_ALUMNO
from app.core.uow import UnitOfWork, get_uow
from app.modules.alumnos.model import AlumnoPublic
from app.modules.panel_alumno.model import AccesoDatos, IngresoPropio, ResumenAlumno
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


@router.post("/salir")
def salir(response: Response):
    """Borra la cookie de sesión del alumno."""
    response.delete_cookie(
        key=COOKIE_ALUMNO,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
    )
    return {"mensaje": "Sesión cerrada"}


@router.get("/resumen", response_model=ResumenAlumno)
def resumen(
    alumno: Annotated[AlumnoPublic, Depends(get_alumno_actual)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        return PanelAlumnoService(uow).resumen(alumno)


@router.get("/asistencias", response_model=list[IngresoPropio])
def asistencias(
    alumno: Annotated[AlumnoPublic, Depends(get_alumno_actual)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    with uow:
        return PanelAlumnoService(uow).historial(alumno)