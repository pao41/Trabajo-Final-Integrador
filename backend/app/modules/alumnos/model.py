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


# Datos que se devuelven al frontend (nunca incluyen el hash del código)
class AlumnoPublic(SQLModel):
    id: int
    nombre: str
    dni: str
    contacto: str | None
    activo: bool
    fecha_alta: date


# Respuesta del alta y de la regeneración: el código se muestra una única vez (RN37)
class AlumnoConCodigo(AlumnoPublic):
    codigo_acceso: str


# Tabla ficha_salud
class FichaSalud(SQLModel, table=True):
    __tablename__ = "ficha_salud"

    id: int | None = Field(default=None, primary_key=True)
    alumno_id: int
    problemas_cardiacos: bool = False
    lesiones: str | None = None
    observaciones: str | None = None
    fecha_registro: date = Field(default_factory=today_ar)


# Datos de la ficha de salud que carga el administrador
class FichaSaludDatos(SQLModel):
    problemas_cardiacos: bool = False
    lesiones: str | None = Field(default=None, max_length=500)
    observaciones: str | None = Field(default=None, max_length=500)


# Ficha que se devuelve; sin fecha si todavía no se cargó
class FichaSaludPublic(FichaSaludDatos):
    fecha_registro: date | None = None


# Tabla metas_alumno
class MetaAlumno(SQLModel, table=True):
    __tablename__ = "metas_alumno"

    id: int | None = Field(default=None, primary_key=True)
    alumno_id: int
    meta_asistencias_semanales: int = 3
    fecha_actualizacion: date = Field(default_factory=today_ar)


# Meta semanal de asistencias (de 1 a 7 días)
class MetaDatos(SQLModel):
    meta_asistencias_semanales: int = Field(default=3, ge=1, le=7)
