from app.core.uow import UnitOfWork
from app.modules.alumnos.model import FichaSalud
from app.modules.rutinas.model import Rutina

# Aclaración que acompaña a toda rutina que ve el alumno (RN23)
AVISO = (
    "Estas rutinas son una guía orientativa: no reemplazan la supervisión presencial "
    "del entrenador ni una evaluación médica profesional."
)


def es_compatible(rutina: Rutina, ficha: FichaSalud) -> bool:
    """Una rutina sirve si sus contraindicaciones no mencionan nada de la ficha del alumno."""
    texto = (rutina.contraindicaciones or "").lower()
    if ficha.problemas_cardiacos and "card" in texto:
        return False
    lesiones = (ficha.lesiones or "").lower().replace(",", " ").replace(".", " ")
    # Se comparan las palabras de más de 3 letras (así se ignoran "de", "la", etc.)
    return not any(len(palabra) > 3 and palabra in texto for palabra in lesiones.split())


class AsistenteService:
    """Asistente de IA: filtra el banco de rutinas, no inventa ejercicios (RN18)."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow
