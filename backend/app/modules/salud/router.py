from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.clock import now_ar
from app.core.database import get_session
from app.modules.salud.schemas import EstadoSalud

router = APIRouter(prefix="/salud", tags=["Salud"])


@router.get("", response_model=EstadoSalud)
def estado_del_sistema(session: Session = Depends(get_session)):
    """Comprueba que la API responde y que llega a la base de datos."""
    try:
        session.exec(select(1)).one()
    except Exception:
        raise HTTPException(status_code=503, detail="No hay conexión con la base de datos")
    return EstadoSalud(estado="ok", base_de_datos="ok", hora_argentina=now_ar())
