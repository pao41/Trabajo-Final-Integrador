from app.core.config import settings

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
