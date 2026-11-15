from fastapi.testclient import TestClient

from app.main import app

FICHA = {"problemas_cardiacos": True, "lesiones": "Rodilla derecha", "observaciones": None}


def nuevo_alumno(admin):
    datos = {"nombre": "Ana Pérez", "dni": "30111222"}
    return admin.post("/alumnos", json=datos).json()["id"]


def sesion_de_entrenador(crear_usuario, crear_entrenador, iniciar_sesion):
    crear_usuario("laura", rol="entrenador", entrenador_id=crear_entrenador())
    entrenador = TestClient(app)
    iniciar_sesion(entrenador, "laura")
    return entrenador


def test_sin_sesion_no_se_ve_la_ficha(client):
    assert client.get("/alumnos/1/ficha-salud").status_code == 401
