from app.core.uow import UnitOfWork


class PanelAlumnoService:
    """Acceso y consultas del panel de autoconsulta del alumno (solo lectura)."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow