from datetime import date
from decimal import Decimal

from sqlmodel import SQLModel


# Total cobrado con un método de pago
class FacturacionPorMetodo(SQLModel):
    metodo_pago: str
    total: Decimal


# Cantidad de ingresos de una semana (la semana empieza el lunes)
class AsistenciaSemanal(SQLModel):
    semana_desde: date
    total: int


# Indicadores que se muestran en el dashboard
class DashboardPublic(SQLModel):
    mes_desde: date
    mes_hasta: date
    facturacion_total: Decimal
    facturacion_por_metodo: list[FacturacionPorMetodo]
    alumnos_activos: int
    alumnos_por_vencer: int
    alumnos_vencidos: int
    alumnos_nuevos_mes: int
    asistencias_por_semana: list[AsistenciaSemanal]
    cuotas_vencidas: int
    monto_cuotas_vencidas: Decimal
    ingresos_proyectados: Decimal
