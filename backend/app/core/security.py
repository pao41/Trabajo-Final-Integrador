import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    """Devuelve el hash de la contraseña: nunca se guarda el texto original."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Compara la contraseña con su hash."""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        # bcrypt rechaza contraseñas de más de 72 bytes: se toma como incorrecta
        return False


def create_access_token(user_id: int, rol: str) -> str:
    """Crea el token de sesión firmado, con fecha de vencimiento."""
    vence = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    datos = {"sub": str(user_id), "rol": rol, "exp": vence}
    return jwt.encode(datos, settings.secret_key, algorithm="HS256")


def decode_access_token(token: str) -> dict | None:
    """Devuelve los datos del token, o None si es inválido, fue alterado o venció."""
    try:
        return jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None


# Minutos que dura la sesión del alumno (más corta que la del personal)
MINUTOS_SESION_ALUMNO = 60


def create_alumno_token(alumno_id: int) -> str:
    """Crea el token de sesión del alumno; la marca "aud" lo distingue del token del personal."""
    vence = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_SESION_ALUMNO)
    datos = {"sub": str(alumno_id), "aud": "alumno", "exp": vence}
    return jwt.encode(datos, settings.secret_key, algorithm="HS256")


def decode_alumno_token(token: str) -> dict | None:
    """Devuelve los datos del token del alumno, o None si es inválido, venció o no es de alumno."""
    try:
        return jwt.decode(token, settings.secret_key, algorithms=["HS256"], audience="alumno")
    except jwt.PyJWTError:
        return None


# Letras y números sin los que se confunden entre sí (0/O, 1/I/L)
ALFABETO_CODIGO = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"


def generate_access_code() -> str:
    """Genera un código de acceso aleatorio de 8 caracteres; no se deriva del DNI."""
    return "".join(secrets.choice(ALFABETO_CODIGO) for _ in range(8))
