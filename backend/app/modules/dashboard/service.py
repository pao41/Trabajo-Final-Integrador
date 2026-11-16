import calendar
from datetime import date, timedelta
from decimal import Decimal

from app.core.clock import today_ar
from app.core.uow import UnitOfWork
from app.modules.configuracion.service import ConfiguracionService
from app.modules.dashboard.model import AsistenciaSemanal, DashboardPublic, FacturacionPorMetodo
from app.modules.planes.inscripcion_service import calcular_estado

SEMANAS = 4
METODOS_PAGO = ["efectivo", "transferencia", "debito", "credito"]


class DashboardService:
    """Calcula los indicadores del dashboard con la fecha de hoy."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def obtener(self) -> DashboardPublic:
        hoy = today_ar()
        mes_desde = hoy.replace(day=1)
        mes_hasta = hoy.replace(day=calendar.monthrange(hoy.year, hoy.month)[1])
        facturado = self.uow.dashboard.facturacion_por_metodo(mes_desde, mes_hasta)
        total = sum(facturado.values(), Decimal(0))
        estados = self._estados_de_cuotas(hoy, mes_hasta)
        return DashboardPublic(
            mes_desde=mes_desde,
            mes_hasta=mes_hasta,
            facturacion_total=total,
            facturacion_por_metodo=[
                FacturacionPorMetodo(metodo_pago=m, total=facturado.get(m, Decimal(0)))
                for m in METODOS_PAGO
            ],
            alumnos_activos=estados["activo"],
            alumnos_por_vencer=estados["por_vencer"],
            alumnos_vencidos=estados["vencido"],
            alumnos_nuevos_mes=self.uow.dashboard.contar_alumnos_nuevos(mes_desde, mes_hasta),
            asistencias_por_semana=self._asistencias_por_semana(hoy),
            cuotas_vencidas=estados["vencido"],
            monto_cuotas_vencidas=estados["monto_vencido"],
            ingresos_proyectados=total + estados["a_renovar"],
        )

    def _estados_de_cuotas(self, hoy: date, fin_de_mes: date) -> dict:
        """Cuenta los alumnos por estado de su cuota y suma lo que falta cobrar."""
        dias_aviso = ConfiguracionService(self.uow).obtener().dias_aviso_vencimiento
        datos = {"activo": 0, "por_vencer": 0, "vencido": 0}
        datos["monto_vencido"] = Decimal(0)
        # Lo que se espera cobrar de las cuotas que vencen de acá a fin de mes
        datos["a_renovar"] = Decimal(0)
        for inscripcion, plan in self.uow.dashboard.ultimas_inscripciones():
            estado = calcular_estado(inscripcion, hoy, dias_aviso)
            datos[estado] += 1
            if estado == "vencido":
                datos["monto_vencido"] += plan.precio
            elif inscripcion.fecha_vencimiento <= fin_de_mes:
                datos["a_renovar"] += plan.precio
        return datos

    def _asistencias_por_semana(self, hoy: date) -> list[AsistenciaSemanal]:
        """Ingresos de las últimas semanas (de lunes a domingo), la más vieja primero."""
        lunes_actual = hoy - timedelta(days=hoy.weekday())
        primer_lunes = lunes_actual - timedelta(weeks=SEMANAS - 1)
        por_dia = self.uow.dashboard.ingresos_por_dia(primer_lunes, hoy)
        semanas = []
        for n in range(SEMANAS):
            lunes = primer_lunes + timedelta(weeks=n)
            total = sum(por_dia.get(lunes + timedelta(days=d), 0) for d in range(7))
            semanas.append(AsistenciaSemanal(semana_desde=lunes, total=total))
        return semanas
