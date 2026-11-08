from datetime import date

from sqlmodel import Field, SQLModel

from app.core.clock import today_ar


# Tabla usuarios (definida en database/schema.sql)
class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: int | None = Field(default=None, primary_key=True)
    nombre_usuario: str
    password_hash: str
    rol: str
    entrenador_id: int | None = None
    activo: bool = True
    fecha_alta: date = Field(default_factory=today_ar)


# Datos que se piden para dar de alta un usuario
class UsuarioCreate(SQLModel):
    nombre_usuario: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=72)


# Datos que se devuelven al frontend (nunca incluyen el hash de la contraseña)
class UsuarioPublic(SQLModel):
    id: int
    nombre_usuario: str
    rol: str
    entrenador_id: int | None
    activo: bool
    fecha_alta: date


# Dato que se pide para restablecer la contraseña
class CambioPassword(SQLModel):
    nueva_password: str = Field(min_length=8, max_length=72)
