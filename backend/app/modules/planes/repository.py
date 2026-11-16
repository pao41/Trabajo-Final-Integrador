from datetime import date

from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.modules.planes.model import Inscripcion, Plan


class PlanRepository(BaseRepository[Plan]):
    def __init__(self, session: Session):
        super().__init__(Plan, session)

    def get_by_nombre(self, nombre: str) -> Plan | None:
        consulta = select(Plan).where(Plan.nombre == nombre)
        return self.session.exec(consulta).first()

    def listar(self) -> list[Plan]:
        return list(self.session.exec(select(Plan).order_by(Plan.nombre)).all())


class InscripcionRepository(BaseRepository[Inscripcion]):
    def __init__(self, session: Session):
        super().__init__(Inscripcion, session)

    def listar(self, alumno_id: int | None = None) -> list[Inscripcion]:
        """Las más nuevas primero; con alumno_id, solo las de ese alumno."""
        consulta = select(Inscripcion).order_by(
            Inscripcion.fecha_inicio.desc(), Inscripcion.id.desc()
        )
        if alumno_id is not None:
            consulta = consulta.where(Inscripcion.alumno_id == alumno_id)
        return list(self.session.exec(consulta.limit(200)).all())

    def get_vigente(self, alumno_id: int, hoy: date) -> Inscripcion | None:
        """Inscripción del alumno que todavía no venció (por fecha ni por saldo de clases)."""
        consulta = select(Inscripcion).where(
            Inscripcion.alumno_id == alumno_id,
            Inscripcion.fecha_vencimiento > hoy,
            (Inscripcion.clases_restantes.is_(None)) | (Inscripcion.clases_restantes > 0),
        )
        return self.session.exec(consulta).first()

    def existe_de_plan(self, plan_id: int) -> bool:
        consulta = select(Inscripcion.id).where(Inscripcion.plan_id == plan_id)
        return self.session.exec(consulta.limit(1)).first() is not None
