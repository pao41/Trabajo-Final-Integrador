from datetime import timedelta

from app.core.clock import now_ar
from app.core.uow import UnitOfWork
from app.modules.asistencias.model import (
    Asistencia,
    AsistenciaDatos,
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
