from fastapi.testclient import TestClient

from app.main import app

NUEVO = {"nombre": "Laura Gómez", "contacto": "387-4111111"}


def alta(admin, **cambios):
    """Da de alta un entrenador por la API y devuelve la respuesta."""
    return admin.post("/entrenadores", json={**NUEVO, **cambios})


def test_solo_el_administrador_gestiona_entrenadores(
    client, crear_usuario, crear_entrenador, iniciar_sesion
):
    crear_usuario("laura", rol="entrenador", entrenador_id=crear_entrenador())
    entrenador = TestClient(app)
    iniciar_sesion(entrenador, "laura")

    assert client.get("/entrenadores").status_code == 401
    assert entrenador.get("/entrenadores").status_code == 403
    assert entrenador.post("/entrenadores", json=NUEVO).status_code == 403