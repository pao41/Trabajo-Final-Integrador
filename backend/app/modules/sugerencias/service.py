from fastapi import HTTPException, status

from app.core.clock import today_ar
from app.core.uow import UnitOfWork
from app.modules.alumnos.model import FichaSalud
from app.modules.rutinas.model import Rutina
from app.modules.sugerencias.ia import elegir
from app.modules.sugerencias.model import (
    RutinaAprobada,
    RutinaAsignada,
    RutinasDelAlumno,
    SolicitudSugerencia,
    SugerenciaPublic,
)

# Aclaración que acompaña a toda rutina que ve el alumno
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

    def solicitar(self, alumno_id: int, datos: SolicitudSugerencia) -> str | None:
        """Deja una rutina compatible con la ficha como sugerencia pendiente.

        Devuelve la explicación de la IA, o None si la IA no respondió."""
        ficha = self.uow.fichas_salud.get_by_alumno(alumno_id)
        if not ficha:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                "Todavía no tenés una ficha de salud: pedí que la carguen en el gimnasio",
            )
        anteriores = self.uow.sugerencias.de_alumno(alumno_id)
        if any(s.estado == "pendiente" for s in anteriores):
            raise HTTPException(
                status.HTTP_409_CONFLICT, "Ya tenés una sugerencia pendiente de aprobación"
            )
        ya_sugeridas = {s.rutina_id for s in anteriores}
        candidatas = [
            rutina
            for rutina in self.uow.rutinas.listar()
            if rutina.id not in ya_sugeridas
            and es_compatible(rutina, ficha)
            and (datos.tipo is None or rutina.tipo == datos.tipo)
        ]
        if not candidatas:
            raise HTTPException(
                status.HTTP_409_CONFLICT, "No hay rutinas compatibles para sugerirte por ahora"
            )
        rutina, explicacion = elegir(candidatas, ficha, datos.animo)
        self.uow.sugerencias.add(RutinaAsignada(alumno_id=alumno_id, rutina_id=rutina.id))
        return explicacion

    def listar(self, estado: str | None) -> list[SugerenciaPublic]:
        return [self._armar(s) for s in self.uow.sugerencias.listar(estado)]

    def resolver(self, sugerencia_id: int, entrenador_id: int, estado: str) -> SugerenciaPublic:
        """Aprueba o rechaza una sugerencia pendiente, a nombre del entrenador (RN21, RN24)."""
        sugerencia = self.uow.sugerencias.get_by_id(sugerencia_id)
        if not sugerencia:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Sugerencia no encontrada")
        if sugerencia.estado != "pendiente":
            raise HTTPException(status.HTTP_409_CONFLICT, "Esa sugerencia ya fue resuelta")
        sugerencia.estado = estado
        sugerencia.entrenador_id = entrenador_id
        sugerencia.fecha_validacion = today_ar()
        return self._armar(self.uow.sugerencias.update(sugerencia))

    def rutinas_del_alumno(self, alumno_id: int) -> RutinasDelAlumno:
        """Solo las rutinas aprobadas llegan al alumno (RN21)."""
        rutinas = [
            RutinaAprobada.model_validate(self.uow.rutinas.get_by_id(s.rutina_id))
            for s in self.uow.sugerencias.de_alumno(alumno_id)
            if s.estado == "aprobada"
        ]
        return RutinasDelAlumno(aviso=AVISO, rutinas=rutinas)

    def _armar(self, sugerencia: RutinaAsignada) -> SugerenciaPublic:
        alumno = self.uow.alumnos.get_by_id(sugerencia.alumno_id)
        rutina = self.uow.rutinas.get_by_id(sugerencia.rutina_id)
        ficha = self.uow.fichas_salud.get_by_alumno(sugerencia.alumno_id)
        return SugerenciaPublic(
            id=sugerencia.id,
            estado=sugerencia.estado,
            alumno_nombre=alumno.nombre,
            rutina_nombre=rutina.nombre,
            rutina_tipo=rutina.tipo,
            contraindicaciones=rutina.contraindicaciones,
            problemas_cardiacos=ficha.problemas_cardiacos if ficha else False,
            lesiones=ficha.lesiones if ficha else None,
            fecha_validacion=sugerencia.fecha_validacion,
        )
