from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.modules.pagos.model import Pago
from app.modules.planes.model import Inscripcion


class PagoRepository(BaseRepository[Pago]):
    def __init__(self, session: Session):
        super().__init__(Pago, session)

    def ultimo_de_inscripcion(self, inscripcion_id: int) -> Pago | None:
        consulta = select(Pago).where(Pago.inscripcion_id == inscripcion_id)
        return self.session.exec(consulta.order_by(Pago.fecha_pago.desc(), Pago.id.desc())).first()

    def listar(self, alumno_id: int | None = None) -> list[Pago]:
        """Los más nuevos primero; con alumno_id, solo los de ese alumno (RF14)."""
        consulta = select(Pago).order_by(Pago.fecha_pago.desc(), Pago.id.desc())
        if alumno_id is not None:
            consulta = consulta.join(Inscripcion, Inscripcion.id == Pago.inscripcion_id)
            consulta = consulta.where(Inscripcion.alumno_id == alumno_id)
        return list(self.session.exec(consulta.limit(200)).all())
