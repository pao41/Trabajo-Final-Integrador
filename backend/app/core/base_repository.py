from typing import Generic, TypeVar

from sqlmodel import Session, SQLModel, select

T = TypeVar("T", bound=SQLModel)


class BaseRepository(Generic[T]):
    """Consultas comunes a todos los módulos: buscar, listar, agregar, actualizar y borrar."""

    def __init__(self, model: type[T], session: Session):
        self.model = model
        self.session = session

    def get_by_id(self, entity_id: int) -> T | None:
        return self.session.get(self.model, entity_id)

    def get_all(self, offset: int = 0, limit: int = 100) -> list[T]:
        # Se ordena por id para que las páginas no repitan ni salteen filas
        consulta = select(self.model).order_by(self.model.id).offset(offset).limit(limit)
        return list(self.session.exec(consulta).all())

    def add(self, entity: T) -> T:
        self.session.add(entity)
        # flush envía el INSERT pero no confirma: el commit lo hace solo el Unit of Work
        self.session.flush()
        self.session.refresh(entity)
        return entity

    def update(self, entity: T) -> T:
        self.session.add(entity)
        self.session.flush()
        self.session.refresh(entity)
        return entity

    def delete(self, entity: T) -> None:
        self.session.delete(entity)
        self.session.flush()