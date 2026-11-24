from fastapi import HTTPException, status

from app.core.bloqueo import control_de_intentos
from app.core.security import create_alumno_token, verify_password
from app.core.uow import UnitOfWork
from app.modules.panel_alumno.model import (
    AccesoDatos,
)


class PanelAlumnoService:
    """Acceso y consultas del panel de autoconsulta del alumno (solo lectura)."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def acceder(self, datos: AccesoDatos) -> str:
        """Valida DNI y código y devuelve el token de sesión del alumno."""
        dni = datos.dni.strip()
        # Los códigos se generan en mayúsculas: se acepta también escrito en minúsculas
        codigo = datos.codigo.strip().upper()
        clave = f"alumno:{dni}"
        # Si ese DNI está bloqueado por intentos fallidos, ni se comprueba el código
        control_de_intentos.verificar(clave)
        alumno = self.uow.alumnos.get_by_dni(dni)
        # El mismo mensaje si falla el DNI, el código o el alumno está dado de baja
        datos_validos = alumno is not None and verify_password(codigo, alumno.codigo_acceso_hash)
        if not datos_validos or not alumno.activo:
            control_de_intentos.registrar_fallo(clave)
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "DNI o código incorrectos")
        control_de_intentos.limpiar(clave)
        return create_alumno_token(alumno.id)
