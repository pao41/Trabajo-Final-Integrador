from datetime import date

from sqlmodel import Field, SQLModel

from app.core.clock import today_ar


# Tabla alumnos (definida en database/schema.sql)
class Alumno(SQLModel, table=True):
    __tablename__ = "alumnos"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    dni: str
    contacto: str | None = None
    codigo_acceso_hash: str
    activo: bool = True
    fecha_alta: date = Field(default_factory=today_ar)


# Datos que se piden para dar de alta o editar un alumno
class AlumnoDatos(SQLModel):
    nombre: str = Field(min_length=2, max_length=150)
    dni: str = Field(min_length=6, max_length=20)
    contacto: str | None = Field(default=None, max_length=150)
