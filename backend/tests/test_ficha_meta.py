from fastapi.testclient import TestClient

from app.core.uow import UnitOfWork
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


def test_guardar_dos_veces_modifica_la_misma_ficha(admin):
    alumno_id = nuevo_alumno(admin)
    admin.put(f"/alumnos/{alumno_id}/ficha-salud", json=FICHA)

    admin.put(f"/alumnos/{alumno_id}/ficha-salud", json={**FICHA, "lesiones": "Hombro"})

    # Hay una sola ficha por alumno
    with UnitOfWork() as uow:
        assert len(uow.fichas_salud.get_all()) == 1
    assert admin.get(f"/alumnos/{alumno_id}/ficha-salud").json()["lesiones"] == "Hombro"


def test_el_entrenador_ve_la_ficha_pero_no_la_modifica(
    admin, crear_usuario, crear_entrenador, iniciar_sesion
):
    alumno_id = nuevo_alumno(admin)
    admin.put(f"/alumnos/{alumno_id}/ficha-salud", json=FICHA)
    entrenador = sesion_de_entrenador(crear_usuario, crear_entrenador, iniciar_sesion)

    assert entrenador.get(f"/alumnos/{alumno_id}/ficha-salud").status_code == 200
    assert entrenador.put(f"/alumnos/{alumno_id}/ficha-salud", json=FICHA).status_code == 403


def test_la_ficha_de_un_alumno_inexistente_da_404(admin):
    assert admin.get("/alumnos/999/ficha-salud").status_code == 404
    assert admin.put("/alumnos/999/ficha-salud", json=FICHA).status_code == 404


def test_un_alumno_sin_meta_tiene_la_meta_por_defecto(admin):
    alumno_id = nuevo_alumno(admin)

    respuesta = admin.get(f"/alumnos/{alumno_id}/meta")

    assert respuesta.json()["meta_asistencias_semanales"] == 3


def test_se_guarda_la_meta_semanal(admin):
    alumno_id = nuevo_alumno(admin)

    admin.put(f"/alumnos/{alumno_id}/meta", json={"meta_asistencias_semanales": 5})

    assert admin.get(f"/alumnos/{alumno_id}/meta").json()["meta_asistencias_semanales"] == 5


def test_una_meta_fuera_de_1_a_7_da_422(admin):
    alumno_id = nuevo_alumno(admin)

    assert (
        admin.put(f"/alumnos/{alumno_id}/meta", json={"meta_asistencias_semanales": 0}).status_code
        == 422
    )
    assert (
        admin.put(f"/alumnos/{alumno_id}/meta", json={"meta_asistencias_semanales": 8}).status_code
        == 422
    )