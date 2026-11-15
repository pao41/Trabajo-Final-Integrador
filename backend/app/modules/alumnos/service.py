from app.core.security import generate_access_code, hash_password
from app.core.uow import UnitOfWork
from app.modules.alumnos.model import Alumno, AlumnoConCodigo, AlumnoDatos, AlumnoPublic


class AlumnoService:
    """Reglas de negocio de los alumnos."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def crear(self, datos: AlumnoDatos) -> AlumnoConCodigo:
        """Da de alta un alumno y genera su código de acceso; el DNI no se repite (RN13)."""
        self._validar_dni(datos.dni)
        codigo = generate_access_code()
        alumno = Alumno(
            nombre=datos.nombre.strip(),
            dni=datos.dni,
            contacto=datos.contacto,
            codigo_acceso_hash=hash_password(codigo),
        )
        return self._con_codigo(self.uow.alumnos.add(alumno), codigo)

    def listar(self, texto: str | None = None) -> list[AlumnoPublic]:
        return [AlumnoPublic.model_validate(a) for a in self.uow.alumnos.buscar(texto)]

    def obtener(self, alumno_id: int) -> AlumnoPublic:
        return AlumnoPublic.model_validate(self._buscar(alumno_id))