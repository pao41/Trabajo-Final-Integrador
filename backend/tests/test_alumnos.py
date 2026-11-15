from fastapi.testclient import TestClient

from app.core.security import verify_password
from app.core.uow import UnitOfWork
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


def test_el_alta_devuelve_el_alumno_activo_y_su_codigo_de_acceso(admin):
    respuesta = alta(admin)

    assert respuesta.status_code == 201
    datos = respuesta.json()
    assert datos["nombre"] == "Ana Pérez"
    assert datos["activo"] is True
    # El código se muestra en el alta (RN37)
    assert len(datos["codigo_acceso"]) == 8


def test_la_base_guarda_el_hash_del_codigo_y_no_el_codigo(admin):
    datos = alta(admin).json()

    uow = UnitOfWork()
    with uow:
        guardado = uow.alumnos.get_by_id(datos["id"])
        assert guardado.codigo_acceso_hash.startswith("$2b$")
        assert datos["codigo_acceso"] not in guardado.codigo_acceso_hash
        assert verify_password(datos["codigo_acceso"], guardado.codigo_acceso_hash)