from datetime import timedelta

from app.core.clock import now_ar
from app.core.uow import UnitOfWork
from app.modules.asistencias.model import Asistencia
from tests.test_inscripciones import TIEMPO, inscribir, nuevo_alumno, nuevo_plan


def alumno_inscripto(admin, plan=TIEMPO, dias_atras=0):
    """Crea alumno, plan e inscripción y devuelve (alumno_id, inscripcion_id)."""
    alumno_id, plan_id = nuevo_alumno(admin), nuevo_plan(admin, plan)
    return alumno_id, inscribir(admin, alumno_id, plan_id, dias_atras).json()["id"]


def ingresar(admin, alumno_id):
    return admin.post("/asistencias", json={"alumno_id": alumno_id})


def ingreso_hace(alumno_id, inscripcion_id, horas):
    """Deja guardado un ingreso anterior, de hace tantas horas."""
    antes = now_ar().replace(tzinfo=None) - timedelta(hours=horas)
    with UnitOfWork() as uow:
        uow.asistencias.add(
            Asistencia(
                alumno_id=alumno_id,
                inscripcion_id=inscripcion_id,
                fecha=antes.date(),
                hora=antes.time(),
            )
        )