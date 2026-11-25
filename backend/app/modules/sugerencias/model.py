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