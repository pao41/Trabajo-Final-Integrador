from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración leída de las variables de entorno o del archivo .env."""

    database_url: str
    frontend_origin: str = "http://localhost:5173"
    # Clave con la que se firman las sesiones (obligatoria, mínimo 32 caracteres)
    secret_key: str
    # Duración de la sesión en minutos (480 = un turno de 8 horas)
    access_token_expire_minutes: int = 480
    # La cookie viaja solo por HTTPS cuando es True (se activa en producción)
    cookie_secure: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

# La aplicación no arranca con una clave corta
if len(settings.secret_key) < 32:
    raise ValueError("SECRET_KEY debe tener al menos 32 caracteres")
