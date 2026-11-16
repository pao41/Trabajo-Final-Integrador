from datetime import date
from decimal import Decimal

from sqlmodel import Field, SQLModel

from app.modules.configuracion.model import MetodoPago
from app.modules.planes.model import InscripcionPublic


# Tabla pagos (definida en database/schema.sql)
class Pago(SQLModel, table=True):
    __tablename__ = "pagos"

    id: int | None = Field(default=None, primary_key=True)
    inscripcion_id: int
    fecha_pago: date
    monto: Decimal
    metodo_pago: str


# Datos que se piden al registrar un pago: el monto lo toma el servidor del plan (RN05)
class PagoDatos(SQLModel):
    inscripcion_id: int
    metodo_pago: MetodoPago
    fecha_pago: date | None = None


# Pago que se devuelve al frontend, con los datos para mostrarlo en el historial
class PagoPublic(SQLModel):
    id: int
    inscripcion_id: int
    alumno_id: int
    plan_nombre: str
    fecha_pago: date
    monto: Decimal
    metodo_pago: str


# Respuesta de registrar un pago: el pago y cómo quedó la inscripción
class PagoRegistrado(SQLModel):
    pago: PagoPublic
    inscripcion: InscripcionPublic
