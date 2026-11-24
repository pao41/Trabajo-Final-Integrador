from fastapi.testclient import TestClient

from app.main import app
from tests.test_alumnos import alta


def entrar(dni, codigo):
    """Un cliente nuevo, sin la sesión del administrador, que intenta entrar al panel."""
    cliente = TestClient(app)
    respuesta = cliente.post("/panel-alumno/acceso", json={"dni": dni, "codigo": codigo})
    return cliente, respuesta


def test_el_error_es_el_mismo_si_falla_el_dni_o_el_codigo(admin):
    alumno = alta(admin).json()

    _, dni_inexistente = entrar("99999999", alumno["codigo_acceso"])
    _, codigo_incorrecto = entrar(alumno["dni"], "XXXXXXXX")

    assert dni_inexistente.status_code == codigo_incorrecto.status_code == 401
    assert dni_inexistente.json() == codigo_incorrecto.json()
