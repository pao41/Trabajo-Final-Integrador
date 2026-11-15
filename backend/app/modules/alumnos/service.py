from fastapi import HTTPException, status

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

    def editar(self, alumno_id: int, datos: AlumnoDatos) -> AlumnoPublic:
        """Modifica nombre, DNI y contacto; si cambia el DNI, tampoco puede repetirse."""
        alumno = self._buscar(alumno_id)
        if datos.dni != alumno.dni:
            self._validar_dni(datos.dni)
        alumno.nombre = datos.nombre.strip()
        alumno.dni = datos.dni
        alumno.contacto = datos.contacto
        return AlumnoPublic.model_validate(self.uow.alumnos.update(alumno))

    def cambiar_estado(self, alumno_id: int, activo: bool) -> AlumnoPublic:
        """Baja lógica (RN14): el alumno no se elimina, queda inactivo con su historial."""
        alumno = self._buscar(alumno_id)
        alumno.activo = activo
        return AlumnoPublic.model_validate(self.uow.alumnos.update(alumno))

    def regenerar_codigo(self, alumno_id: int) -> AlumnoConCodigo:
        """Genera un código nuevo; el anterior deja de ser válido (RN37)."""
        alumno = self._buscar(alumno_id)
        codigo = generate_access_code()
        alumno.codigo_acceso_hash = hash_password(codigo)
        return self._con_codigo(self.uow.alumnos.update(alumno), codigo)

    def _buscar(self, alumno_id: int) -> Alumno:
        alumno = self.uow.alumnos.get_by_id(alumno_id)
        if not alumno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado",
            )
        return alumno

    def _validar_dni(self, dni: str) -> None:
        """El DNI lleva solo números y no puede repetirse (RN13)."""
        if not (dni.isascii() and dni.isdigit()):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="El DNI debe tener solo números",
            )
        if self.uow.alumnos.get_by_dni(dni):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un alumno con ese DNI",
            )

    def _con_codigo(self, alumno: Alumno, codigo: str) -> AlumnoConCodigo:
        datos = AlumnoPublic.model_validate(alumno).model_dump()
        return AlumnoConCodigo(**datos, codigo_acceso=codigo)