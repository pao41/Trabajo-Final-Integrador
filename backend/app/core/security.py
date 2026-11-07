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