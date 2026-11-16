from datetime import date
from decimal import Decimal

from sqlmodel import Session, func, select

from app.modules.alumnos.model import Alumno
from app.modules.asistencias.model import Asistencia
from app.modules.pagos.model import Pago
from app.modules.planes.model import Inscripcion, Plan


class DashboardRepository:
    """Consultas de suma y conteo para los indicadores del dashboard."""

    def __init__(self, session: Session):
        self.session = session

    def facturacion_por_metodo(self, desde: date, hasta: date) -> dict[str, Decimal]:
        """Total cobrado en el período, agrupado por método de pago."""
        consulta = (
            select(Pago.metodo_pago, func.sum(Pago.monto))
            .where(Pago.fecha_pago >= desde, Pago.fecha_pago <= hasta)
            .group_by(Pago.metodo_pago)
        )
        return {metodo: total for metodo, total in self.session.exec(consulta).all()}

    def contar_alumnos_nuevos(self, desde: date, hasta: date) -> int:
        consulta = select(func.count()).select_from(Alumno)
        consulta = consulta.where(Alumno.fecha_alta >= desde, Alumno.fecha_alta <= hasta)
        return self.session.exec(consulta).one()

    def ingresos_por_dia(self, desde: date, hasta: date) -> dict[date, int]:
        """Cantidad de ingresos de cada día del período."""
        consulta = (
            select(Asistencia.fecha, func.count())
            .where(Asistencia.fecha >= desde, Asistencia.fecha <= hasta)
            .group_by(Asistencia.fecha)
        )
        return {dia: cantidad for dia, cantidad in self.session.exec(consulta).all()}

    def ultimas_inscripciones(self) -> list[tuple[Inscripcion, Plan]]:
        """La inscripción más reciente de cada alumno activo, con su plan."""
        consulta = (
            select(Inscripcion, Plan)
            .join(Plan, Plan.id == Inscripcion.plan_id)
            .join(Alumno, Alumno.id == Inscripcion.alumno_id)
            .where(Alumno.activo)
            .order_by(Inscripcion.alumno_id, Inscripcion.fecha_inicio.desc(), Inscripcion.id.desc())
        )
        ultimas = {}
        for inscripcion, plan in self.session.exec(consulta).all():
            # Como vienen ordenadas, la primera de cada alumno es la más reciente
            ultimas.setdefault(inscripcion.alumno_id, (inscripcion, plan))
        return list(ultimas.values())
