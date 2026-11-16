from datetime import datetime, timedelta

from app.core.clock import now_ar

MAX_INTENTOS = 5
MINUTOS_DE_BLOQUEO = 15


class ControlDeIntentos:
    """Cuenta los intentos fallidos seguidos de cada usuario y lo bloquea por un tiempo."""

    def __init__(self):
        self.fallos: dict[str, int] = {}
        self.bloqueado_hasta: dict[str, datetime] = {}

    def registrar_fallo(self, clave: str) -> None:
        """Suma un fallo; al llegar al máximo bloquea la clave."""
        self.fallos[clave] = self.fallos.get(clave, 0) + 1
        if self.fallos[clave] >= MAX_INTENTOS:
            self.bloqueado_hasta[clave] = now_ar() + timedelta(minutes=MINUTOS_DE_BLOQUEO)

    def limpiar(self, clave: str) -> None:
        """Borra los fallos y el bloqueo de la clave."""
        self.fallos.pop(clave, None)
        self.bloqueado_hasta.pop(clave, None)