from fastapi.testclient import TestClient

from app.main import app

NUEVA = {
    "nombre": "Movilidad de hombros",
    "tipo": "movilidad",
    "contraindicaciones": "Lesión de hombro",
    "descripcion": "Círculos suaves con los brazos, 2 series de 10.",
}


def entrenador_con_sesion(crear_usuario, crear_entrenador, iniciar_sesion, nombre="laura"):
    """Crea un usuario entrenador y devuelve un cliente con su sesión iniciada."""
    entrenador_id = crear_entrenador()
    crear_usuario(nombre, rol="entrenador", entrenador_id=entrenador_id)
    sesion = TestClient(app)
    iniciar_sesion(sesion, nombre)
    return sesion, entrenador_id
