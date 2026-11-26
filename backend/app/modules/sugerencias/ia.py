import json
import logging
import urllib.request

from app.core.config import settings
from app.modules.alumnos.model import FichaSalud
from app.modules.rutinas.model import Rutina

URL = "https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"
# Segundos máximos de espera de la respuesta de la IA
ESPERA = 8

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


def consultar(texto: str) -> str:
    """Envía el texto a Gemini y devuelve la respuesta."""
    pedido = urllib.request.Request(
        URL.format(modelo=settings.gemini_model),
        data=json.dumps({"contents": [{"parts": [{"text": texto}]}]}).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": settings.gemini_api_key},
    )
    with urllib.request.urlopen(pedido, timeout=ESPERA) as respuesta:
        datos = json.load(respuesta)
    return datos["candidates"][0]["content"]["parts"][0]["text"]


def elegir(
    candidatas: list[Rutina], ficha: FichaSalud, animo: str | None
) -> tuple[Rutina, str | None]:
    """La IA elige una de las candidatas y explica por qué; si no responde, queda la primera."""
    if settings.gemini_api_key:
        try:
            respuesta = consultar(armar_consulta(candidatas, ficha, animo))
            numero, explicacion = respuesta.strip().split("\n", 1)
            posicion = int(numero.strip().rstrip(".")) - 1
            if 0 <= posicion < len(candidatas):
                return candidatas[posicion], explicacion.strip()[:400]
        except (OSError, ValueError, KeyError, IndexError) as error:
            logging.warning("No se pudo consultar a la IA: %s", error)
    return candidatas[0], None