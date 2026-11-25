from typing import Literal

from sqlmodel import Field, SQLModel

# Tipos de rutina permitidos (RN22)
TipoRutina = Literal["calentamiento", "movilidad", "vuelta_a_la_calma"]


# Tabla rutinas (definida en database/schema.sql)
class Rutina(SQLModel, table=True):
    __tablename__ = "rutinas"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    tipo: str
    contraindicaciones: str | None = None
    descripcion: str | None = None
    entrenador_id: int | None = None


# Datos que se piden para cargar o editar una rutina
class RutinaDatos(SQLModel):
    nombre: str = Field(min_length=2, max_length=150)
    tipo: TipoRutina
    # Condiciones de salud que excluyen la rutina (RN19)
    contraindicaciones: str | None = Field(default=None, max_length=500)
    descripcion: str | None = Field(default=None, max_length=1000)


# Datos que se devuelven al frontend
class RutinaPublic(RutinaDatos):
    id: int
    entrenador_id: int | None
