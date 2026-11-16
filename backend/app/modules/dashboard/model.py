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