from app.core.uow import UnitOfWork

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