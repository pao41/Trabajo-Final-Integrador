from fastapi.testclient import TestClient

from app.main import app

NUEVA = {
    "nombre_gimnasio": "Gimnasio Central",
    "dias_aviso_vencimiento": 10,
    "metodos_pago_habilitados": ["efectivo", "transferencia"],
}


def test_sin_sesion_no_se_ve_la_configuracion(client):
    assert client.get("/configuracion").status_code == 401


def test_el_entrenador_no_puede_ver_la_configuracion(
    crear_usuario, crear_entrenador, iniciar_sesion
):
    crear_usuario("laura", rol="entrenador", entrenador_id=crear_entrenador())
    entrenador = TestClient(app)
    iniciar_sesion(entrenador, "laura")

    assert entrenador.get("/configuracion").status_code == 403


def test_la_primera_vez_devuelve_valores_por_defecto(admin):
    datos = admin.get("/configuracion").json()

    assert datos["dias_aviso_vencimiento"] == 7
    assert datos["metodos_pago_habilitados"] == ["efectivo", "transferencia", "debito", "credito"]


def test_se_guarda_y_se_consulta_la_configuracion(admin):
    guardada = admin.put("/configuracion", json=NUEVA)

    assert guardada.status_code == 200
    assert admin.get("/configuracion").json() == NUEVA


def test_hay_una_sola_configuracion(admin):
    admin.put("/configuracion", json=NUEVA)
    admin.put("/configuracion", json={**NUEVA, "nombre_gimnasio": "Otro nombre"})

    assert admin.get("/configuracion").json()["nombre_gimnasio"] == "Otro nombre"


def test_los_dias_de_aviso_tienen_que_ser_positivos(admin):
    assert (
        admin.put("/configuracion", json={**NUEVA, "dias_aviso_vencimiento": 0}).status_code == 422
    )


def test_hace_falta_al_menos_un_metodo_de_pago_valido(admin):
    sin_metodos = {**NUEVA, "metodos_pago_habilitados": []}
    invalido = {**NUEVA, "metodos_pago_habilitados": ["bitcoin"]}

    assert admin.put("/configuracion", json=sin_metodos).status_code == 422
    assert admin.put("/configuracion", json=invalido).status_code == 422


def test_el_nombre_del_gimnasio_se_ve_sin_iniciar_sesion(admin):
    sin_sesion = TestClient(app)

    por_defecto = sin_sesion.get("/configuracion/publica")
    admin.put("/configuracion", json=NUEVA)
    cambiado = sin_sesion.get("/configuracion/publica")

    assert por_defecto.json() == {"nombre_gimnasio": "Mi gimnasio"}
    assert cambiado.json() == {"nombre_gimnasio": "Gimnasio Central"}
    # Solo se publica el nombre: el resto de la configuración sigue siendo del administrador
    assert sin_sesion.get("/configuracion").status_code == 401
