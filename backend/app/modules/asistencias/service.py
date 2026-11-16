from datetime import date, timedelta

from fastapi import HTTPException, status

from app.core.clock import now_ar
from app.core.uow import UnitOfWork
from app.modules.alumnos.model import Alumno
from app.modules.asistencias.model import (
    Asistencia,
    AsistenciaDatos,
    AsistenciaPublic,
    AsistenciaRegistrada,
)
from app.modules.planes.inscripcion_service import InscripcionService

# Tiempo que debe pasar entre dos ingresos del mismo alumno 
VENTANA = timedelta(hours=2)


class AsistenciaService:
    """Registro de ingresos al gimnasio (check-in manual desde el mostrador)."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def registrar(self, datos: AsistenciaDatos) -> AsistenciaRegistrada:
        """Guarda el ingreso y, si el plan es por clases, descuenta una clase (RN30)."""
        alumno = self._alumno_activo(datos.alumno_id)
        ahora = now_ar().replace(tzinfo=None, microsecond=0)
        self._controlar_ventana(alumno, ahora)
        inscripcion = self._inscripcion_para_ingresar(alumno)
        asistencia = Asistencia(
            alumno_id=alumno.id,
            inscripcion_id=inscripcion.id,
            fecha=ahora.date(),
            hora=ahora.time(),
        )
        self.uow.asistencias.add(asistencia)
        if inscripcion.clases_restantes is not None:
            inscripcion.clases_restantes -= 1
            self.uow.inscripciones.update(inscripcion)
        return AsistenciaRegistrada(
            asistencia=self._armar(asistencia),
            inscripcion=InscripcionService(self.uow).armar(inscripcion),
        )

    def listar(
        self, alumno_id: int | None = None, fecha: date | None = None
    ) -> list[AsistenciaPublic]:
        return [self._armar(a) for a in self.uow.asistencias.listar(alumno_id, fecha)]

    def _armar(self, asistencia: Asistencia) -> AsistenciaPublic:
        """Arma la respuesta con el nombre del alumno y el del plan."""
        alumno = self.uow.alumnos.get_by_id(asistencia.alumno_id)
        inscripcion = self.uow.inscripciones.get_by_id(asistencia.inscripcion_id)
        plan = self.uow.planes.get_by_id(inscripcion.plan_id) if inscripcion else None
        return AsistenciaPublic(
            **asistencia.model_dump(),
            alumno_nombre=alumno.nombre,
            plan_nombre=plan.nombre if plan else None,
        )

    def _alumno_activo(self, alumno_id: int) -> Alumno:
        alumno = self.uow.alumnos.get_by_id(alumno_id)
        if not alumno:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Alumno no encontrado")
        if not alumno.activo:
            raise HTTPException(status.HTTP_409_CONFLICT, "El alumno está dado de baja")
        return alumno
