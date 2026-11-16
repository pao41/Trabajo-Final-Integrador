from decimal import Decimal

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
