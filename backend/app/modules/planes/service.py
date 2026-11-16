from app.core.uow import UnitOfWork
from app.modules.planes.model import Plan, PlanDatos, PlanPublic


class PlanService:
    """Reglas de negocio del catálogo de planes."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def listar(self) -> list[PlanPublic]:
        return [PlanPublic.model_validate(p) for p in self.uow.planes.listar()]

    def crear(self, datos: PlanDatos) -> PlanPublic:
        """Crea un plan; el nombre no se repite."""
        self._validar_nombre(datos.nombre)
        plan = Plan(**datos.model_dump())
        return PlanPublic.model_validate(self.uow.planes.add(plan))
