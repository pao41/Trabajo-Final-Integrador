from fastapi import HTTPException, status

from app.core.uow import UnitOfWork
from app.modules.entrenadores.model import Entrenador, EntrenadorDatos, EntrenadorPublic


class EntrenadorService:
    """Reglas de negocio de los entrenadores (los da de alta y edita el administrador)."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def listar(self) -> list[EntrenadorPublic]:
        return [EntrenadorPublic.model_validate(e) for e in self.uow.entrenadores.listar()]

    def crear(self, datos: EntrenadorDatos) -> EntrenadorPublic:
        """Da de alta un entrenador; después se le puede crear su usuario."""
        entrenador = Entrenador(nombre=datos.nombre.strip(), contacto=datos.contacto)
        return EntrenadorPublic.model_validate(self.uow.entrenadores.add(entrenador))

    def editar(self, entrenador_id: int, datos: EntrenadorDatos) -> EntrenadorPublic:
        """Modifica el nombre y el contacto; el entrenador conserva sus rutinas y su usuario."""
        entrenador = self.uow.entrenadores.get_by_id(entrenador_id)
        if not entrenador:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Entrenador no encontrado")
        entrenador.nombre = datos.nombre.strip()
        entrenador.contacto = datos.contacto
        return EntrenadorPublic.model_validate(self.uow.entrenadores.update(entrenador))