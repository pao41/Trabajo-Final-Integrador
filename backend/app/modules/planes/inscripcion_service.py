from datetime import date, timedelta

from fastapi import HTTPException, status

from app.core.clock import today_ar
from app.core.uow import UnitOfWork
from app.modules.alumnos.model import Alumno
from app.modules.configuracion.service import ConfiguracionService
from app.modules.planes.model import Inscripcion, InscripcionDatos, InscripcionPublic, Plan


def calcular_estado(inscripcion: Inscripcion, hoy: date, dias_aviso: int) -> str:
    """Estado según la fecha de hoy (RN01, RN09) y, en planes por clases, el saldo (RN31)."""
    if hoy >= inscripcion.fecha_vencimiento or inscripcion.clases_restantes == 0:
        return "vencido"
    if (inscripcion.fecha_vencimiento - hoy).days < dias_aviso:
        return "por_vencer"
    return "activo"


class InscripcionService:
    """Inscripción de alumnos a los planes y control de su estado."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def inscribir(self, datos: InscripcionDatos) -> InscripcionPublic:
        """Inscribe al alumno: calcula el vencimiento y, si el plan es por clases, su saldo."""
        alumno, plan = self._validar(datos)
        inicio = datos.fecha_inicio or today_ar()
        inscripcion = Inscripcion(
            alumno_id=alumno.id,
            plan_id=plan.id,
            fecha_inicio=inicio,
            fecha_vencimiento=inicio + timedelta(days=plan.duracion_dias),
            clases_restantes=plan.cantidad_clases if plan.tipo == "clases" else None,
        )
        self.uow.inscripciones.add(inscripcion)
        return self.armar(inscripcion)

    def listar(self, alumno_id: int | None = None) -> list[InscripcionPublic]:
        return [self.armar(i) for i in self.uow.inscripciones.listar(alumno_id)]

    def armar(self, inscripcion: Inscripcion) -> InscripcionPublic:
        """Actualiza el estado guardado (RF05) y arma la respuesta con los datos del plan."""
        dias_aviso = ConfiguracionService(self.uow).obtener().dias_aviso_vencimiento
        estado = calcular_estado(inscripcion, today_ar(), dias_aviso)
        if estado != inscripcion.estado:
            inscripcion.estado = estado
            self.uow.inscripciones.update(inscripcion)
        plan = self.uow.planes.get_by_id(inscripcion.plan_id)
        return InscripcionPublic(
            **inscripcion.model_dump(), plan_nombre=plan.nombre, tipo=plan.tipo
        )

    def _validar(self, datos: InscripcionDatos) -> tuple[Alumno, Plan]:
        """Comprueba que el alumno y el plan existan y que el alumno pueda inscribirse."""
        alumno = self.uow.alumnos.get_by_id(datos.alumno_id)
        if not alumno:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Alumno no encontrado")
        plan = self.uow.planes.get_by_id(datos.plan_id)
        if not plan:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Plan no encontrado")
        if not alumno.activo:
            raise HTTPException(status.HTTP_409_CONFLICT, "El alumno está dado de baja")
        # Mientras la inscripción vigente no venza, el plan nuevo espera a la renovación (RN06)
        vigente = self.uow.inscripciones.get_vigente(alumno.id, today_ar())
        if vigente:
            actual = self.uow.planes.get_by_id(vigente.plan_id)
            hasta = vigente.fecha_vencimiento.strftime("%d/%m/%Y")
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                f"El alumno ya tiene una inscripción vigente: {actual.nombre}, hasta el {hasta}",
            )
        return alumno, plan
