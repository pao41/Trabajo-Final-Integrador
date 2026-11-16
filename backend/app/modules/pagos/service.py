from datetime import date, timedelta

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