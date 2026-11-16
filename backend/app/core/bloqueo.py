from datetime import datetime, timedelta

from fastapi import HTTPException, status

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

    def verificar(self, clave: str) -> None:
        """Rechaza el intento si la clave sigue bloqueada."""
        hasta = self.bloqueado_hasta.get(clave)
        if hasta is None:
            return
        if now_ar() >= hasta:
            # El bloqueo ya terminó: se empieza de cero
            self.limpiar(clave)
            return
        minutos = int((hasta - now_ar()).total_seconds() // 60) + 1
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Demasiados intentos fallidos. Probá de nuevo en {minutos} minutos",
        )

    def reiniciar(self) -> None:
        """Olvida todo (lo usan las pruebas)."""
        self.fallos.clear()
        self.bloqueado_hasta.clear()


# Un solo control para toda la aplicación (lo comparten el personal y el panel del alumno)
control_de_intentos = ControlDeIntentos()
