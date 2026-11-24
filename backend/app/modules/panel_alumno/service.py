from app.core.security import create_alumno_token, verify_password
from app.core.uow import UnitOfWork
from app.modules.alumnos.model import AlumnoPublic
from app.modules.asistencias.service import AsistenciaService
from app.modules.panel_alumno.model import (
    AccesoDatos,
    IngresoPropio,
    ResumenAlumno,
)
from app.modules.planes.inscripcion_service import InscripcionService


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


    def resumen(self, alumno: AlumnoPublic) -> ResumenAlumno:
        """Cuota actual (la inscripción más reciente) y checklist de la semana."""
        inscripciones = self.uow.inscripciones.listar(alumno.id)
        actual = inscripciones[0] if inscripciones else None
        inscripcion = InscripcionService(self.uow).armar(actual) if actual else None
        return ResumenAlumno(
            nombre=alumno.nombre,
            inscripcion=inscripcion,
            checklist=self._checklist(alumno.id),
        )

    def historial(self, alumno: AlumnoPublic) -> list[IngresoPropio]:
        """Ingresos del propio alumno, el más nuevo primero."""
        ingresos = AsistenciaService(self.uow).listar(alumno_id=alumno.id)
        return [IngresoPropio.model_validate(i, from_attributes=True) for i in ingresos]