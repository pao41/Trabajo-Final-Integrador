from fastapi.testclient import TestClient

from app.main import app

NUEVO = {"nombre": "Laura Gómez", "contacto": "387-4111111"}


def alta(admin, **cambios):
    """Da de alta un entrenador por la API y devuelve la respuesta."""
    return admin.post("/entrenadores", json={**NUEVO, **cambios})


def usuario_entrenador(admin, entrenador_id, nombre="laura"):
    """Crea el usuario de un entrenador por la API y devuelve la respuesta."""
    datos = {
        "nombre_usuario": nombre,
        "password": "clave-laura-123",
        "rol": "entrenador",
        "entrenador_id": entrenador_id,
    }
    return admin.post("/usuarios", json=datos)


def test_solo_el_administrador_gestiona_entrenadores(
    client, crear_usuario, crear_entrenador, iniciar_sesion
):
    crear_usuario("laura", rol="entrenador", entrenador_id=crear_entrenador())
    entrenador = TestClient(app)
    iniciar_sesion(entrenador, "laura")

    assert client.get("/entrenadores").status_code == 401
    assert entrenador.get("/entrenadores").status_code == 403
    assert entrenador.post("/entrenadores", json=NUEVO).status_code == 403


def test_el_administrador_da_de_alta_edita_y_lista_entrenadores(admin):
    creado = alta(admin)
    entrenador_id = creado.json()["id"]
    cambios = {"nombre": "Laura Gómez Díaz", "contacto": None}

    editado = admin.put(f"/entrenadores/{entrenador_id}", json=cambios)

    assert creado.status_code == 201
    assert editado.json()["nombre"] == "Laura Gómez Díaz"
    assert editado.json()["contacto"] is None
    assert [e["nombre"] for e in admin.get("/entrenadores").json()] == ["Laura Gómez Díaz"]
    assert admin.put("/entrenadores/999", json=NUEVO).status_code == 404


def test_un_entrenador_con_su_usuario_entra_pero_no_gestiona(admin, iniciar_sesion):
    entrenador_id = alta(admin).json()["id"]

    creado = usuario_entrenador(admin, entrenador_id)
    sesion = TestClient(app)

    assert creado.status_code == 201
    assert creado.json()["rol"] == "entrenador"
    assert creado.json()["entrenador_id"] == entrenador_id
    assert iniciar_sesion(sesion, "laura", "clave-laura-123").status_code == 200
    assert sesion.get("/auth/me").json()["rol"] == "entrenador"
    assert sesion.get("/alumnos").status_code == 403


def test_el_usuario_entrenador_exige_un_entrenador_valido_y_libre(admin):
    entrenador_id = alta(admin).json()["id"]
    sin_entrenador = {"nombre_usuario": "pedro", "password": "clave-pedro-123", "rol": "entrenador"}

    assert admin.post("/usuarios", json=sin_entrenador).status_code == 422
    assert usuario_entrenador(admin, 999).status_code == 404
    assert usuario_entrenador(admin, entrenador_id).status_code == 201
    # Un entrenador tiene un solo usuario
    assert usuario_entrenador(admin, entrenador_id, nombre="otro").status_code == 409
    # Un administrador no lleva entrenador
    datos = {
        "nombre_usuario": "marta",
        "password": "clave-marta-123",
        "entrenador_id": entrenador_id,
    }
    assert admin.post("/usuarios", json=datos).status_code == 422