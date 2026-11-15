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


def test_un_alumno_sin_ficha_devuelve_una_ficha_vacia(admin):
    alumno_id = nuevo_alumno(admin)

    respuesta = admin.get(f"/alumnos/{alumno_id}/ficha-salud")

    assert respuesta.status_code == 200
    assert respuesta.json()["problemas_cardiacos"] is False
    assert respuesta.json()["fecha_registro"] is None


def test_se_guarda_y_se_consulta_la_ficha(admin):
    alumno_id = nuevo_alumno(admin)

    guardada = admin.put(f"/alumnos/{alumno_id}/ficha-salud", json=FICHA)

    assert guardada.status_code == 200
    ficha = admin.get(f"/alumnos/{alumno_id}/ficha-salud").json()
    assert ficha["problemas_cardiacos"] is True
    assert ficha["lesiones"] == "Rodilla derecha"
    assert ficha["fecha_registro"] is not None
