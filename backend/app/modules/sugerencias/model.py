from datetime import date
from typing import Literal

from sqlmodel import Field, SQLModel

from app.modules.rutinas.model import TipoRutina

EstadoSugerencia = Literal["pendiente", "aprobada", "rechazada"]
# Cómo dice el alumno que se siente el día que consulta al asistente
Animo = Literal["con_energia", "cansado", "con_molestia"]


# Tabla rutinas_asignadas (definida en database/schema.sql): una sugerencia del asistente
class RutinaAsignada(SQLModel, table=True):
    __tablename__ = "rutinas_asignadas"

    id: int | None = Field(default=None, primary_key=True)
    alumno_id: int
    rutina_id: int
    estado: str = "pendiente"
    entrenador_id: int | None = None
    fecha_validacion: date | None = None


# Lo que el alumno elige en el chat del asistente (los dos datos son opcionales)
class SolicitudSugerencia(SQLModel):
    tipo: TipoRutina | None = None
    animo: Animo | None = None


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
