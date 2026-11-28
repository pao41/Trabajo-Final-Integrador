from datetime import date

from sqlmodel import Field, SQLModel

from app.core.clock import today_ar


# Tabla entrenadores (definida en database/schema.sql)
class Entrenador(SQLModel, table=True):
    __tablename__ = "entrenadores"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    contacto: str | None = None
    activo: bool = True
    fecha_alta: date = Field(default_factory=today_ar)


# Datos que se piden para dar de alta o editar un entrenador
class EntrenadorDatos(SQLModel):
    nombre: str = Field(min_length=2, max_length=150)
    contacto: str | None = Field(default=None, max_length=150)


# Entrenador que se devuelve al frontend
class EntrenadorPublic(EntrenadorDatos):
    id: int
    activo: bool
    fecha_alta: date
