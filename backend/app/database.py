from sqlmodel import Session, create_engine

from app.config import settings


def _con_driver(url: str) -> str:
    """Indica el driver (psycopg) y acepta las URL "postgres://" que entregan algunos servicios."""
    for prefijo in ("postgres://", "postgresql://"):
        if url.startswith(prefijo):
            return "postgresql+psycopg://" + url[len(prefijo) :]
    return url


engine = create_engine(_con_driver(settings.database_url), pool_pre_ping=True)


def get_session():
    """Entrega una sesión por petición y la cierra al terminar."""
    with Session(engine) as session:
        yield session
