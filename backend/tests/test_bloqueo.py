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