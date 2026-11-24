from datetime import date, time

from sqlmodel import Field, SQLModel

from app.modules.planes.model import InscripcionPublic


# Datos que escribe el alumno para entrar al panel
class AccesoDatos(SQLModel):
    dni: str = Field(min_length=1, max_length=20)
    codigo: str = Field(min_length=1, max_length=20)


# Avance de la meta semanal: ingresos de la semana en curso contra la meta del alumno
class ChecklistSemana(SQLModel):
    meta: int
    asistencias: int
    cumplida: bool


# Lo que ve el alumno al entrar: su cuota y su checklist (sin datos de salud)
class ResumenAlumno(SQLModel):
    nombre: str
    inscripcion: InscripcionPublic | None
    checklist: ChecklistSemana


# Un ingreso propio del alumno, para su historial de asistencia
class IngresoPropio(SQLModel):
    id: int
    fecha: date
    hora: time
    plan_nombre: str | None