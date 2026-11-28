from datetime import date, time

from sqlmodel import Field, SQLModel

from app.modules.planes.model import InscripcionPublic


# Tabla asistencias (definida en database/schema.sql)
class Asistencia(SQLModel, table=True):
    __tablename__ = "asistencias"

    id: int | None = Field(default=None, primary_key=True)
    alumno_id: int
    inscripcion_id: int | None = None
    fecha: date
    hora: time


# Datos que se piden al registrar un ingreso: la fecha y la hora las pone el servidor
class AsistenciaDatos(SQLModel):
    alumno_id: int


# Ingreso que se devuelve al frontend, con los nombres para mostrarlo en el historial
class AsistenciaPublic(SQLModel):
    id: int
    alumno_id: int
    alumno_nombre: str
    inscripcion_id: int | None
    plan_nombre: str | None
    clases_restantes: int | None
    fecha: date
    hora: time

# Respuesta de registrar un ingreso: el ingreso y cómo quedó la inscripción
class AsistenciaRegistrada(SQLModel):
    asistencia: AsistenciaPublic
    inscripcion: InscripcionPublic
