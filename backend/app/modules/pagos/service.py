from datetime import date, timedelta

from app.core.clock import today_ar
from app.core.uow import UnitOfWork
from app.modules.pagos.model import Pago, PagoDatos, PagoPublic, PagoRegistrado
from app.modules.planes.inscripcion_service import InscripcionService
from app.modules.planes.model import Inscripcion, Plan


def renovar(inscripcion: Inscripcion, plan: Plan, fecha_pago: date, primer_pago: bool) -> None:
    """Aplica el pago a la inscripción según RN02, RN03, RN04 y RN32."""
    duracion = timedelta(days=plan.duracion_dias)
    clases = plan.cantidad_clases or 0
    vigente = fecha_pago < inscripcion.fecha_vencimiento
    if primer_pago:
        # El primer pago confirma la inscripción: vence a la duración del plan desde el pago 
        inscripcion.fecha_vencimiento = fecha_pago + duracion
        if not vigente and plan.tipo == "clases":
            inscripcion.clases_restantes = clases
    elif vigente:
        # Paga antes de vencer: se suma el período y las clases que sobraban 
        inscripcion.fecha_vencimiento += duracion
        if plan.tipo == "clases":
            inscripcion.clases_restantes += clases
    else:
        # Paga vencida: arranca desde la fecha del pago y el saldo se reinicia 
        inscripcion.fecha_vencimiento = fecha_pago + duracion
        if plan.tipo == "clases":
            inscripcion.clases_restantes = clases


class PagoService:
    """Registro de pagos y renovación de la inscripción."""


    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def registrar(self, datos: PagoDatos) -> PagoRegistrado:
        """Guarda el pago y renueva la inscripción en la misma operación (RF06)."""
        inscripcion = self._validar(datos)
        plan = self.uow.planes.get_by_id(inscripcion.plan_id)
        fecha = datos.fecha_pago or today_ar()
        ultimo = self.uow.pagos.ultimo_de_inscripcion(inscripcion.id)
        self._validar_fecha(inscripcion, ultimo, fecha)
        # El monto es siempre el precio completo del plan (RN05)
        pago = Pago(
            inscripcion_id=inscripcion.id,
            fecha_pago=fecha,
            monto=plan.precio,
            metodo_pago=datos.metodo_pago,
        )
        self.uow.pagos.add(pago)
        renovar(inscripcion, plan, fecha, primer_pago=ultimo is None)
        self.uow.inscripciones.update(inscripcion)
        return PagoRegistrado(
            pago=self._armar(pago, inscripcion, plan),
            inscripcion=InscripcionService(self.uow).armar(inscripcion),
        )

    def listar(self, alumno_id: int | None = None) -> list[PagoPublic]:
        historial = []
        for pago in self.uow.pagos.listar(alumno_id):
            inscripcion = self.uow.inscripciones.get_by_id(pago.inscripcion_id)
            plan = self.uow.planes.get_by_id(inscripcion.plan_id)
            historial.append(self._armar(pago, inscripcion, plan))
        return historial

    def _armar(self, pago: Pago, inscripcion: Inscripcion, plan: Plan) -> PagoPublic:
        return PagoPublic(
            **pago.model_dump(), alumno_id=inscripcion.alumno_id, plan_nombre=plan.nombre
        )
