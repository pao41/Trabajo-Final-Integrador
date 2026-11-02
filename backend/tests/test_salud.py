from fastapi.testclient import TestClient

from app.database import get_session
from app.main import app

client = TestClient(app)


def test_salud_responde_ok_con_la_base_conectada():
    respuesta = client.get("/salud")
    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "ok"
    assert respuesta.json()["base_de_datos"] == "ok"


def test_salud_responde_503_si_la_base_falla():
    class SesionRota:
        def exec(self, *args, **kwargs):
            raise RuntimeError("sin conexión")

    app.dependency_overrides[get_session] = lambda: SesionRota()
    try:
        respuesta = client.get("/salud")
    finally:
        app.dependency_overrides.clear()
    assert respuesta.status_code == 503
