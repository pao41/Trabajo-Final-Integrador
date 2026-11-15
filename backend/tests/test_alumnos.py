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


def test_el_codigo_no_se_deriva_del_dni(admin):
    primero = alta(admin).json()["codigo_acceso"]
    segundo = alta(admin, dni="30111333").json()["codigo_acceso"]

    assert primero != segundo
    assert "30111222" not in primero


def test_un_dni_repetido_da_409(admin):
    alta(admin)

    assert alta(admin, nombre="Otra Persona").status_code == 409


def test_un_dni_con_letras_o_un_nombre_corto_da_422(admin):
    assert alta(admin, dni="12AB5678").status_code == 422
    assert alta(admin, nombre="A").status_code == 422


def test_el_listado_no_muestra_el_codigo_ni_el_hash(admin):
    alta(admin)

    respuesta = admin.get("/alumnos")

    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 1
    assert "codigo" not in respuesta.text


def test_se_busca_por_nombre_o_por_dni(admin):
    alta(admin)
    alta(admin, nombre="Luis Díaz", dni="28999000")

    assert len(admin.get("/alumnos", params={"buscar": "ana"}).json()) == 1
    assert admin.get("/alumnos", params={"buscar": "2899"}).json()[0]["nombre"] == "Luis Díaz"
    assert admin.get("/alumnos", params={"buscar": "zzz"}).json() == []


def test_se_edita_un_alumno(admin):
    alumno_id = alta(admin).json()["id"]

    respuesta = admin.put(f"/alumnos/{alumno_id}", json={**NUEVO, "contacto": "ana@correo.com"})

    assert respuesta.status_code == 200
    assert admin.get(f"/alumnos/{alumno_id}").json()["contacto"] == "ana@correo.com"


def test_editar_con_el_dni_de_otro_alumno_da_409(admin):
    alta(admin)
    otro_id = alta(admin, dni="28999000").json()["id"]

    respuesta = admin.put(f"/alumnos/{otro_id}", json=NUEVO)

    assert respuesta.status_code == 409


def test_editar_sin_cambiar_el_dni_no_da_error(admin):
    alumno_id = alta(admin).json()["id"]

    respuesta = admin.put(f"/alumnos/{alumno_id}", json={**NUEVO, "nombre": "Ana María Pérez"})

    assert respuesta.status_code == 200


def test_un_alumno_que_no_existe_da_404(admin):
    assert admin.get("/alumnos/999").status_code == 404
    assert admin.put("/alumnos/999", json=NUEVO).status_code == 404
    assert admin.patch("/alumnos/999/desactivar").status_code == 404
    assert admin.post("/alumnos/999/codigo-acceso").status_code == 404


def test_la_baja_es_logica_y_se_puede_reactivar(admin):
    alumno_id = alta(admin).json()["id"]

    baja = admin.patch(f"/alumnos/{alumno_id}/desactivar")

    assert baja.status_code == 200
    assert baja.json()["activo"] is False
    # El registro sigue existiendo y se puede consultar (RN14)
    assert admin.get(f"/alumnos/{alumno_id}").json()["activo"] is False
    assert len(admin.get("/alumnos").json()) == 1
    assert admin.patch(f"/alumnos/{alumno_id}/activar").json()["activo"] is True


def test_regenerar_el_codigo_invalida_el_anterior(admin):
    creado = alta(admin).json()

    nuevo = admin.post(f"/alumnos/{creado['id']}/codigo-acceso").json()["codigo_acceso"]

    assert nuevo != creado["codigo_acceso"]
    uow = UnitOfWork()
    with uow:
        hash_guardado = uow.alumnos.get_by_id(creado["id"]).codigo_acceso_hash
        assert verify_password(nuevo, hash_guardado)
        assert not verify_password(creado["codigo_acceso"], hash_guardado)
