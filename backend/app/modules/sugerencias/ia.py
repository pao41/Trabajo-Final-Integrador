from app.modules.alumnos.model import FichaSalud
from app.modules.rutinas.model import Rutina

# Cómo se describe en la consulta lo que el alumno dijo sobre cómo se siente
ANIMOS = {
    "con_energia": "con energía",
    "cansado": "cansado/a",
    "con_molestia": "con alguna molestia",
}


def armar_consulta(candidatas: list[Rutina], ficha: FichaSalud, animo: str | None) -> str:
    """Arma el texto para la IA: solo datos de salud y rutinas, sin nombre ni DNI del alumno."""
    opciones = "\n".join(
        f"{i}. {r.nombre}: {r.descripcion or 'sin descripción'}"
        for i, r in enumerate(candidatas, start=1)
    )
    return (
        "Sos el asistente de un gimnasio. Elegí una sola rutina de la lista para una persona "
        f"que hoy se siente {ANIMOS.get(animo, 'bien')}.\n"
        f"Problemas cardíacos declarados: {'sí' if ficha.problemas_cardiacos else 'no'}.\n"
        f"Lesiones declaradas: {ficha.lesiones or 'ninguna'}.\n"
        f"Rutinas:\n{opciones}\n"
        "Respondé en dos líneas. Primera línea: solo el número de la rutina elegida. "
        "Segunda línea: explicá en una o dos oraciones, hablándole de vos, por qué es adecuada. "
        "No uses nombres propios y no inventes ejercicios ni rutinas."
    )