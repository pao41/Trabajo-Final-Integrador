from sqlmodel import Session, or_, select

from app.core.base_repository import BaseRepository
from app.modules.alumnos.model import Alumno, FichaSalud


class AlumnoRepository(BaseRepository[Alumno]):
    def __init__(self, session: Session):
        super().__init__(Alumno, session)

    def get_by_dni(self, dni: str) -> Alumno | None:
        consulta = select(Alumno).where(Alumno.dni == dni)
        return self.session.exec(consulta).first()

    def buscar(self, texto: str | None) -> list[Alumno]:
        """Lista los alumnos por nombre; si hay texto, filtra por nombre o DNI."""
        consulta = select(Alumno).order_by(Alumno.nombre)
        if texto:
            patron = f"%{texto}%"
            consulta = consulta.where(or_(Alumno.nombre.ilike(patron), Alumno.dni.like(patron)))
        return list(self.session.exec(consulta.limit(200)).all())


class FichaSaludRepository(BaseRepository[FichaSalud]):
    def __init__(self, session: Session):
        super().__init__(FichaSalud, session)

    def get_by_alumno(self, alumno_id: int) -> FichaSalud | None:
        consulta = select(FichaSalud).where(FichaSalud.alumno_id == alumno_id)
        return self.session.exec(consulta).first()