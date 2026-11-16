from datetime import date, timedelta

from fastapi import HTTPException, status

from app.core.clock import today_ar
from app.core.uow import UnitOfWork
from app.modules.configuracion.service import ConfiguracionService
from app.modules.pagos.model import Pago, PagoDatos, PagoPublic, PagoRegistrado
from app.modules.planes.inscripcion_service import InscripcionService
from app.modules.planes.model import Inscripcion, Plan


def renovar(inscripcion: Inscripcion, plan: Plan, fecha_pago: date, primer_pago: bool) -> None:
    """Aplica el pago a la inscripción"""
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
        """Guarda el pago y renueva la inscripción en la misma operación."""
        inscripcion = self._validar(datos)
        plan = self.uow.planes.get_by_id(inscripcion.plan_id)
        fecha = datos.fecha_pago or today_ar()
        ultimo = self.uow.pagos.ultimo_de_inscripcion(inscripcion.id)
        self._validar_fecha(inscripcion, ultimo, fecha)
        # El monto es siempre el precio completo del plan
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

    def _validar(self, datos: PagoDatos) -> Inscripcion:
        """Comprueba que se pueda pagar esa inscripción con ese método."""
        inscripcion = self.uow.inscripciones.get_by_id(datos.inscripcion_id)
        if not inscripcion:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Inscripción no encontrada")
        if not self.uow.alumnos.get_by_id(inscripcion.alumno_id).activo:
            raise HTTPException(status.HTTP_409_CONFLICT, "El alumno está dado de baja")
        # Pagar renueva la última inscripción; para otro plan se inscribe de nuevo
        ultima = self.uow.inscripciones.listar(inscripcion.alumno_id)[0]
        if ultima.id != inscripcion.id:
            raise HTTPException(
                status.HTTP_409_CONFLICT, "Solo se puede pagar la inscripción más reciente"
            )
        habilitados = ConfiguracionService(self.uow).obtener().metodos_pago_habilitados
        if datos.metodo_pago not in habilitados:
            raise HTTPException(
                status.HTTP_409_CONFLICT, f"El método {datos.metodo_pago} no está habilitado"
            )
        return inscripcion

    def _validar_fecha(self, inscripcion: Inscripcion, ultimo: Pago | None, fecha: date) -> None:
        """La fecha no puede ser futura ni anterior al último pago o al inicio."""
        if fecha > today_ar():
            raise HTTPException(status.HTTP_409_CONFLICT, "La fecha del pago no puede ser futura")
        piso = ultimo.fecha_pago if ultimo else inscripcion.fecha_inicio
        if fecha < piso:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                f"La fecha del pago no puede ser anterior al {piso:%d/%m/%Y}",
            )
