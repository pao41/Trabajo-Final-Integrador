from datetime import date, datetime
from zoneinfo import ZoneInfo

# Todas las fechas del negocio (vencimientos, check-in) se calculan en hora de Argentina,
# porque el servidor en la nube suele trabajar en UTC (3 horas adelantado).
ARGENTINA = ZoneInfo("America/Argentina/Buenos_Aires")


def now_ar() -> datetime:
    return datetime.now(ARGENTINA)


def today_ar() -> date:
    return now_ar().date()
