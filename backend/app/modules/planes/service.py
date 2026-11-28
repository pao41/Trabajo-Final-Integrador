from fastapi import HTTPException, status

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

    def editar(self, plan_id: int, datos: PlanDatos) -> PlanPublic:
        """Modifica un plan. Las inscripciones ya creadas conservan sus fechas y su saldo."""
        plan = self.uow.planes.get_by_id(plan_id)
        if not plan:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Plan no encontrado")
        if datos.nombre != plan.nombre:
            self._validar_nombre(datos.nombre)
        # Con inscripciones hechas no se cambia el tipo: sus saldos dejarían de tener sentido
        if datos.tipo != plan.tipo and self.uow.inscripciones.existe_de_plan(plan_id):
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                "No se puede cambiar el tipo de un plan que ya tiene inscripciones",
            )
        for campo, valor in datos.model_dump().items():
            setattr(plan, campo, valor)
        return PlanPublic.model_validate(self.uow.planes.update(plan))

    def eliminar(self, plan_id: int) -> None:
        """Elimina un plan que nunca se usó; con inscripciones no se borra (RN28, RN47)."""
        plan = self.uow.planes.get_by_id(plan_id)
        if not plan:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Plan no encontrado")
        if self.uow.inscripciones.existe_de_plan(plan_id):
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                "No se puede eliminar un plan que ya tiene inscripciones",
            )
        self.uow.planes.delete(plan)

    def _validar_nombre(self, nombre: str) -> None:
        if self.uow.planes.get_by_nombre(nombre):
            raise HTTPException(status.HTTP_409_CONFLICT, "Ya existe un plan con ese nombre")
