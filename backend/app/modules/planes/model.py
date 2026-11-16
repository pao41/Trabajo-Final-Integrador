from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import model_validator
from sqlmodel import Field, SQLModel


# Tabla planes (definida en database/schema.sql)
class Plan(SQLModel, table=True):
    __tablename__ = "planes"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    duracion_dias: int
    precio: Decimal
    tipo: str
    cantidad_clases: int | None = None


# Datos que se piden para crear o editar un plan
class PlanDatos(SQLModel):
    nombre: str = Field(min_length=2, max_length=100)
    duracion_dias: int = Field(gt=0)
    precio: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    tipo: Literal["tiempo", "clases"]
    cantidad_clases: int | None = Field(default=None, gt=0)

    @model_validator(mode="after")
    def comprobar_cantidad_de_clases(self):
        """Un plan por clases indica cuántas clases tiene; uno por tiempo no (RN29)."""
        if self.tipo == "clases" and self.cantidad_clases is None:
            raise ValueError("Un plan por clases debe indicar su cantidad de clases")
        if self.tipo == "tiempo" and self.cantidad_clases is not None:
            raise ValueError("Un plan por tiempo no lleva cantidad de clases")
        return self


# Plan que se devuelve al frontend
class PlanPublic(PlanDatos):
    id: int


# Tabla inscripciones (definida en database/schema.sql)
class Inscripcion(SQLModel, table=True):
    __tablename__ = "inscripciones"

    id: int | None = Field(default=None, primary_key=True)
    alumno_id: int
    plan_id: int
    fecha_inicio: date
    fecha_vencimiento: date
    clases_restantes: int | None = None
    estado: str = "activo"


# Datos que se piden para inscribir a un alumno; sin fecha de inicio se toma la de hoy
class InscripcionDatos(SQLModel):
    alumno_id: int
    plan_id: int
    fecha_inicio: date | None = None
