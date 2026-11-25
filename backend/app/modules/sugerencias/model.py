from datetime import date
from typing import Literal

from sqlmodel import Field, SQLModel

EstadoSugerencia = Literal["pendiente", "aprobada", "rechazada"]


# Tabla rutinas_asignadas (definida en database/schema.sql): una sugerencia del asistente
class RutinaAsignada(SQLModel, table=True):
    __tablename__ = "rutinas_asignadas"

    id: int | None = Field(default=None, primary_key=True)
    alumno_id: int
    rutina_id: int
    estado: str = "pendiente"
    entrenador_id: int | None = None
    fecha_validacion: date | None = None


# Sugerencia como la ve el personal: con lo necesario para decidir si se aprueba
class SugerenciaPublic(SQLModel):
    id: int
    estado: str
    alumno_nombre: str
    rutina_nombre: str
    rutina_tipo: str
    contraindicaciones: str | None
    problemas_cardiacos: bool
    lesiones: str | None
    fecha_validacion: date | None


# Rutina aprobada como la ve el alumno
class RutinaAprobada(SQLModel):
    nombre: str
    tipo: str
    descripcion: str | None
    contraindicaciones: str | None


# Rutinas aprobadas del alumno, siempre con la aclaración obligatoria (RN23)
class RutinasDelAlumno(SQLModel):
    aviso: str
    rutinas: list[RutinaAprobada]
