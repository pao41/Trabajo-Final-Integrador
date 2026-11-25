from sqlmodel import Session

from app.core.database import engine
from app.modules.alumnos.repository import (
    AlumnoRepository,
    FichaSaludRepository,
    MetaAlumnoRepository,
)
from app.modules.asistencias.repository import AsistenciaRepository
from app.modules.configuracion.repository import ConfiguracionRepository
from app.modules.dashboard.repository import DashboardRepository
from app.modules.entrenadores.repository import EntrenadorRepository
from app.modules.pagos.repository import PagoRepository
from app.modules.planes.repository import InscripcionRepository, PlanRepository
from app.modules.rutinas.repository import RutinaRepository
from app.modules.sugerencias.repository import SugerenciaRepository
from app.modules.usuarios.repository import UsuarioRepository


class UnitOfWork:
    """Abre una sesión y, al terminar el bloque with, confirma todo junto o lo descarta."""

    def __init__(self):
        self.session: Session | None = None

    def __enter__(self):
        # expire_on_commit=False deja los objetos legibles después del commit
        self.session = Session(engine, expire_on_commit=False)
        # Acá se crea el repositorio de cada módulo (una línea por módulo)
        self.usuarios = UsuarioRepository(self.session)
        self.alumnos = AlumnoRepository(self.session)
        self.fichas_salud = FichaSaludRepository(self.session)
        self.metas = MetaAlumnoRepository(self.session)
        self.configuracion = ConfiguracionRepository(self.session)
        self.planes = PlanRepository(self.session)
        self.inscripciones = InscripcionRepository(self.session)
        self.pagos = PagoRepository(self.session)
        self.asistencias = AsistenciaRepository(self.session)
        self.dashboard = DashboardRepository(self.session)
        self.entrenadores = EntrenadorRepository(self.session)
        self.rutinas = RutinaRepository(self.session)
        self.sugerencias = SugerenciaRepository(self.session)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                self.session.rollback()
            else:
                self.session.commit()
        finally:
            # La sesión se cierra siempre, aunque el commit falle
            self.session.close()


def get_uow() -> UnitOfWork:
    """Dependencia de FastAPI: entrega un Unit of Work por petición."""
    return UnitOfWork()
