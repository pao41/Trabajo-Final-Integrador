import calendar
from decimal import Decimal

from app.core.clock import today_ar
from app.core.uow import UnitOfWork
from app.modules.dashboard.model import DashboardPublic, FacturacionPorMetodo

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
