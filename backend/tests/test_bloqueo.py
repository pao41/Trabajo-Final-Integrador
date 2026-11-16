from datetime import timedelta

from fastapi.testclient import TestClient

from app.core import bloqueo
from app.core.clock import now_ar
from app.main import app

MENSAJE_GENERICO = "Usuario o contraseña incorrectos"


def fallar(client, iniciar_sesion, veces, nombre="admin"):
    """Intenta iniciar sesión con una contraseña incorrecta varias veces."""
    for _ in range(veces):
        iniciar_sesion(client, nombre, "clave-incorrecta")


def test_los_primeros_cinco_fallos_dan_el_mensaje_generico(client, crear_usuario, iniciar_sesion):
    crear_usuario("admin")

    for _ in range(5):
        respuesta = iniciar_sesion(client, "admin", "clave-incorrecta")
        assert respuesta.status_code == 401
        assert respuesta.json()["detail"] == MENSAJE_GENERICO


def test_despues_de_cinco_fallos_el_usuario_queda_bloqueado(client, crear_usuario, iniciar_sesion):
    crear_usuario("admin")
    fallar(client, iniciar_sesion, 5)

    # Con la contraseña correcta tampoco entra mientras dure el bloqueo
    respuesta = iniciar_sesion(client, "admin")

    assert respuesta.status_code == 429
    assert "Demasiados intentos fallidos" in respuesta.json()["detail"]
    assert "set-cookie" not in respuesta.headers


def test_un_acierto_borra_los_fallos_anteriores(client, crear_usuario, iniciar_sesion):
    crear_usuario("admin")
    fallar(client, iniciar_sesion, 4)
    assert iniciar_sesion(client, "admin").status_code == 200

    fallar(client, iniciar_sesion, 4)

    # Son 4 fallos seguidos, no 8: todavía puede entrar
    assert iniciar_sesion(client, "admin").status_code == 200


def test_el_bloqueo_de_un_usuario_no_afecta_a_otro(client, crear_usuario, iniciar_sesion):
    crear_usuario("admin")
    crear_usuario("marta")
    fallar(client, iniciar_sesion, 5, "admin")

    assert iniciar_sesion(TestClient(app), "marta").status_code == 200


def test_un_usuario_que_no_existe_tambien_se_bloquea(client, iniciar_sesion):
    fallar(client, iniciar_sesion, 5, "no-existe")

    assert iniciar_sesion(client, "no-existe").status_code == 429


def test_el_bloqueo_termina_a_los_quince_minutos(
    client, crear_usuario, iniciar_sesion, monkeypatch
):
    crear_usuario("admin")
    fallar(client, iniciar_sesion, 5)
    assert iniciar_sesion(client, "admin").status_code == 429

    # Se simula que pasaron 16 minutos
    despues = now_ar() + timedelta(minutes=16)
    monkeypatch.setattr(bloqueo, "now_ar", lambda: despues)

    assert iniciar_sesion(client, "admin").status_code == 200
