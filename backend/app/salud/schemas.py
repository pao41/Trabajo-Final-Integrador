from datetime import datetime

from pydantic import BaseModel


class EstadoSalud(BaseModel):
    estado: str
    base_de_datos: str
    hora_argentina: datetime

