from fastapi.testclient import TestClient

from app.main import app

NUEVO = {"nombre": "Ana Pérez", "dni": "30111222", "contacto": "387-4000000"}


def alta(admin, **cambios):
    """Da de alta un alumno por la API y devuelve la respuesta."""
    return admin.post("/alumnos", json={**NUEVO, **cambios})


def test_sin_sesion_no_se_puede_gestionar_alumnos(client):
    assert client.get("/alumnos").status_code == 401


def test_el_entrenador_no_puede_gestionar_alumnos(crear_usuario, crear_entrenador, iniciar_sesion):
    crear_usuario("laura", rol="entrenador", entrenador_id=crear_entrenador())
    entrenador = TestClient(app)
    iniciar_sesion(entrenador, "laura")

    assert entrenador.get("/alumnos").status_code == 403
    assert entrenador.post("/alumnos", json=NUEVO).status_code == 403