from fastapi.testclient import TestClient

from app.core.uow import UnitOfWork
from app.main import app


NUEVO = {"nombre_usuario": "Marta", "password": "clave-marta-123"}


def test_sin_sesion_no_se_puede_gestionar_usuarios(client):
    assert client.get("/usuarios").status_code == 401


def test_el_administrador_crea_un_usuario(admin):
    respuesta = admin.post("/usuarios", json=NUEVO)

    assert respuesta.status_code == 201
    assert respuesta.json()["nombre_usuario"] == "marta"
    assert respuesta.json()["rol"] == "administrador"
    # La respuesta nunca incluye la contraseña ni su hash
    assert "password" not in respuesta.text


def test_la_base_guarda_el_hash_y_no_la_contrasena(admin):
    admin.post("/usuarios", json=NUEVO)

    uow = UnitOfWork()
    with uow:
        guardado = uow.usuarios.get_by_nombre_usuario("marta")
        assert guardado.password_hash.startswith("$2b$")
        assert "clave-marta-123" not in guardado.password_hash


def test_el_usuario_creado_puede_iniciar_sesion(admin, iniciar_sesion):
    admin.post("/usuarios", json=NUEVO)

    assert iniciar_sesion(TestClient(app), "marta", "clave-marta-123").status_code == 200


def test_un_nombre_repetido_da_409_aunque_cambien_las_mayusculas(admin):
    admin.post("/usuarios", json=NUEVO)

    respuesta = admin.post("/usuarios", json={**NUEVO, "nombre_usuario": "MARTA"})

    assert respuesta.status_code == 409


def test_una_contrasena_corta_da_422(admin):
    respuesta = admin.post("/usuarios", json={**NUEVO, "password": "corta"})

    assert respuesta.status_code == 422


def test_una_contrasena_de_mas_de_72_bytes_da_422_y_no_un_error_del_servidor(admin):
    # 40 letras con tilde ocupan 80 bytes, aunque tengan menos de 72 caracteres
    respuesta = admin.post("/usuarios", json={**NUEVO, "password": "ñ" * 40})

    assert respuesta.status_code == 422


def test_el_listado_muestra_los_usuarios_sin_contrasena(admin):
    admin.post("/usuarios", json=NUEVO)

    respuesta = admin.get("/usuarios")

    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 2
    assert "password" not in respuesta.text
