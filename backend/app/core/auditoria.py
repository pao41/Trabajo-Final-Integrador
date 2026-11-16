import logging
from contextlib import contextmanager

from fastapi import HTTPException

from app.core.clock import now_ar

registro = logging.getLogger("auditoria")
registro.setLevel(logging.INFO)
consola = logging.StreamHandler()
consola.setFormatter(logging.Formatter("%(message)s"))
registro.addHandler(consola)


def escribir(usuario: str, accion: str, entidad: str, resultado: str) -> None:
    """Escribe una línea del registro: fecha y hora | usuario | acción | entidad | resultado."""
    registro.info(f"{now_ar():%Y-%m-%d %H:%M:%S} | {usuario} | {accion} | {entidad} | {resultado}")


@contextmanager
def auditar(usuario: str, accion: str, entidad: str):
    """Registra la acción como éxito si termina bien y como rechazo si el sistema la rechaza."""
    try:
        yield
    except HTTPException:
        escribir(usuario, accion, entidad, "rechazo")
        raise
    escribir(usuario, accion, entidad, "éxito")