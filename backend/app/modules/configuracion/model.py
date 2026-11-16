from typing import Literal

from sqlalchemy import ARRAY, Column, String
from sqlmodel import Field, SQLModel

# Métodos de pago que acepta el sistema (RN08)
MetodoPago = Literal["efectivo", "transferencia", "debito", "credito"]


# Tabla configuracion: tiene una sola fila, la del id 1 (definida en database/schema.sql)
class Configuracion(SQLModel, table=True):
    __tablename__ = "configuracion"

    id: int = Field(default=1, primary_key=True)
    nombre_gimnasio: str
    dias_aviso_vencimiento: int = 7
    metodos_pago_habilitados: list[str] = Field(sa_column=Column(ARRAY(String), nullable=False))


# Datos que el administrador puede modificar
class ConfiguracionDatos(SQLModel):
    nombre_gimnasio: str = Field(min_length=2, max_length=150)
    # Días de anticipación para el estado "por vencer" (RN09)
    dias_aviso_vencimiento: int = Field(ge=1, le=60)
    metodos_pago_habilitados: list[MetodoPago] = Field(min_length=1)
