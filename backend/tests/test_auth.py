from datetime import datetime, timedelta, timezone

import jwt
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app


MENSAJE_GENERICO = "Usuario o contraseña incorrectos"


def test_cp25_login_correcto_deja_la_sesion_en_una_cookie_httponly(
    client, crear_usuario, iniciar_sesion
):
    crear_usuario("admin")

    respuesta = iniciar_sesion(client, "admin")

    assert respuesta.status_code == 200
    cookie = respuesta.headers["set-cookie"].lower()
    assert "httponly" in cookie
    assert "samesite=lax" in cookie
    assert f"max-age={settings.access_token_expire_minutes * 60}" in cookie
    # El token viaja solo en la cookie, nunca en el cuerpo de la respuesta
    assert respuesta.json() == {"mensaje": "Sesión iniciada"}


def test_cp25_el_usuario_se_escribe_sin_distinguir_mayusculas(
    client, crear_usuario, iniciar_sesion
):
    crear_usuario("admin")

    respuesta = iniciar_sesion(client, "  ADMIN ")

    assert respuesta.status_code == 200


def test_cp25_contrasena_incorrecta_da_401_con_mensaje_generico(
    client, crear_usuario, iniciar_sesion
):
    crear_usuario("admin")

    respuesta = iniciar_sesion(client, "admin", "otra-clave-incorrecta")

    assert respuesta.status_code == 401
    assert respuesta.json()["detail"] == MENSAJE_GENERICO
    assert "set-cookie" not in respuesta.headers


def test_cp25_usuario_inexistente_da_el_mismo_mensaje(client, iniciar_sesion):
    respuesta = iniciar_sesion(client, "no-existe")

    assert respuesta.status_code == 401
    assert respuesta.json()["detail"] == MENSAJE_GENERICO


def test_me_sin_sesion_da_401(client):
    assert client.get("/auth/me").status_code == 401


def test_me_con_sesion_devuelve_el_usuario_sin_contrasena(admin):
    respuesta = admin.get("/auth/me")

    assert respuesta.status_code == 200
    assert respuesta.json()["nombre_usuario"] == "admin"
    assert respuesta.json()["rol"] == "administrador"
    assert "password" not in respuesta.text


def test_el_encabezado_authorization_no_se_acepta(admin):
    token = admin.cookies.get("access_token")
    otro_cliente = TestClient(app)

    respuesta = otro_cliente.get("/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert respuesta.status_code == 401


def test_logout_borra_la_cookie(admin):
    admin.post("/auth/logout")

    assert admin.get("/auth/me").status_code == 401


def test_cp26_un_entrenador_no_puede_gestionar_usuarios(
    client, crear_usuario, crear_entrenador, iniciar_sesion
):
    entrenador_id = crear_entrenador()
    crear_usuario("laura", rol="entrenador", entrenador_id=entrenador_id)
    iniciar_sesion(client, "laura")
    nuevo = {"nombre_usuario": "marta", "password": "clave-marta-123"}

    assert client.get("/usuarios").status_code == 403
    assert client.post("/usuarios", json=nuevo).status_code == 403


def test_un_token_vencido_da_401(client):
    ayer = datetime.now(timezone.utc) - timedelta(days=1)
    vencido = jwt.encode({"sub": "1", "exp": ayer}, settings.secret_key, algorithm="HS256")
    client.cookies.set("access_token", vencido)

    assert client.get("/auth/me").status_code == 401


def test_un_token_firmado_con_otra_clave_da_401(client):
    manana = datetime.now(timezone.utc) + timedelta(days=1)
    falso = jwt.encode({"sub": "1", "exp": manana}, "otra-clave-" * 5, algorithm="HS256")
    client.cookies.set("access_token", falso)

    assert client.get("/auth/me").status_code == 401


def test_cp29_un_usuario_desactivado_no_puede_iniciar_sesion(admin, crear_usuario, iniciar_sesion):
    marta_id = crear_usuario("marta")

    admin.patch(f"/usuarios/{marta_id}/desactivar")

    assert iniciar_sesion(TestClient(app), "marta").status_code == 401


def test_cp29_desactivar_corta_tambien_la_sesion_ya_abierta(admin, crear_usuario, iniciar_sesion):
    marta_id = crear_usuario("marta")
    sesion_de_marta = TestClient(app)
    iniciar_sesion(sesion_de_marta, "marta")
    assert sesion_de_marta.get("/auth/me").status_code == 200

    admin.patch(f"/usuarios/{marta_id}/desactivar")

    assert sesion_de_marta.get("/auth/me").status_code == 401
